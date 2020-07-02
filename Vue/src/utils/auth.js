import Cookies from 'js-cookie'

const TokenKey = 'vue_admin_template_token'

export function getToken() {

  // console.log(Cookies)
  return Cookies.get(TokenKey)
}

export function setToken(token) {
  // console.log("set  cookie")
  return Cookies.set(TokenKey, token)
}

export function removeToken() {
  return Cookies.remove(TokenKey)
}

let getCookie = function (cookie) {
  let reg = /csrftoken=([\w]+)[;]?/g
  return reg.exec(cookie)[1]

}