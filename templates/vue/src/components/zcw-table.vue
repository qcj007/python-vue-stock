<template>
  <a-table
    :columns="props.columns"
    :data-source="props.stocksList"
    :pagination="{ pageSize: 100 }"
    :scroll="{ x: 'max-content', y: props.tabHeight || tabHeight }"
    :row-class-name="(_record, index) => (_record.syl <0 ? 'green greenBg' : null)"
  >
    <template #bodyCell="{ column, text, record }">
      <template
        v-if="
          column.dataIndex === 'buyPrice' ||
          column.dataIndex === 'stopSurplus' ||
          column.dataIndex === 'stopLoss'
        "
      >
        <div class="editable-cell">
          <div
            v-if="editableData[record.code] && state.dataIndex === column.dataIndex"
            class="editable-cell-input-wrapper"
          >
            <a-input
              v-model:value="editableData[record.code][column.dataIndex]"
              @pressEnter="onSaveStock(record.code)"
              @blur="onSaveStock(record.code)"
              :ref="(el) => registerRef(el, record.code, column.dataIndex)"
            />
          </div>
          <div
            v-else
            class="editable-cell-text-wrapper"
            @dblclick="onEditClick(record.code, column.dataIndex)"
          >
            {{ text }}
          </div>
        </div>
      </template>
      <template v-else-if="column.dataIndex === 'code'">
        <div class="blue hover" @click="onClickCode(record)">{{ text }}</div>
      </template>
      <template v-else-if="column.dataIndex === 'operation'">
        <slot :record="record"></slot>
      </template>
    </template>
  </a-table>
</template>
<script setup>
import { useStore } from "vuex"
import { editZcwStocks } from "@/api"
import { computed, ref, watch, onMounted, reactive, nextTick } from "vue"
import { round, cloneDeep, isEqual } from "lodash-es"
import { message } from "ant-design-vue"
const store = useStore()
const state = reactive({
  dataIndex: ""
})

const tabHeight = computed(() => store.getters.tabHeight)
const props = defineProps({
  columns: {
    type: Array,
    default: () => []
  },
  stocksList: {
    type: Array,
    default: () => []
  },
  tabHeight: {
    type: String,
    default: ""
  }
})

// 创建一个对象来存储每个item对应的DOM元素引用，后续可以通过itemRefs.value[itemId]来访问特定item对应的DOM元素
const itemRefs = ref({})
function registerRef(element, code, dataIndex) {
  if (element) {
    itemRefs.value[code + dataIndex] = element
  }
}

const editableData = reactive({})
const onClickCode = (record)=>{
  const {code,house} = record
  // window.open(`https://xueqiu.com/S/${house}${code}`)
  window.open(`https://www.iwencai.com/unifiedwap/result?w=${code}%20&querytype=stock`)
}

// 编辑
const onEditClick = (code, dataIndex) => {
  editableData[code] = cloneDeep(props.stocksList.filter((item) => code === item.code)[0])
  state.dataIndex = dataIndex
  nextTick(() => {
    itemRefs.value[code + dataIndex].focus()
  })
}

// 保存
const onSaveStock = async (code) => {
  const stockItem = props.stocksList.filter((item) => code === item.code)[0]
  const type = isEqual(stockItem, editableData[code])
  if (!type) {
    const params = {
      list: [editableData[code]]
    }
    const { errcode, data } = await editZcwStocks(params)
    if (errcode == 0) {
      Object.assign(stockItem, editableData[code])
      message.success("编辑成功")
    }
  }
  state.dataIndex = ""
  delete editableData[code]
}

</script>
<style lang="less" scoped>
.hover{
  cursor: pointer;
}
</style>