<template>
  <div class="minions-content">
    <div class="minions-left">
      <div class="left-head">
        <h6>行业概念</h6>
        <a-button @click="state.isEditIndustry = !state.isEditIndustry">
          {{ state.isEditIndustry ? "确定" : "编辑" }}
        </a-button>
      </div>
      <div class="left-body">
        <vuedraggable
          :list="industryList"
          ghost-class="ghost"
          chosen-class="chosenClass"
          animation="300"
          itemKey="id"
          @update="editIndustrySort"
        >
          <template #item="{ element, index }">
            <div
              class="left-li"
              :class="{ s: state.industryCheckedId == element.id }"
              @click="state.industryCheckedId = element.id"
            >
              <span>{{ element.name }}</span>
              <a-popconfirm title="确定要删除这个行业概念?" @confirm="onDeleteIndustry(element.id)">
                <div class="icon-close" v-if="state.isEditIndustry"></div>
              </a-popconfirm>
            </div>
          </template>
        </vuedraggable>
        <div
          class="left-li-add-btn"
          v-if="state.isEditIndustry"
          @click="state.isAddIndustryShow = true"
        >
          新增
        </div>
      </div>
    </div>
    <div class="minions-right">
      <div class="right-head">
        <a-button type="primary" @click="searchStockList(stocksCodeList)">刷新</a-button>
        <a-button @click="handleExport">导出</a-button>
        <a-button type="primary" @click="state.isEditShow = true">新增</a-button>
      </div>
      <div class="right-body">
        <zcw-table :columns="columns" :stocksList="stocksList" v-slot="slotProps">
          <a-popconfirm title="确定要删除这个股票?" @confirm="onDeleteStock(slotProps.record.code)">
            <a>删除</a>
          </a-popconfirm>
        </zcw-table>
      </div>
    </div>
  </div>
  <a-modal class="infoTips" v-model:visible="state.isAddIndustryShow" width="400px">
    <template #title>
      <div class="info-header">新增行业概念</div>
    </template>
    <div class="info-content">
      <a-form
        :model="addForm"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
        autocomplete="off"
      >
        <a-form-item label="行业概念" :rules="[{ required: true }]">
          <a-input v-model:value="state.addIndustryName" placeholder="行业概念" />
        </a-form-item>
      </a-form>
    </div>
    <template #footer>
      <a-button @click="state.isAddIndustryShow = false">取消</a-button>
      <a-button type="primary" @click="onAddIndustry">确定</a-button>
    </template>
  </a-modal>

  <a-modal
    class="infoTips"
    v-model:visible="state.isEditShow"
    width="400px"
    @cancel="state.isEditShow = false"
  >
    <template #title>
      <div class="info-header">新增股票</div>
    </template>
    <div class="info-content">
      <a-form
        :model="addForm"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
        autocomplete="off"
      >
        <a-form-item label="股票代码" :rules="[{ required: true }]">
          <a-input
            v-model:value="addForm.code"
            style="width: 35%"
            placeholder="股票代码"
            @change="onCodeChange(addForm)"
            ref="codeRef"
          />
          &nbsp;

          <span>{{ addForm.name }}{{ addForm.industry }}</span>
        </a-form-item>

        <a-form-item label="买入价" :rules="[{ required: true }]">
          <a-input-number
            v-model:value="addForm.buyPrice"
            :min="0"
            placeholder="请输入股票买入价格"
            @blur="onBuyPriceBlur(addForm)"
          />
        </a-form-item>

        <a-form-item label="止盈" :rules="[{ required: true }]">
          <a-input-number
            v-model:value="addForm.stopSurplus"
            :min="0"
            placeholder="请输入股票止盈价格"
          />
        </a-form-item>

        <a-form-item label="止损" :rules="[{ required: true }]">
          <a-input-number
            v-model:value="addForm.stopLoss"
            :min="0"
            placeholder="请输入股票止损价格"
          />
        </a-form-item>
      </a-form>
    </div>
    <template #footer>
      <a-button @click="state.isEditShow = false">取消</a-button>
      <a-button type="primary" @click="onAddIndustryStock">确定</a-button>
    </template>
  </a-modal>
</template>

<script setup>
import vuedraggable from "vuedraggable"
import { useStore } from "vuex"
import { computed, ref, watch, onMounted, reactive, nextTick } from "vue"
import { round, cloneDeep, isEqual } from "lodash-es"
import { convertDateFormat, getStockHouse } from "@/plugins/utils/index"
import zcwTable from "@/components/zcw-table.vue"
import useStockZcw from "@/hooks/useStockZcw"
import useExcel from "@/hooks/useExcel"
import {
  editStocksConcepts,
  searchStocksConcepts,
  deleteStocksConcepts,
  addStocksConcepts
} from "@/api"
import { message } from "ant-design-vue"
const store = useStore()
const {
  columns,
  searchStockList,
  onCodeChange,
  onAddZcwStock,
  stocksList,
  zcwlist,
  onBuyPriceBlur,
  onEditStock
} = useStockZcw()
const state = reactive({
  isEditIndustry: false,
  industryCheckedId: "",
  list: [],
  addIndustryName: "",
  isAddIndustryShow: false,
  isEditShow: false,
  stocksCodeList: []
})

const codeRef = ref(null)
watch(
  () => state.isEditShow,
  () => {
    if (state.isEditShow) {
      setTimeout(() => {
        codeRef.value.focus()
      }, 100)
    }
  }
)

const addFormObj = {
  code: "",
  buyPrice: "",
  stopSurplus: "",
  stopLoss: "",
  house: "",
  name: "",
  isExist: "",
  industry: ""
}

const addForm = ref(cloneDeep(addFormObj))

const industryList = computed(() => {
  const list = cloneDeep(state.list)
  return list.sort((a, b) => a.sort - b.sort)
})

// 查询行业概念
const onSearchConcepts = async () => {
  const { errcode, data } = await searchStocksConcepts({})
  if (errcode == 0) {
    state.list = data
    if (state.list.length > 0 && !state.industryCheckedId) {
      nextTick(() => {
        state.industryCheckedId = industryList.value[0].id
      })
    }
  }
}

// 修改行业排序
const editIndustrySort = async (evt) => {
  state.list = cloneDeep(industryList.value).map((item, index) => {
    item.sort = index
    return item
  })
  const params = {
    list: state.list
  }
  const { errcode, data } = await editStocksConcepts(params)
}

const checkedIndustry = computed(() => {
  return state.list.find((item) => item.id == state.industryCheckedId) || {}
})

const stocksCodeList = computed(() => {
  const stocks = checkedIndustry.value?.stocks || ""
  return stocks.split(",").filter((item) => item)
})

watch(
  () => stocksCodeList.value,
  (val) => {
    if (val.length > 0) {
      searchStockList(val)
    } else {
      zcwlist.value = []
    }
  },
  { deep: true }
)

// 删除行业股票
const onDeleteStock = async (code) => {
  const codeList = cloneDeep(stocksCodeList.value).filter((item) => item != code)
  const industry = cloneDeep(checkedIndustry.value)
  industry.stocks = codeList.join(",")
  const params = {
    list: [industry]
  }
  const { errcode, data } = await editStocksConcepts(params)
  if (errcode == 0) {
    message.success(`删除成功`)
    onSearchConcepts()
  }
}

// 添加行业股票
const onAddIndustryStock = async () => {
  const { code, name, isExist } = addForm.value
  if (code.length != 6) {
    message.warn("请输入正确的股票代码")
    return
  }

  if (stocksCodeList.value.includes(code)) {
    message.warn("股票已存在")
    return
  }

  if (!isExist) {
    const res = await onAddZcwStock(addForm.value)
    if (!res) {
      message.error("新增股票失败")
      return
    }
  }else{
    const res = await onEditStock(addForm.value)
    if (!res) {
      message.error("修改股票失败")
      return
    }
  }
  const codeList = [code, ...stocksCodeList.value]
  const industry = cloneDeep(checkedIndustry.value)
  industry.stocks = codeList.join(",")
  const params = {
    list: [industry]
  }
  const { errcode, data } = await editStocksConcepts(params)
  if (errcode == 0) {
    message.success(`新增成功`)
    state.isEditShow = false
    addForm.value = cloneDeep(addFormObj)
    onSearchConcepts()
  }
}

// 新增行业
const onAddIndustry = async () => {
  const params = {
    sort: state.list.length,
    name: state.addIndustryName
  }
  const { errcode, data } = await addStocksConcepts(params)
  if (errcode == 0) {
    state.list = data
    state.isAddIndustryShow = false
    state.addIndustryName = ""
  }
}

// 删除行业
const onDeleteIndustry = async (id) => {
  const { errcode, data } = await deleteStocksConcepts({ id })
  if (errcode == 0) {
    state.list = data
    if (state.list.length > 0 && id == state.industryCheckedId) {
      state.industryCheckedId = state.list[0].id
    }
  }
}
const { exportEecel } = useExcel()
// 导出
const handleExport = () => {
  const { name } = checkedIndustry.value
  exportEecel(stocksList.value, columns, `${name}_${store.getters.getYMDate}`)
}
onMounted(() => {
  onSearchConcepts()
})
</script>
<style lang="less" scoped>
@leftWidth: 180px;
.minions-content {
  padding: 10px 0;
  display: flex;
  justify-content: space-between;
  .minions-left {
    width: @leftWidth;
    height: 100%;
    border-right: 1px solid #ccc;

    .left-head {
      width: 100%;
      height: 50px;
      display: flex;
      justify-content: space-between;
      padding-right: 10px;
      h6 {
        font-size: 16px;
        font-weight: bold;
        line-height: 32px;
      }
    }
    .left-body {
      width: 100%;
      height: calc(100% - 50px);
      overflow-y: auto;
      .left-li-add-btn {
        width: 80%;
        font-size: 12px;
        color: #1890ff;
        border: 1px solid #1890ff;
        line-height: 30px;
        text-align: center;
        user-select: none;
        cursor: pointer;
        margin: 10px auto;
        border-radius: 4px;
      }
      .left-li {
        width: 100%;
        font-size: 14px;
        line-height: 40px;
        cursor: pointer;
        user-select: none;
        position: relative;
        text-align: center;
        &:hover {
          color: #1890ff;
        }
        &.s {
          color: #fff;
          background: #1890ff;
        }
        .icon-close {
          width: 20px;
          height: 20px;
          background: url("../../assets/images/m_close.png");
          background-size: cover;
          position: absolute;
          right: 20px;
          top: 10px;
          display: none;
        }
        &:hover {
          .icon-close {
            display: block;
          }
        }
      }
    }
  }
  .minions-right {
    width: calc(100% - @leftWidth);

    height: 100%;
    .right-head {
      width: 100%;
      height: 50px;
      display: flex;
      justify-content: right;
      button {
        margin-left: 10px;
      }
    }
    .right-body {
      width: 100%;
      height: calc(100% - 50px);
      padding-left: 10px;
    }
  }
}
</style>
