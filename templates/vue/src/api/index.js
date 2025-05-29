import Axios from "./axios"

// 查询单个股票信息
export const searchStockInfo = (data) => Axios("/searchStockInfo", data, "POST")

// -----------支撑位价值投资股票---------------
// 股票列表
export const searchZcwStocks = (data) => Axios("/searchZcwStocks", data, "POST")
// 编辑股票
export const editZcwStocks = (data) => Axios("/editZcwStocks", data, "POST")
// 删除股票
export const deleteZcwStocks = (data) => Axios("/deleteZcwStocks", data, "POST")
// 添加股票
export const addZcwStocks = (data) => Axios("/addZcwStocks", data, "POST")
// 查询单个股票信息
export const searchZcwStockInfo = (data) => Axios("/searchZcwStockInfo", data, "POST")

// --------------------股票事件列表-----------------
// 股票列表
export const searchStocksEvents = (data) => Axios("/searchStocksEvents", data, "POST")
// 编辑股票
export const editStocksEvents = (data) => Axios("/editStocksEvents", data, "POST")
// 删除股票
export const deleteStocksEvents = (data) => Axios("/deleteStocksEvents", data, "POST")
// 添加股票
export const addStocksEvents = (data) => Axios("/addStocksEvents", data, "POST")

// 行业概念
// 行业概念列表
export const searchStocksConcepts = (data) => Axios("/searchStocksConcepts", data, "POST")
// 编辑行业概念
export const editStocksConcepts = (data) => Axios("/editStocksConcepts", data, "POST")
// 删除行业概念
export const deleteStocksConcepts = (data) => Axios("/deleteStocksConcepts", data, "POST")
// 添加行业概念
export const addStocksConcepts = (data) => Axios("/addStocksConcepts", data, "POST")

// 股票机会
// 股票机会列表
export const searchStockOpportunity = (data) => Axios("/searchStockOpportunity", data, "POST")
// 编辑股票机会
export const addStockOpportunity = (data) => Axios("/addStockOpportunity", data, "POST")
// 删除股票机会
export const deleteStockOpportunity = (data) => Axios("/deleteStockOpportunity", data, "POST")
// 添加股票机会
export const editStockOpportunity = (data) => Axios("/editStockOpportunity", data, "POST")

// 周期股票
// 查询周期股票
export const searchStockCycle = (data) => Axios("/searchStockCycle", data, "POST")
// 添加周期股票
export const addStockCycle = (data) => Axios("/addStockCycle", data, "POST")
// 删除周期股票
export const deleteStockCycle = (data) => Axios("/deleteStockCycle", data, "POST")

// 我关心的股票
// 股票我关心的股票
export const searchStockMyCare = (data) => Axios("/searchStockMyCare", data, "POST")
// 添加我关心的股票
export const addStockMyCare = (data) => Axios("/addStockMyCare", data, "POST")
// 删除我关心的股票
export const deleteStockMyCare = (data) => Axios("/deleteStockMyCare", data, "POST")
