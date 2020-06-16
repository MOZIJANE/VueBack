/**
 * Created by PanJiaChen on 16/11/18.
 */

/**
 * @param {string} path
 * @returns {Boolean}
 */
export function isExternal(path) {
  return /^(https?:|mailto:|tel:)/.test(path)
}

/**
 * @param {string} str
 * @returns {Boolean}
 */
export function validUsername(str) {
  const valid_map = ['admin', 'editor']
  return valid_map.indexOf(str.trim()) >= 0
}

export function timeFormat(str = '') {
  var dt = str ? new Date(str) : new Date()
  // console.log(dt)
  var y = dt.getFullYear()
  var m = (dt.getMonth() + 1).toString().padStart(2, '0')
  var d = dt.getDate().toString().padStart(2, '0')
  var hh = dt.getHours().toString().padStart(2, '0')
  var mm = dt.getMinutes().toString().padStart(2, '0')
  var ss = dt.getSeconds().toString().padStart(2, '0')
  return `${y}-${m}-${d}-${hh}-${mm}-${ss}`
}

// 传入的值为分钟
export function timeComputed(int) {
  var stamptime = new Date().getTime() - (int * 60 * 1000)
  var edate = timeFormat()
  var sdate = timeFormat(stamptime)
  return [sdate, edate]
}
