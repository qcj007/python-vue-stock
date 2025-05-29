import { round, cloneDeep } from "lodash-es"

export default {
  // 获取当前年月日
  getYMDate(state) {
    const currentDate = new Date()
    const year = currentDate.getFullYear()
    let month = currentDate.getMonth() + 1
    month = month < 10 ? `0${month}` : month
    let date = currentDate.getDate()
    date = date < 10 ? `0${date}` : date
    return `${year}-${month}-${date}`
  },
  tabHeight(state) {
    return `${state.contHeight - 175}px`
  },
  offset(){
    const dapan = 3050
    return 0.9 + ((dapan -3000) / 100) * 0.1
  }
}
