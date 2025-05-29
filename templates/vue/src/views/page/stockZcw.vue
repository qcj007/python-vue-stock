<template>
  <div class="minions-content">
    <div class="minions-head">
      <div></div>
      <div class="btn-cont">
        <a-button @click="isEditShow = true">新增</a-button>
        <a-button @click="handleExport">导出</a-button>
        <a-button type="primary" @click="searchStockList()">刷新</a-button>
      </div>
    </div>
    <div class="minions-body">
      <zcw-table :columns="columns" :stocksList="stocksList" v-slot="slotProps">
        <a-popconfirm title="确定要删除这个股票?" @confirm="onDeleteStock(slotProps.record.code)">
          <a>删除</a>
        </a-popconfirm>
      </zcw-table>
    </div>
  </div>
  <a-modal class="infoTips" v-model:visible="isEditShow" width="400px" @cancel="isEditShow = false">
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
          />
          &nbsp;
          <span style="color: red" v-if="addForm.isExist">{{ addForm.name }}（已存在）</span>
          <span v-else>{{ addForm.name }}{{ addForm.industry }}</span>
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
      <a-button @click="isEditShow = false">取消</a-button>
      <a-button type="primary" @click="onAddStock">确定</a-button>
    </template>
  </a-modal>
</template>

<script setup>
import { useStore } from "vuex"
import { deleteZcwStocks, addZcwStocks } from "@/api"
import { computed, ref, watch, onMounted, reactive, nextTick } from "vue"
import { round, cloneDeep, isEqual } from "lodash-es"
import useStockZcw from "@/hooks/useStockZcw"
import useExcel from "@/hooks/useExcel"
import { message } from "ant-design-vue"
import zcwTable from "@/components/zcw-table.vue"
const store = useStore()
const isEditShow = ref(false)

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

const { columns, searchStockList, stocksList, onCodeChange, onAddZcwStock ,zcwlist,onBuyPriceBlur} = useStockZcw()
const { exportEecel } = useExcel()

// 删除一条记录
const onDeleteStock = async (code) => {
  const params = {
    list: [code]
  }
  const { errcode, data } = await deleteZcwStocks(params)
  if (errcode == 0) {
    message.success("删除成功")
    zcwlist.value = zcwlist.value.filter((item) => code !== item.code)
  }
}


// 新增
const onAddStock = async () => {
  if(addForm.isExist){
    message.error("该股票已存在")
    return
  }
  const res = await onAddZcwStock(addForm.value)
  if (res) {
    message.success("新增成功")
    isEditShow.value = false
    searchStockList()
    addForm.value = cloneDeep(addForm.value)
  }else{
    message.error("新增失败")
  }
}


// 导出
const handleExport = () => {
  exportEecel(stocksList.value, columns, `支撑位_${store.getters.getYMDate}`)
}
onMounted(() => {
  searchStockList()
})
</script>
