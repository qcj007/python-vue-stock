<template>
  <div class="head-opportunity">
    <a-button @click="state.isEditBtnShow = !state.isEditBtnShow">
      {{ state.isEditBtnShow ? "确定" : "编辑" }}
    </a-button>
    <a-button type="primary" @click="state.isEditShow = true" v-if="state.isEditBtnShow">
      新增
    </a-button>
  </div>
  <div class="app-opportunity">
    <vuedraggable
      :list="state.list"
      ghost-class="ghost"
      chosen-class="chosenClass"
      animation="300"
      itemKey="id"
      @update="editIndustrySort"
    >
      <template #item="{ element, index }">
        <div class="opportunity-li">
          <div class="opportunity-head">
            <h6>{{ element.title }}</h6>
            <div class="btn-right" v-if="state.isEditBtnShow">
              <a-popconfirm title="确定要删除这个框架?" @confirm="onDeleteOty(element)">
                <div class="btn">删除</div>
              </a-popconfirm>
              <div class="btn" @click="onEditOty(element)" style="color: #1890ff">编辑</div>
            </div>
          </div>
          <div class="opportunity-content"><p v-for="(item, index) in element.textList" >{{ item }}</p></div>
        </div>
      </template>
    </vuedraggable>
  </div>
  <a-modal
    class="infoTips"
    v-model:visible="state.isEditShow"
    width="430px"
    @cancel="state.isEditShow = false"
  >
    <template #title>
      <div class="info-header">股票机会</div>
    </template>
    <div class="info-content">
      <a-form
        :model="addForm"
        :label-col="{ span: 6 }"
        :wrapper-col="{ span: 18 }"
        autocomplete="off"
      >
        <a-form-item label="标题" :rules="[{ required: true }]">
          <a-input v-model:value="addForm.title" style="width: 100%" placeholder="输入标题" />
        </a-form-item>
        <a-form-item label="内容" :rules="[{ required: true }]">
          <a-textarea
            v-model:value="addForm.text"
            placeholder="输入内容"
            :auto-size="{ minRows: 5, maxRows: 10 }"
          />
        </a-form-item>
      </a-form>
    </div>
    <template #footer>
      <a-button @click="onClose">取消</a-button>
      <a-button type="primary" @click="onSure">确定</a-button>
    </template>
  </a-modal>
</template>
<script setup>
import vuedraggable from "vuedraggable"
import { computed, ref, watch, onMounted, reactive, nextTick } from "vue"
import { cloneDeep } from "lodash-es"
import { message } from "ant-design-vue"
import {
  searchStockOpportunity,
  addStockOpportunity,
  editStockOpportunity,
  deleteStockOpportunity
} from "@/api/index"
const state = reactive({
  isEditShow: false,
  isEditBtnShow: false,
  list: [],
  shortTerm:
    "4月份：1.旅游概念：往年劳动节、国庆节、春节都会带动旅游概念、旅游股票的上涨。2.chatGPT和sora：GPT5即将发布，sora可能跟着一起公测，关注热点实事和概念股回调。3.消费电子：华为P70即将发布。"
})

const addFormObj = {
  id: "",
  title: "",
  text: "",
  sort: 0
}
const addForm = ref(cloneDeep(addFormObj))
const onClose = () => {
  addForm.value = cloneDeep(addFormObj)
  state.isEditShow = false
}
// 弹窗确定按钮
const onSure = async () => {
  const { id, title, text } = addForm.value
  if (title && text) {
    if (id) {
      onEditOtyFun([addForm.value])
      return
    }
    let params = addForm.value
    params.sort = state.list.length
    const { errcode, data } = await addStockOpportunity(addForm.value)
    if (errcode == 0) {
      addForm.value = cloneDeep(addFormObj)
      state.isEditShow = false
      onSearchsopty()
    }
  } else {
    message.info("请输入标题和内容")
  }
}
// 更新排序
const editIndustrySort = async (e) => {
  state.list = cloneDeep(state.list).map((item, index) => {
    item.sort = index
    return item
  })

  onEditOtyFun(state.list)
}

// 更新
const onEditOtyFun = async (list) => {
  const { errcode, data } = await editStockOpportunity({ list })
  if (errcode == 0) {
    onSearchsopty()
    addForm.value = cloneDeep(addFormObj)
    state.isEditShow = false
  }
}

// 查询列表
const onSearchsopty = async () => {
  const { errcode, data } = await searchStockOpportunity({})
  if (errcode === 0) {
    state.list = data
      .sort((a, b) => a.sort - b.sort)
      .map((item) => {
        item.textList = item.text.split("\n")
        return item
      })
  }
}
// 删除数据
const onDeleteOty = async (cont) => {
  const { errcode, data } = await deleteStockOpportunity({ id: cont.id })
  if (errcode === 0) {
    onSearchsopty()
    message.success("删除成功")
  }
}
const onEditOty = (cont) => {
  addForm.value = cloneDeep(cont)
  state.isEditShow = true
}

onMounted(() => {
  onSearchsopty()
})
</script>
<style lang="less" scoped>
.head-opportunity {
  height: 50px;
  display: flex;
  align-items: center;
  padding-left: 20px;
  button {
    margin-right: 10px;
  }
}
.app-opportunity {
  width: 100%;
  overflow-y: auto;
  height: calc(100% - 55px);
}
.opportunity-li {
  width: calc((100% - 100px) / 5);
  height: 300px;
  border: 1px solid #f1f1f1;
  border-radius: 8px;
  margin: 10px;
  float: left;
  .opportunity-head {
    display: flex;
    height: 50px;
    justify-content: space-between;
    align-items: center;
    border-bottom: 1px solid #f1f1f1;
    h6 {
      font-size: 14px;
      font-weight: 600;
      padding-left: 10px;
    }
    .btn-right {
      padding-right: 20px;
      .btn {
        color: #181818;
        font-size: 12px;
        cursor: pointer;
        user-select: none;
        margin: 0 5px;
        float: left;
      }
    }
  }
  .opportunity-content {
    width: 100%;
    overflow-y: auto;
    margin: 5px 0;
    padding: 0 8px;
    height: calc(100% - 60px);
    p {
        margin-bottom: 5px;
        font-size: 12px;
        line-height: 22px;
    }
  }
}
</style>
