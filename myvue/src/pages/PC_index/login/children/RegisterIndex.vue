<template>
  <div class="register-main">
    <div class="detail">
      <el-form ref="loginform" :model="user" status-icon :rules="rules" label-width="78px">
        <el-form-item class="usernumipt" label="账号" prop="usernum" required>
          <el-input name="usernum" type="text" v-model.trim="user.usernum"></el-input>
        </el-form-item>
        <el-form-item class="userpwd" label="密码" prop="userpwd" required>
          <el-input name="userpwd" type="password" id="pwd" v-model="user.userpwd"></el-input>
        </el-form-item>
        <el-form-item class="userpwd2" label="确认密码" prop="checkpwd" required>
          <el-input type="password" id="confirmpwd" v-model="user.checkpwd"></el-input>
        </el-form-item>
        <el-form-item label="QQ邮箱" prop="email" required>
          <el-input v-model="user.email" placeholder="请输入qq邮箱" type="text" name="email"></el-input>
        </el-form-item>
        <el-form-item label="验证码" prop="mode">
          <div class="modeverify"><el-input v-model="user.mode" type="text" placeholder="输入验证码"
              name="mode"></el-input><el-button @click="getVerifymode">获取验证码</el-button>
          </div>
        </el-form-item>
      </el-form>
    </div>
    <router-link to="" id="submitBtn">
      <div @click="GetRegister('loginform')" id="registerbtn">注册</div>
    </router-link>
  </div>
</template>

<script>
import https from '@/api/http'
import eventBus from '@/components/eventBus'
import { fetchPost } from '@/api/http'

export default {
  name: 'RegisterIndex',
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码！'))
      } else if (value.length < 6) {
        callback(new Error('请输入6位以上的密码'))
      } else {
        if (this.user.checkpwd !== '') {
          this.$refs.loginform.validateField('checkpwd')
        }
        callback()
      }
    }
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.user.userpwd) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    const validateUser = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入账号'))
      } else if (value.length > 10 || value.length < 6) {
        callback(new Error('请输入6到10位数字'))
      } else {
        const pattern = /\d{6,10}$/
        const res = pattern.test(value)
        if (res) {
          callback()
        } else {
          callback(new Error('只能使用数字组合'))
        }
      }
    }
    const validateEamail = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入qq邮箱'))
      } else {
        var regEx = /^[1-9]\d{4,10}@qq\.com$/;
        if (!regEx.test(value)) {
          callback(new Error('请输入正确qq邮箱'))
        }
      }
      callback()
    }
    const validateMode = (rule, value, callback) => {
      if (value === '' || value.length < 6) {
        callback(new Error('请输入验证码'))
      }
      callback()
    }
    return {
      user: {
        usernum: '',
        userpwd: '',
        checkpwd: '',
        email: '',
        mode: ''
      },
      rules: {
        userpwd: [{ validator: validatePass, trigger: 'blur' }],
        checkpwd: [{ validator: validatePass2, trigger: 'blur' }],
        usernum: [{ validator: validateUser, trigger: 'blur' }],
        email: [{ validator: validateEamail, trigger: 'blur' }],
        mode: [{ validator: validateMode, trigger: 'blur' }]
      }
    }
  },
  methods: {
    GetRegister(formName) {
      this.$refs[formName].validate((valid) => {
        if (valid) {
          const data = {
            usernum: this.user.usernum,
            userpwd: this.crypt(this.user.userpwd + ',c2hhMjU2,'),
            mode: this.user.mode,
            email: this.user.email.split('.')[0]
          }
          https.fetchPost('/register', data).then((res) => {
            if (!res.data.register) {
              alert(res.data.msg)
            } else {
              this.$emit('comchange', 'login')
              eventBus.$emit('shareu', this.user.usernum)
            }
          }).catch((err) => {
            this.$message.error('注册失败')
          })
        } else {
          console.log('Error submit!!')
          return false
        }
      })
    },
    async getVerifymode() {
      const data = {
        email: this.user.email,
        _: String(new Date().getTime()) + '2'
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
.detail {
  width: 360px;
  margin: 0 auto;

  .modeverify {
    display: flex;

    span {
      font-size: 14px;
    }
  }
}

#submitBtn {
  display: inline-block;

  #registerbtn {
    width: 200px;
    height: 50px;
    line-height: 50px;
    font-size: 25px;
    font-family: 'Microsoft Yahei', serif;
    background-color: #67c23a;
    border-radius: 8px;
  }
}

#submitBtn:hover {
  opacity: 0.7;
}
</style>
