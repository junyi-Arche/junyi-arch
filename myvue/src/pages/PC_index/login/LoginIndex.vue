<template>
  <div class="outerloginbox">
    <div class="login-box">
      <h3>
        <a href="javascript:" @click="comname = 'login'">登录</a> /
        <a href="javascript:" @click="comname = 'register'">注册</a>
      </h3>
      <transition mode="out-in">
        <keep-alive include="LoginMain">
          <component @comchange="getnewCOM" :is="comname"></component>
        </keep-alive>
      </transition>
    </div>
  </div>
</template>

<script>
import login from '@/pages/PC_index/login/children/LoginMain.vue'
import register from '@/pages/PC_index/login/children/RegisterIndex.vue'
export default {
  name: 'LoginBox',
  data() {
    return {
      comname: 'login'
    }
  },
  methods: {
    getnewCOM(val) {
      this.comname = val
    }
  },
  components: {
    login,
    register
  }
}
</script>

<style lang="less" scoped>
.outerloginbox {
  background: linear-gradient(125deg, #b8fa9f, #eb5050, #5ab4e8, #bc81ec);
  background-size: 500%;
  display: flex;
  justify-items: center;
  height: 100vh;
  animation: bgAnimation 15s linear infinite;
}

@keyframes bgAnimation {
  0% {
    background-position: 0% 50%;
  }

  50% {
    background-position: 100% 50%;
  }

  100% {
    background-position: 0% 50%;
  }
}

h3>a {
  color: coral;
}

.v-enter,
.v-leave-to {
  opacity: 0;
}

.v-enter-active,
.v-leave-active {
  transition: 0.3s;
}

.login-box {
  h3 {
    margin-bottom: 20px;
  }

  margin: auto;
  padding: 20px;
  width: 400px;
  height: 550px;
  border-radius: 5px;
  font-size: 20px;
  background-color: #e5e8ec;
}</style>
