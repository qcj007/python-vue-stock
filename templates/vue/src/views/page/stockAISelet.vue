<template>
  <div class="minions-content">
    <div class="minions-head">
      <div></div>
    </div>
    <div class="minions-body">
      <zcw-table :columns="state.columns" :stocksList="state.stocksList"></zcw-table>
    </div>
  </div>
</template>
<!-- https://www.iwencai.com/unifiedwap/result?w=430476.BJ%20&querytype=stock -->
<script setup>
import { useStore } from "vuex"
import { deleteZcwStocks, addZcwStocks } from "@/api"
import { computed, ref, watch, onMounted, reactive, nextTick } from "vue"
import { round, cloneDeep, isEqual } from "lodash-es"
import useStockZcw from "@/hooks/useStockZcw"
import useExcel from "@/hooks/useExcel"
import { message } from "ant-design-vue"
import zcwTable from "@/components/zcw-table.vue"
import { data } from "./JSON/data.js"
import { convertDateFormat, getStockHouse, calcOddsRate, columnsItem } from "@/plugins/utils/index"
const state = reactive({
  columns: [
    {
      title: "序号",
      dataIndex: "index", // 注意这里不是实际的数据字段名，因为序号是虚拟的
      key: "index", // 需要指定一个唯一的key值，通常用'index'或'serialNumber'
      width: 60,
      align: "center",
      customRender: ({ text, record, index }) => `${index + 1}`
    },
    { title: "股票代码", dataIndex: "code" },
    { title: "股票简称", dataIndex: "股票简称" },
    { title: "总市值[20250314]", dataIndex: "总市值" },
    {
      ...columnsItem("涨跌幅", "涨跌幅:前复权", (record) => {
        const rate = record["涨跌幅:前复权"] * 1
        const className = rate < 0 ? "green" : "red"
        return {
          innerHTML: `<span class="${className}">${rate}%</span>`
        }
      })
    },
    {
      ...columnsItem("换手率", "换手率", (record) => {
        return {
          innerHTML: `<span class="blue">${record["换手率"]}%</span>`
        }
      })
    },
    { title: "量比[20250314]", dataIndex: "量比1" },
    { title: "量比[20250313]", dataIndex: "量比2" },
    { title: "量比[20250312]", dataIndex: "量比3" },
    { title: "量比[20250311]", dataIndex: "量比4" },
    { title: "量比[20250310]", dataIndex: "量比5" }
  ],
  stocksList: []
})

// # 当日涨跌幅，近5天每天量比，当天量比大于2， 涨跌幅-1%~4%，换手率小于15%大于4%，企业市值小于80亿
// # 筛选出：
// # 1.当日换手率大于4,且小于12
// # 2.量比： ①当天量比大于3，前一天量比大于2      ②当天量比大于2，前面四天量比小于1.2
// # 交易当天交易方法：
// # 1.开盘买：买入价格设置日线支撑位，可以高一两分
// # 2.尾盘买：看放量是否比前一天高或者齐平

onMounted(() => {
  const { answer } = data.data

  if (answer.length > 0) {
    const { columns, datas } = answer[0].txt[0].content.components[0].data
    let columnsKey = [
      {
        label: "code",
        name: "股票代码"
      }
    ]
    const keyList = ["股票简称", "总市值", "换手率", "涨跌幅:前复权", "量比"]
    let lbIndex = 1
    columns.forEach((item) => {
      let { key, index_name, timestamp } = item

      if (keyList.includes(index_name)) {
        if (index_name === "量比") {
          index_name = "量比" + lbIndex
          lbIndex++
        }

        columnsKey.push({
          label: index_name,
          name: key
        })
      }
    })
    console.log("columnsKey", columnsKey)
    state.columns = state.columns.map((item) => {
      if (item.dataIndex.includes("量比")) {
        const child = columnsKey.find((keyItem) => keyItem.label === item.dataIndex)
        item.title = child.name
      }

      return item
    })

    console.log("state.columns", JSON.stringify(state.columns))
    state.stocksList = datas
      .map((item) => {
        const child = {}
        columnsKey.forEach((columnsItem) => {
          if (columnsItem.label === "总市值") {
            child[columnsItem.label] = round((item[columnsItem.name] * 1) / 100000000, 2) + "亿元"
          } else if (columnsItem.label === "股票简称" || columnsItem.label === "code") {
            child[columnsItem.label] = item[columnsItem.name]
          } else {
            child[columnsItem.label] = round(item[columnsItem.name] * 1, 2)
          }
        })
        return child
      })
      .filter((item) => {
        if (item["换手率"] * 1 > 4 && item["换手率"] * 1 < 12) {
          if (
            (item["量比1"] * 1 > 3 && item["量比2"] * 1 > 2) ||
            (item["量比1"] * 1 > 2 &&
              item["量比2"] * 1 < 1.2 &&
              item["量比3"] * 1 < 1.2 &&
              item["量比4"] * 1 < 1.2 &&
              item["量比5"] * 1 < 1.2)
          ) {
            return item
          }
        }
      })
  }
})

// 市值小于100亿，70%成本下限比现价高，集中度小于3，换手率小于15%大于5%，近5日量比
// 市值小于100亿，70%成本上限比现价低，换手率，近5日量比
// 集中度70=(70%成本的最高价-70%成本的最低价)/(70%成本的最高价+70%成本的最低价)*100%，集中度70的值越小，说明成本越集中。反之，则成本越分散。


// 1.当日涨跌幅，近5天每天量比，当天量比大于2， 涨跌幅-1%~4%，换手率小于15%大于4%，企业市值小于80亿
// 2.市值小于100亿，70%成本下限比现价高，集中度小于3，换手率小于15%大于5%，近5日量比
// 3.当日涨跌幅，近5天每天量比，当天量比大于2， 涨跌幅-1%~4%，换手率小于15%大于3%，企业市值小于100亿，筹码集中度小于5
// 4.当日涨跌幅，近5天每天量比，当天量比大于2， 企业市值小于100亿，筹码集中度小于5


</script>


