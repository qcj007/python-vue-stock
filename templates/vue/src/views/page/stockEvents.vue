<template>
  <div class="minions-content">
    <div class="minions-head">
      <div></div>
      <div class="btn-cont">
        <a-button @click="isEditShow = true">新增</a-button>
        <a-button @click="handleExport">导出</a-button>
        <a-button type="primary" @click="searchStockList">刷新</a-button>
      </div>
    </div>
    <div class="minions-body">
      <zcw-table :columns="columns" :stocksList="stocksList" v-slot="slotProps">
        <a @click="onEditEvent(slotProps.record)" style="margin-right: 10px">编辑</a>
        <a-popconfirm title="确定要删除这个股票?" @confirm="onDelete(slotProps.record.id)">
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
        <a-form-item label="事件时间" :rules="[{ required: true }]">
          <a-date-picker v-model:value="addForm.eventTime" />
        </a-form-item>
        <a-form-item label="股票时间" :rules="[{ required: true }]">
          <a-range-picker v-model:value="addForm.stockTime" />
        </a-form-item>

        <a-form-item label="事件备注" :rules="[{ required: true }]">
          <a-textarea
            v-model:value="addForm.eventRemark"
            placeholder="输入事件备注"
            :auto-size="{ minRows: 2, maxRows: 5 }"
          />
        </a-form-item>
      </a-form>
    </div>
    <template #footer>
      <a-button @click="onClose">取消</a-button>
      <a-button type="primary" @click="onAddStock">确定</a-button>
    </template>
  </a-modal>
</template>

<script setup>
import { useStore } from "vuex"
import {
  editStocksEvents,
  deleteStocksEvents,
  addStocksEvents,
  searchStockInfo,
  editZcwStocks
} from "@/api"
import { computed, ref, watch, onMounted, reactive, nextTick } from "vue"
import { round, cloneDeep, isEqual } from "lodash-es"
import useStockEvents from "@/hooks/useStockEvents"
import useExcel from "@/hooks/useExcel"
import useStockZcw from "@/hooks/useStockZcw"
import { message } from "ant-design-vue"
import dayjs, { Dayjs } from "dayjs"
import zcwTable from "@/components/zcw-table.vue"

const dateFormat = "YYYY-MM-DD"
const store = useStore()
const isEditShow = ref(false)

const addFormObj = {
  code: "",
  house: "",
  name: "",
  industry: "",
  eventTime: "",
  stockTime: [],
  eventRemark: "",
  buyPrice: "",
  stopSurplus: "",
  stopLoss: "",
  isExist: false
}

const addForm = ref(cloneDeep(addFormObj))

const { columns, state, searchStockList, stocksList } = useStockEvents()
const { onCodeChange, onAddZcwStock, onBuyPriceBlur,onEditStock } = useStockZcw()
const { exportEecel } = useExcel()

const editEventData = ref({})
// 编辑事件
const onEditEvent = (event) => {
  const {
    code,
    house,
    name,
    eventTime,
    eventRemark,
    startTime,
    endTime,
    buyPrice,
    stopSurplus,
    stopLoss
  } = event
  editEventData.value = event
  addForm.value = {
    code,
    house,
    name,
    eventRemark,
    eventTime: dayjs(eventTime, dateFormat),
    stockTime: [dayjs(startTime, dateFormat), dayjs(endTime, dateFormat)],
    buyPrice,
    stopSurplus,
    stopLoss,
    isExist: true
  }
  isEditShow.value = true
}

// 删除一条记录
const onDelete = async (id) => {
  const params = {
    list: [id]
  }
  const { errcode, data } = await deleteStocksEvents(params)
  if (errcode == 0) {
    message.success("删除成功")
    state.list = state.list.filter((item) => id !== item.id)
  }
}
// 导出
const handleExport = () => {
  exportEecel(stocksList.value, columns, `支撑位_${store.getters.getYMDate}`)
}

// 新增
const onAddStock = async () => {
  const { stockTime, eventTime, code, house, name, eventRemark ,isExist} = addForm.value
  if (code.length != 6) {
    message.warn("请输入正确的股票代码")
    return
  }
  const { id } = editEventData.value

  if (!isExist && !id) {
    const res = await onAddZcwStock(addForm.value)
    if (!res) {
      message.error("新增支撑位股票失败")
      return
    }
  }else{
    const res = await onEditStock(addForm.value)
    if (!res) {
      message.error("修改股票失败")
      return
    }
  }

  
  const params = {
    id,
    code,
    house,
    name,
    eventRemark,
    startTime: dayjs(stockTime[0]).format(dateFormat),
    endTime: dayjs(stockTime[1]).format(dateFormat),
    eventTime: dayjs(eventTime).format(dateFormat)
  }

  const onSaveFun = id ? editStocksEvents : addStocksEvents
  const { errcode, data } = await onSaveFun(params)
  if (errcode == 0) {
    message.success(`${id ? "修改" : "新增"}成功`)
    isEditShow.value = false
    searchStockList()
    editEventData.value = {}
    addForm.value = cloneDeep(addFormObj)
  }
}

const onClose = () => {
  isEditShow.value = false
  const { id } = editEventData.value
  if (id) {
    editEventData.value = {}
    addForm.value = cloneDeep(addFormObj)
  }
}
</script>
