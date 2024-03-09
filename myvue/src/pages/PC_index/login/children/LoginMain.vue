<template>
  <div class="login-main">
    <el-form class="loginFrom" :model="user" :rules="rules">
      <el-form-item class="numbox">
        <i class="el-icon-user-solid icon"></i>
        <el-input class="userinp" name="usernum" type="text" v-model.trim="user.usernum" autocomplete="off"></el-input>
      </el-form-item>
      <el-form-item class="pwdbox" prop="userpwd">
        <i class="el-icon-lock icon"></i>
        <el-input class="userinp" name="userpwd" type="password" ref="pwdinp" v-model.trim="user.userpwd"
          autocomplete="off" show-password></el-input>
      </el-form-item>
      <el-form-item prop="email">
        <el-input class="userinp" v-model="user.email" placeholder="请输入qq邮箱" name="email"></el-input>
      </el-form-item>
      <el-form-item>
        <div class="modeverify"><el-input v-model="user.mode" type="text" placeholder="输入验证码"></el-input><el-button
            @click="getVerifyMode">获取验证码</el-button>
        </div>
      </el-form-item>
    </el-form>

    <div class="footer">
      <div class="alog">
        <input ref="autolog" type="checkbox" id="autolog" /><label for="autolog">自动登录</label>
      </div>
      <div id="forgetpwd">
        <router-link to="/forgetpwd">忘记密码</router-link>
      </div>
    </div>
    <el-button id="loginbtn" @click="login">
      <div>登录</div>
    </el-button>
  </div>
</template>

<script>
import https, { fetchPost } from '@/api/http'
import { mapActions } from 'vuex'
import eventBus from '@/components/eventBus.js'
import { sendMsg } from '@/static/js/crossTagMsg.js'
export default {
  name: 'LoginMain',
  data() {
    const validatePass = (rule, value, callback) => {
      if (!value && this.user.usernum === '') {
        return callback(new Error('请输入密码'))
      }
      callback()
    }
    const validateEmail = (rule, value, callback) => {
      if (!value && this.user.email === '') {
        return callback(new Error('请输入qq邮箱'))
      } else {
        var regEx = /^[1-9]\d{4,10}@qq\.com$/;
        if (!regEx.test(value)) {
          callback(new Error('请输入正确qq邮箱'))
        }
      }
      callback()
    }
    return {
      user: {
        usernum: '',
        userpwd: '',
        email: '',
        mode: ''
      },
      rules: {
        userpwd: [{ validator: validatePass, trigger: 'blur' }],
        email: [{ validator: validateEmail, trigger: 'blur' }]
      }
    }
  },
  mounted() {
    const saveduser = localStorage.getItem('userinfo')
    const autolog = localStorage.getItem('ulog')
    if (autolog) {
      this.$refs.autolog.checked = true
    }
    if (saveduser) {
      const userlist = JSON.parse(saveduser)[0]
      this.user.usernum = userlist.userid
      this.user.userpwd = userlist.pwd
      this.$refs.savepwd.checked = true
    }
  },
  activated() {
    eventBus.$on('shareu', (val) => {
      this.user.usernum = val
    })
  },
  methods: {
    ...mapActions(['updateState']),
    async login() {
      if (this.user.usernum === '' || this.user.userpwd === '') {
        this.$message.error('请输入账号和密码！')
      } else if (this.user.mode.length < 6) {
        this.$message.error('请输入6位数字验证码')
      } else {
        const data = {
          usernum: this.user.usernum,
          pwd: this.crypt(this.user.userpwd + ',c2hhMjU2'),
          mode: this.user.mode,
          email: this.user.email.split('.')[0]
        }
        await https.fetchPost('/login', data).then((res) => {
          if (res.data.login) {
            const userlogdata = {
              username: res.data.uname,
              userid: data.usernum,
              lg: true
            }
            localStorage.setItem('ulog', res.data.ulog)
            localStorage.setItem('currentuser', JSON.stringify(userlogdata))
            if (this.$refs.autolog.checked) {
              localStorage.setItem('expirelog', '1')
            } else {
              localStorage.removeItem('expirelog')
            }
            window.name = 'reload'
            sendMsg('userlogin', 'success')
            const returnUrl = this.$route.query.returnUrl || '/';
            this.$router.push(returnUrl);
            console.log('登录成功')
          } else {
            localStorage.clear()
            this.$message.warning('用户名不存在或者密码不正确')
          }
        }).catch((err) => {
          this.$message({
            type: 'error',
            message: "登录失败,请检查网络"
          })
        })
      }
    },
    async getVerifyMode() {
      if (this.user.email == ''){
        this.$message({
          type: 'error',
          message: '请输入邮箱'
        })
        return
      }
      const data = {
        email: this.user.email,
        _: String(new Date().getTime()) + '1'
      }
      await fetchPost('/CaptchaGet', data).then(res => {
        if (res.status == 200) {
          this.$message({
            type: 'success',
            message: '验证码发送成功，请查看qq邮箱'
          })
        } else {
          this.$message({
            type: 'error',
            message: '验证码发送失败'
          })
        }
      }).catch(err => {
        this.$message({
          type: 'error',
          message: err
        })
      })
    }
  }
}
</script>
<style lang="less" scoped>
.loginFrom {
  width: 350px;
  margin: auto;
  text-align: right;
  position: relative;

  .modeverify {
    display: flex;
    width: 300px;
    position: absolute;
    right: 0;
  }

  .userinp {
    width: 300px;
    font-size: 18px;
  }

  .icon {
    font-size: 30px;
    vertical-align: middle;
  }
}

.footer {
  display: flex;
  font-size: 17px;
  margin-top: 15%;

  .alog {
    flex: 50%;
    height: 35px;
    line-height: 35px;
    text-align: center;
  }

  #forgetpwd {
    flex: 50%;
    text-align: center;
    height: 35px;
    font-size: 14px;
    line-height: 35px;

    a {
      color: black;
    }
  }
}

#loginbtn {
  width: 200px;
  height: 50px;
  font-size: 25px;
  font-family: 'Microsoft Yahei', serif;
  margin: 20px auto 0;
  background-color: #409eff;
  color: #000;
  border-radius: 8px;
}

#loginbtn:hover {
  opacity: 0.7;
}
</style>
