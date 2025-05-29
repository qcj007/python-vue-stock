/* 引入资源请求插件 */
import { message } from "ant-design-vue"
import axios from "axios"
import { covertObj } from "@/plugins/utils/coverObj.js"
axios.defaults.baseURL = window.LOCAL_CONFIG.BASE_HOME //设置接口网关地址
axios.defaults.withCredentials = true //前端跨域设置，携带cookie
axios.defaults.timeout = 10000

axios.interceptors.request.use(
  function (config) {
    return config
  },
  function (error) {
    // Do something with request error
    return Promise.reject(error)
  }
)

// Add a response interceptor
axios.interceptors.response.use(
  function (response) {
    let data = {}
    covertObj(response.data, data, false, false)
    // Do something with response data
    const { errcode, errmsg } = data
    if (errcode != 0) {
      message.error(errmsg || "系统错误")
    }
    return data
  },
  function (error) {
    // Do something with response error
    return Promise.reject(error)
  }
)

export default (url, params = {}, type = "POST") => {
  let data = {}
  covertObj(params, data, true, false)

  if (type === "GET") {
    return axios.get(url, {
      params: data
    })
  } else {
    return axios.post(url, data)
  }
}
