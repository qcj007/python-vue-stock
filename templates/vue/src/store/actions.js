import { cloneDeep, isEqual, round, merge } from "lodash-es"
import { message } from "ant-design-vue"

import {searchStockInfo} from "@/api"
import { throttle } from "lodash-es"
export default {
  // 改变右侧tab
  getYMDate({ commit, state, dispatch }, type = "") {
    const currentDate = new Date()
    return `${currentDate.getFullYear()}-${currentDate.getMonth() + 1}-${currentDate.getDate()}`
  },
  onSearchStockInfo({ commit, state, dispatch }, code) {
    return new Promise(async (resolve, reject) => {
      const params = { code }
      const { errcode, data } = await searchStockInfo(params)
      if (errcode == 0) {
        resolve(data)
      }else{
        resolve({})
      }
    })
    
  },
  
}
