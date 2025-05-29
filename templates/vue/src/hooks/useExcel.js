import { saveAs } from "file-saver"
import { utils, writeFile } from "xlsx"
export default () => {
  // 导出
  const exportEecel = (data, columns, fileName) => {
    let columnsObj = {}
    columns.forEach((item) => {
      const { dataIndex, title } = item
      columnsObj[dataIndex] = title
    })
  
    const list = data.map((item) => {
      const obj = {}
      for(let key in item){
        obj[columnsObj[key]] = item[key]
      }
      return obj
    })

    const worksheet = utils.json_to_sheet(list)
    const workbook = utils.book_new()
    utils.book_append_sheet(workbook, worksheet, "Sheet1")
    writeFile(workbook, `${fileName}.xlsx`)
  }
  return {
    exportEecel
  }
}
