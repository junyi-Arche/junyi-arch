<template>
  <div class="outbox">
    <div class="header">
      <ul ref="topbar" class="topbar">
        <li @click="changebar($event, 1)">
          <router-link to="/">首页</router-link>
        </li>
        <li @click="changebar($event, 3)">
          <router-link to="/main/bookrank">排行</router-link>
        </li>
        <li @click="changebar($event, 5)">
          <router-link to="/main/bookhouse">分类</router-link>
        </li>
      </ul>
      <div class="explore">
        <el-autocomplete class="main-input" name="search" v-model="searchname" :trigger-on-focus="false"
          :fetch-suggestions="querySearchAsync" placeholder="请输入搜索内容"></el-autocomplete>
        <div class="searchicon" @click="startsearch()"><i class="el-icon-search"></i></div>
      </div>
      <div class="userlog">
        <router-link v-if="this.$store.state.userinfo.username"
          :to="{ path: '/main/userindex', query: { userid: this.$store.state.userinfo.userid } }">
          <span class="usersign" data-text="个人中心">个人中心</span>
        </router-link>
        <router-link v-else :to="{ path: '/login', query: { returnUrl: this.$route.fullPath } }">
          <span class="usersign" data-text="登录">登录</span>
        </router-link>
        <div v-if="$store.state.userinfo.username" @mouseleave="() => (showusermeun = false)" class="u-menu">
          <router-link :to="{ path: '/main/userindex', query: { userid: this.$store.state.userinfo.userid } }">
            <span>{{
            this.$store.state.userinfo.username
          }}</span>
          </router-link>
          
          <span><a @click="switchUser()" href="javascript:;">切换用户</a></span>
          <span><a @click="logout()" href="javascript:;">退出登录</a></span>

        </div>
      </div>
    </div>
    <keep-alive include="BookList,Bookrank">
      <router-view></router-view>
    </keep-alive>
    <div id="tohead" @click="totop">
      <i class="el-icon-caret-top"></i>
    </div>
  </div>
</template>

<script>
import { fetchGet, fetchPost, status } from '@/api/http'
import { mapActions } from 'vuex'
import { getlocalStorage } from '@/static/js/cookieset'
import { listenMsg, sendMsg } from '@/static/js/crossTagMsg.js'
export default {
  name: 'Main',
  data() {
    return {
      searchbookdata: [],
      searchname: '',
      searchTimer: '',
      topbar: 0,
      showusermeun: false
    }
  },
  watch: {
    searchname(newval, _oldval) {
      this.searchname = newval
      if (this.searchname === '') {
        this.searchbookdata = []
      }
    }
  },
  created() {
    window.addEventListener('scroll', this.showToHead)
    listenMsg(msg => {
      if (msg.data.type === 'userlogin') {
        this.autoUpdateuser()
        sendMsg('response', 'successlogin')
      } else if (msg.data.type === 'userlogout') {
        location.replace(document.referrer)
        sendMsg('response', 'successlogout')
      }
    })
  },
  destroyed() {
    window.removeEventListener('scroll', this.showToHead)
    window.removeEventListener('message', listenMsg, true)
    window.removeEventListener('message', sendMsg, true)
  },
  mounted() {
    this.remainTopbarstyle()
    this.autoUpdateuser()
  },
  updated() {
    this.remainTopbarstyle()
  },
  methods: {
    ...mapActions(['deleteState', 'updateState',]),
    autoUpdateuser() {
      getlocalStorage('currentuser', (user) => {
        if (user) {
          const udata = JSON.parse(user)
          this.$store.dispatch('updateState', {
            username: udata.username,
            userid: udata.userid
          })
        }
      })
    },
    startsearch() {
      if (this.searchname === '' || !status) {
        return null
      } else {
        this.$router.push({
          path: '/main/booksearchs',
          query: { bn: this.searchname }
        })
      }
    },
    querySearchAsync(queryString, cb) {
      if (this.searchname === '') {
        clearTimeout(this.searchTimer)
      } else {
        if (this.searchTimer) {
          clearTimeout(this.searchTimer)
        }
        this.searchTimer = setTimeout(async () => {
          await fetchGet('/searchbook', {
            bn: this.searchname,
            limit: ''
          }).then(res => {
            this.searchbookdata = res.data.searchbooks
          }).catch(err => {
            this.$message({
              type: 'error',
              message: "服务器连接失败，请检查网络"
            })

          })
          cb(this.searchbookdata)
        }, 1800)
      }
    },
    changebar(e, i) {
      if (e.target.childElementCount === 0) {
        const ulel = e.target.parentNode.parentNode
        const lis = ulel.childNodes
        for (var j = 0; j < lis.length; j++) {
          lis[j].className = ''
        }
        this.topbar = (i - 1) / 2
        this.$refs.topbar.classList.remove('hide-after')
        e.target.parentNode.className = 'checked'
        ulel.style.setProperty('--i', i)
      }
    },
    showToHead() {
      const Tohead = document.querySelector('#tohead')
      if (document.documentElement.scrollTop >= 500) {
        Tohead.style.display = 'inline'
      } else {
        Tohead.style.display = 'none'
      }
    },
    totop() {
      var currentPosition = window.pageYOffset
      var scrollSpeed = -currentPosition * 0.1
      var scrollInterval = setInterval(function () {
        window.scrollBy({ top: scrollSpeed, left: 0 })
        if (window.pageYOffset === 0) {
          clearInterval(scrollInterval)
        }
      }, 20)
    },
    async logout() {
      localStorage.removeItem('ulog')
      await fetchPost('/logout', { 'usernum': this.$store.state.userinfo.userid }).then(res => {
        if (res.data.status === 200) {
          this.$message({
            type: 'success',
            message: '退出成功'
          })
        }
      })
      this.deleteState()
      localStorage.clear()
      sendMsg('userlogout', 'success')
      location.replace(document.referrer)
      listenMsg(msg => {
        if (msg.data.type === 'response') {
          this.deleteState()
        }
      })
      sessionStorage.clear()
    },
    switchUser() {
      this.$router.push('/login', { query: { returnUrl: this.$route.fullPath } })
    },
    remainTopbarstyle() {
      // 书库页面刷新时topbar保留滑块样式
      if (this.$route.name === 'Bookhouse') {
        this.topbar = 2
        this.$refs.topbar.style.setProperty('--i', 5)
      } else if (this.$route.name === 'Main') {
        this.topbar = 0
      } else if (this.$route.name === 'Bookrank') {
        this.topbar = 1
        this.$refs.topbar.style.setProperty('--i', 3)
      } else {
        var ele = this.$refs.topbar
        ele.classList.add('hide-after')
        this.$refs.topbar.childNodes[this.topbar].className = ''
        return null
      }
      this.$refs.topbar.childNodes[this.topbar].className = 'checked'
    }
  }
}
</script>

<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
}

.outbox {
  background-color: rgba(218, 213, 213, 0.2);
  min-height: 100vh;
  margin: auto;
  padding-bottom: 90px;
}

.header {
  width: 1100px;
  height: 50px;
  margin: auto;
  line-height: 50px;
  display: flex;

  .topbar {
    flex: 40%;
    --i: 1;
    list-style: none;
    height: 50px;
    font-size: 16px;
    position: relative;

    .checked>a {
      color: red;
    }

    li {
      width: calc(100% / 3);
      text-align: center;
      display: inline-block;

      a {
        color: #b1aeae;
      }

      a:hover {
        color: rgb(225, 143, 143);
      }
    }
  }

  .topbar::after {
    content: '';
    transition: all 0.5s;
    position: absolute;
    bottom: 8px;
    left: calc(100% / 3 / 2 * var(--i));
    transform: translateX(-50%);
    width: 40px;
    height: 3px;
    background-color: red;
  }

  .hide-after::after {
    display: none;
  }

  .explore {
    flex: 50%;
    display: flex;
    justify-content: center;
    align-items: center;


    .main-input {
      width: 300px;
      vertical-align: middle;
    }

    .searchicon {
      background-color: #0099cc;
      display: inline-block;
      width: 40px;
      height: 40px;
      line-height: 40px;
      font-size: 25px;
    }
  }


  .userlog {
    width: 80px;
    border: #909399 solid 1px;
    border-radius: 6px;
    height: 30px;
    position: relative;
    top: 50%;
    z-index: 10;
    transform: translateY(-50%);
    display: flex;
    flex-direction: column;
    align-items: center;

    .usersign::before {
      position: absolute;
      color: #0099cc;
      content: attr(data-text);
      white-space: nowrap;
      height: 60px;
      display: inline-block;
      transition: 0.5s ease-in-out 0s;
      overflow: hidden;
    }

    .usersign:hover::before {
      height: 0;
    }

    .usersign {
      display: block;
      width: 100%;
      height: 100%;
      line-height: 30px;
      color: #333;

    }

    .u-menu {
      transform: translateX(-50%);
      width: 150px;
      background-color: rgb(210, 231, 249);
      border: #909399 solid 1px;
      border-radius: 10px;
      transform: scaleY(0);
      transform-origin: top;
      transition: transform 0.3s ease-in-out;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;

    }
  }

  .userlog:hover .u-menu {
    transform: scaleY(1);
    transform-origin: top;
  }
}

#tohead {
  display: none;
  width: 50px;
  height: 50px;
  line-height: 50px;
  font-size: 30px;
  position: relative;
  background-color: rgb(237, 239, 240);
  box-shadow: 0 0 6px rgba(0, 0, 0, 0.12);
  border-radius: 40%;
  position: fixed;
  bottom: 80px;
  right: 80px;
}
</style>
