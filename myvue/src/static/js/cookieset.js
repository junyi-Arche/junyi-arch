/**
 *
 * @param {string} type 设置cookie值的name
 * @param {string} data cookie值的内容
 */
export function setCookies(type, data, ...args) {
  const date = new Date()
  date.setTime(date.getTime() + 1 * 60 * 1000)
  const expires = 'expires=' + date.toUTCString()
  document.cookie = `${type}=${data}; ${expires}; path=/`
}
/**
 * @param {string} type 获取cookie值的name
 * @param {func} callback
 */
export function getCookies(type, callback) {
  const data = document.cookie.match(type)
  callback && callback(data)
}

export function getlocalStorage(name, callback) {
  const data = localStorage.getItem(name)
  callback && callback(data)
}
// if (this.$store.state.userinfo.username) {
//   const date = new Date()
//   date.setTime(date.getTime() + 24 * 60 * 60 * 1000)
//   const expires = 'expires=' + date.toUTCString()
//   document.cookie = `user=${this.$store.state.userinfo.username}/${this.$store.state.userinfo.userid}; ${expires}; path=/`
// }

// // 匹配到没有用户清除sessionstorage
// if (document.cookie.match('user') === null) {
//   sessionStorage.removeItem('store')
// } else {
//   const user = document.cookie.match('user').input.split('=')[1]
//   this.updateState({
//     username: user.split('/')[0],
//     userid: user.split('/')[1]
//   })
// }
