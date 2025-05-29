// 获取字典
import { useStore } from "vuex"
import { computed, ref, watch, onMounted, reactive } from "vue"
import { round, cloneDeep } from "lodash-es"
import { searchStocksEvents } from "@/api"
import { convertDateFormat, getStockHouse, calcOddsRate,columnsItem } from "@/plugins/utils/index"
export default () => {
  const store = useStore()

  const columns = [
    {
      title: "序号",
      dataIndex: "index", // 注意这里不是实际的数据字段名，因为序号是虚拟的
      key: "index", // 需要指定一个唯一的key值，通常用'index'或'serialNumber'
      width: 60,
      align: "center",
      customRender: ({ text, record, index }) => `${index + 1}`
    },
    {
      title: "股票代码",
      dataIndex: "code"
    },
    {
      title: "股票名称",
      dataIndex: "name"
    },
    {
      title: "现价(元)",
      dataIndex: "price"
    },
    {
      ...columnsItem("涨跌幅", "zdf", (record) => {
        const rate = record.zdf * 1
        const className = rate < 0 ? "green" : "red"
        return {
          innerHTML: `<span class="${className}">${rate}%</span>`
        }
      })
    },
    {
      ...columnsItem("换手率", "hsl", (record) => {
        return {
          innerHTML: `<span class="blue">${record.hsl}%</span>`
        }
      })
    },
    {
      ...columnsItem("量比", "lb")
    },
    
    {
      ...columnsItem("赔率", "oddsRate", (record) => {
        const rate = record.oddsRate * 1
        const className = rate < 0 ? "green" : "red"
        return {
          innerHTML: `<span class="${className}">${rate}%</span>`
        }
      })
    },
    {
      title: "买入价(元)",
      dataIndex: "buyPrice"
    },
    {
      ...columnsItem("距离买入价", "buyRate", (record) => {
        const rate = record.buyRate
        const className = rate < 5 ? "red" : rate < 10 ? "blue" : ""
        return {
          innerHTML: `<span class="${className}">${rate}%</span>`
        }
      })
    },

    {
      title: "止盈(元)",
      dataIndex: "stopSurplus"
    },
    {
      title: "止损(元)",
      dataIndex: "stopLoss"
    },
    
    { title: "事件备注", dataIndex: "eventRemark" },
    { title: "事件时间", dataIndex: "eventTime" },
    { title: "股票开始时间", dataIndex: "startTime" },
    { title: "股票结束时间", dataIndex: "endTime" },
    {
      ...columnsItem("距离开始时间", "distanceStartTime", (record) => {
        const { distanceStartTime, distanceEndTime } = record
        let dtText = `${distanceStartTime}天`
        let className = ""
        if (distanceStartTime <= 0 && distanceEndTime > 0) {
          dtText = "已开始"
          className = "red"
        } else if (distanceEndTime <= 0) {
          dtText = "已结束"
          className = "green"
        }
        return {
          innerHTML: `<span class="${className}">${dtText}</span>`
        }
      })
    },
    {
      ...columnsItem("距离结束时间", "distanceEndTime", (record) => {
        const { distanceStartTime, distanceEndTime } = record
        let dtText = `${distanceEndTime}天`
        let className = ""
        if (distanceStartTime <= 0 && distanceEndTime > 0) {
          className = "blue"
        } else if (distanceEndTime <= 0) {
          dtText = "已结束"
          className = "green"
        }
        return {
          innerHTML: `<span class="${className}">${dtText}</span>`
        }
      })
    },

    {
      ...columnsItem("市盈率", "syl")
    },
    {
      ...columnsItem("市净率", "sjl")
    },
    {
      ...columnsItem("流通市值", "ltsz", (record) => {
        return {
          innerHTML: `${record.ltsz}亿`
        }
      })
    },
    {
      ...columnsItem("总市值", "zsz", (record) => {
        return {
          innerHTML: `${record.zsz}亿`
        }
      })
    },

    {
      title: "操作",
      dataIndex: "operation"
    }
  ]
  const state = reactive({
    dataIndex: "",
    list: []
  })
  // 查询股票列表
  const searchStockList = async () => {
    state.list = []
    const { errcode, data } = await searchStocksEvents({})
    if (errcode == 0) {
      data.reverse()
      state.list = data
      console.log(state.list)
    }
  }

  const nowTime = new Date().getTime()

  const stocksList = computed(() => {
    return cloneDeep(state.list).map((item) => {
      const { price, buyPrice, stopSurplus, startTime, eventTime, endTime } = item
      const { buyRate, oddsRate } = calcOddsRate(
        price,
        buyPrice,
        stopSurplus,
        store.getters.offset
      )
      // # 计算赔率
      item.buyRate = buyRate
      item.oddsRate = oddsRate
      
      item.distanceStartTime = Math.ceil(
        (new Date(startTime).getTime() - nowTime) / 1000 / 60 / 60 / 24
      )
      item.distanceEndTime = Math.ceil(
        (new Date(endTime).getTime() - nowTime) / 1000 / 60 / 60 / 24
      )

      return item
    })
  })
  watch(
    () => stocksList.value,
    () => {
      console.log(stocksList.value)
    },
    { deep: true }
  )

  onMounted(() => {
    searchStockList()
  })

  return {
    columns,
    state,
    searchStockList,
    stocksList
  }
}
