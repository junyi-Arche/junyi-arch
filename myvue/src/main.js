import Vue from 'vue'
import VueCookies from 'vue-cookies';
import App from './App.vue'
// import 'vant/lib/index.less'
import router from '@/router'
import store from '@/store/index.js'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
// 设置body高度与浏览器高度一致
import '@/static/css/all.css'
import c from '@/static/js/crypto.js'
Vue.use(VueCookies)
Vue.use(ElementUI)
Vue.config.productionTip = false

Vue.prototype.slicestr = function (str, num) {
  if (str.length > num) {
    return str.slice(0, num - 1) + '...'
  } else {
    return str
  }
}
Vue.prototype.crypt = c
new Vue({
  store,
  render: (h) => h(App),
  router
}).$mount('#app')
