import VueRouter from 'vue-router'
import Vue from 'vue'
import { fetchGet } from '@/api/http'
import Main from '@/pages/PC_index/home/main.vue'
import Booklist from '@/pages/PC_index/home/children/bookList.vue'
const Bookdetail = () => import('@/pages/PC_index/bookdetail/bookdetail.vue')
const Login = () => import('@/pages/PC_index/login/LoginIndex.vue')
const Booksearchs = () =>
  import('@/pages/PC_index/booksearchmain/booksearchs.vue')
const Bookhouse = () => import('@/pages/PC_index/bookhouse/bookhouse.vue')
const Bookrank = () => import('@/pages/PC_index/bookrank/bookrank.vue')
const Forgetpwd = () => import('@/pages/PC_index/forget/forgetpwd.vue')
const Userindex = () => import('@/pages/PC_index/user/userindex.vue')
const Mmain = () => import('@/pages/M_index/Mobelmain.vue')
const Bookchapter = () => import('@/pages/PC_index/bookdetail/children/bookchapter.vue')

Vue.use(VueRouter)
// 避免重复导航到当前路径
const originalPush = VueRouter.prototype.push
VueRouter.prototype.push = function push(location) {
  return originalPush.call(this, location).catch((err) => err)
}

const router = new VueRouter({
  mode: 'history',
  routes: [
    {
      path: '/',
      component: Main,
      meta: {
        title: '阅读书城'
      },
      children: [
        {
          path: '',
          component: Booklist,
          name: 'Main'
        },
      ]
    },
    {
      path: '/login',
      component: Login,
      meta: {
        title: '登录页'
      }
    },
    {
      path: '/forgetpwd',
      component: Forgetpwd
    },
    {
      path: '/main',
      component: Main,
      meta: {
        title: '阅读书城'
      },
      children: [
        {
          path: 'bookhouse',
          name: 'Bookhouse',
          component: Bookhouse
        },
        {
          path: 'bookrank',
          name: 'Bookrank',
          component: Bookrank
        },
        {
          path: 'userindex',
          component: Userindex,
          name: 'Userindex',
          meta: {
            title: '用户首页',
            requireauth: true
          }
        },
        {
          path: 'bookdetail',
          name: 'Bookdetail',
          component: Bookdetail,
          children: [
            {
              path: 'bookchapter',
              name: 'Bookchapter',
              component: Bookchapter
            }
          ]
        },
        {
          path: 'booksearchs',
          name: 'Booksearch',
          component: Booksearchs
        },

      ]
    },

    {
      path: '/Mmain',
      component: Mmain
    }
  ]
})

router.beforeEach(async function (to, from, next) {
  window.document.title =
    to.meta.title === undefined ? '阅读书城' : to.meta.title
  if (to.path == '/' && from.path == '/') {
    let uautolg = localStorage.getItem('expirelog')
    if (uautolg == '1' && window.name === '') {
      window.name = 'reload'
      const utoken = localStorage.getItem('ulog')
      await fetchGet('/login', { token: utoken }).then((res) => {
        if (!res.data.status) {
          localStorage.removeItem('ulog')
        } else {
          localStorage.setItem('currentuser', JSON.stringify({ username: res.data.username, userid: res.data.userid, login: true }))
        }
      })
    } else if (!uautolg && window.name === '') {
      localStorage.clear()
    }
    next()
  } else if (to.name === 'login' && from.query.returnUrl) {
    // 在登录页面，且传入了 returnURL 参数，保存 returnURL 到路由元信息中
    to.meta.returnUrl = from.query.returnUrl;
  }
  next()
})

export default router
