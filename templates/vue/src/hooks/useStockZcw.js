// 获取字典
import { useStore } from "vuex"
import { computed, ref, watch, onMounted, reactive } from "vue"
import { round, cloneDeep } from "lodash-es"
import {
  searchZcwStocks,
  searchZcwStockInfo,
  searchStockInfo,
  addZcwStocks,
  editZcwStocks
} from "@/api"
import { convertDateFormat, getStockHouse, calcOddsRate, columnsItem } from "@/plugins/utils/index"
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

    {
      ...columnsItem("市盈率", "syl", (record) => {
        const syl = record.syl
        const className = syl < 0 ? "green" : ""
        return {
          innerHTML: `<span class="${className}">${syl}</span>`
        }
      })
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

  const zcwlist = ref([])
  const searchList = ref([])

  // 查询股票列表
  const searchStockList = async (list = "null") => {
    store.commit("setData", { codeList: list })
    const params = {
      codeList: list
    }
    searchList.value = list || []
    const { errcode, data } = await searchZcwStocks(params)
    if (errcode == 0) {
      data.reverse()
      if (!list || JSON.stringify(list) == JSON.stringify(searchList.value)) {
        if (list && list != "null" && list.length > 0) {
          zcwlist.value = list.map((item) => {
            return data.find((zcwItem) => item == zcwItem.code)
          })
        } else {
          zcwlist.value = data
        }
      }
    }
  }

  const stocksList = computed(() => {
    return cloneDeep(zcwlist.value).map((item) => {
      const { code, name, price, buyPrice, stopSurplus, stopLoss } = item
      const { buyRate, oddsRate } = calcOddsRate(price, buyPrice, stopSurplus, store.getters.offset)
      // # 计算赔率
      item.buyRate = buyRate
      item.oddsRate = oddsRate
      return item
    })
  })

  // 股票代码修改
  const onCodeChange = async (addForm) => {
    const { code } = addForm

    if (code.length != 6) {
      addForm.name = ""
      addForm.isExist = ""
      addForm.industry = ""
      addForm.buyPrice = ""
      addForm.stopSurplus = ""
      addForm.stopLoss = ""
    } else {
      addForm.house = getStockHouse(code)
      onSearchStockInfo(code, addForm)
      const { errcode, data } = await searchZcwStockInfo({ code_list: [code] })
      if (errcode == 0 && data.length > 0) {
        addForm.isExist = true
        const { buyPrice, stopSurplus, stopLoss } = data[0]
        addForm.buyPrice = buyPrice
        addForm.stopSurplus = stopSurplus
        addForm.stopLoss = stopLoss
      } else {
        addForm.isExist = false
        addForm.buyPrice = ""
        addForm.stopSurplus = ""
        addForm.stopLoss = ""
      }
    }
  }
  // 查询股票信息
  const onSearchStockInfo = async (code, addForm) => {
    const params = { code }
    const { errcode, data } = await searchStockInfo(params)
    if (errcode == 0) {
      addForm.name = data["股票简称"]
      addForm.industry = `（${data["行业"]}）`
    }
  }

  // 新增支撑位股票
  const onAddZcwStock = async (addForm) => {
    try {
      if (addForm.code.length != 6) {
        message.warn("请输入正确的股票代码")
        return
      }
      const params = {
        stock: addForm
      }
      const { errcode, data } = await addZcwStocks(params)
      if (errcode == 0) {
        return true
      } else {
        throw new Error("新增失败")
      }
    } catch (err) {
      return false
    }
  }

  // 修改股票买卖价格
  const onEditStock = async (item) => {
    try {
      const params = {
        list: [item]
      }
      const { errcode, data } = await editZcwStocks(params)
      if (errcode == 0) {
        return true
      } else {
        throw new Error("修改失败")
      }
    } catch (err) {
      return false
    }
  }

  // 根据买入价调整止损位
  const onBuyPriceBlur = (addForm) => {
    addForm.stopLoss = round(addForm.buyPrice * 0.95, 2)
  }

  return {
    columns,
    zcwlist,
    searchStockList,
    stocksList,
    onCodeChange,
    onAddZcwStock,
    onBuyPriceBlur,
    onEditStock
  }
}
