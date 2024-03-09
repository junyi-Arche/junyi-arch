<template>
  <div id="app">
    <router-view></router-view>
  </div>
</template>

<script>
import { mapActions } from 'vuex'
export default {
  name: 'App',
  watch: {
    '$route'(to, from) {
      if (to.name === 'Bookchapter') {
        this._onbeforeTime = this.$cookies.get('_onbeforeTime'); // 读取cookie值
        if (this._onbeforeTime) {
          const bookinfo = JSON.parse(sessionStorage.getItem('bookdata'));
          this.updateBookinfo(bookinfo);
        }
        window.addEventListener('beforeunload', () => {
          window.name = 'reload';
          this.$cookies.set('_onbeforeTime', new Date().getTime(), 2);
          const bookinfo = JSON.stringify(this.$store.state.bookdata);
          sessionStorage.setItem('bookdata', bookinfo);
        })
      }
    }
  },

  created() {
    if (this.isMobile()) {
      this.$router.push('/Mmain')
    }
  },
  methods: {
    ...mapActions(['updateBookinfo']),

    isMobile() {
      const flag = navigator.userAgent.match(
        /(phone|pad|pod|iPhone|iPod|ios|iPad|Android|Mobile|BlackBerry|IEMobile|MQQBrowser|JUC|Fennec|wOSBrowser|BrowserNG|WebOS|Symbian|Windows Phone)/i
      )
      return flag
    },
    browserTest() {
      if (navigator.userAgentData) {
        // 如果浏览器支持navigator.userAgentData
        const userAgentData = navigator.userAgentData;
        const browserName = userAgentData.brands[0].brand;
        const browserVersion = userAgentData.brands[0].version;

        // 进一步处理获取的浏览器信息
      } else {
        // 如果浏览器不支持navigator.userAgentData，您可以回退到使用其他方式获取信息
        // 比如使用navigator.userAgent、navigator.appVersion、特性检测等
        console.log('浏览器不支持navigator.userAgentData');
      }
    }
  }
}
</script>

<style lang="less" scoped>
#app {
  font-family: Avenir, Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
}
</style>
