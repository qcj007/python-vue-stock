/**
 * 数据库类型对象转驼峰型对象
 * @param obj 数据库类型对象
 * @param item 驼峰类型对象
 * @param type 转换类型（参数存在代表驼峰转成字段）
 * @param transStr 是否将value转换为字符串，默认为true
 * @return
 */
export function covertObj (obj, item, type = false, transStr = true) {
  let newObj = {}
  for (let key in obj) {
    let fieldName = columnName2FieldName(key)
    if (type) {
      fieldName = fieldName2ColumnName(key)
    }

    let val = (obj[key] !== undefined && obj[key] !== null) ? obj[key] : ''
    if (!transStr && val !== null && typeof val === 'object') {
      if (Array.isArray(val)) {
        val = val.map(v => {
          if(typeof v !== "object") return v;
          let tempObj = {}
          covertObj(v, tempObj, type, transStr)
          return tempObj
        })
      } else {
        let tempObj = {}
        covertObj(val, tempObj, type, transStr)
        val = tempObj
      }
    }
    newObj[fieldName] = transStr ? val + '' : val
  }
  Object.assign(item, newObj)
}


/**
 * 数据库列名转属性(下划线转驼峰)
 * @param columnName 数据库列名
 * @return
 */
function columnName2FieldName (columnName) {
  let result = ''
  let upcaseFlag = false
  if (!columnName || columnName === '') return columnName
  for (let i = 0; i < columnName.length; i++) {
    let ch = columnName[i]
    if (ch === '_') {
      upcaseFlag = true
      continue
    } else if (upcaseFlag) {
      result += ('' + ch).toUpperCase()
      upcaseFlag = false
    } else {
      result += ch
      upcaseFlag = false
    }
  }
  return result
}
/**
 * 属性转数据库列名(驼峰传下划线)
 * @param str 属性名
 * @return
 */
function fieldName2ColumnName (columnName) {
  let result = ''
  var upcaseFlag = false
  if (!columnName || columnName == '') return columnName
  for (var i = 0; i < columnName.length; i++) {
    var ch = columnName[i]
    if (allCaps(ch)) {
      result += ('_' + ch).toLowerCase()
    } else {
      result += ch
    }
  }
  return result
}
function allCaps (text) {
  if (text < 'A' || text > 'Z') {
    return false
  }
  return true
}