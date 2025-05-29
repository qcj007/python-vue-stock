import { round } from "lodash-es"

// 20010101 转化成2001-01-01
export const convertDateFormat = (dateStr) => {
  if (!dateStr) return ""
  // 将字符串分割成数组
  let dateParts = (dateStr + "").split("")
  // 按照年月日重新组合，并在相应位置插入破折号
  const formattedDate =
    dateParts.slice(0, 4).join("") +
    "-" +
    dateParts.slice(4, 6).join("") +
    "-" +
    dateParts.slice(6, 8).join("")

  return formattedDate
}
// 根据股票代码获取股票所属市场
export const getStockHouse = (code = "") => {
  if (code.length != 6) {
    return ""
  }
  const codeStart = code.split("")[0]
  return codeStart == "6" ? "SH" : codeStart == "3" || codeStart == "0" ? "SZ" : "BJ"
}

// 计算赔率
export const calcOddsRate = (price, buyPrice, stopSurplus, offset) => {
  const buyRate = round(((price - buyPrice) / price) * 100, 2)
  const oddsPrice = (stopSurplus - buyPrice) * offset + buyPrice * 1
  const oddsRate = round(((oddsPrice - price) / price) * 100 - buyRate, 2)
  return { oddsRate, buyRate }
}

// 表格列
export  const columnsItem = (title, key, customCell = () => {}) => {
  return {
    title,
    dataIndex: key,
    customCell: (record) => customCell(record),
    sorter: {
      compare: (a, b) => a[key] - b[key]
    }
  }
}
