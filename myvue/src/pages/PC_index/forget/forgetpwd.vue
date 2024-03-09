<template>
  <div class="main">
    <p class="back"><a href="javascript:history.go(-1)">返回登录</a></p>
    <div class="forgetbox">
      <div v-show="!exist" class="userinp">
        <p>请输入账号</p>
        <el-form class="inp_form">
          <el-form-item><el-input v-model="usernum" type="text" autofocus required /><br /></el-form-item>
          <el-form-item>
            <el-input v-model="email" placeholder="请输入qq邮箱" type="text"></el-input>
          </el-form-item>
          <el-form-item>
            <div class="modeverify"><el-input type="text" v-model="mode"
                placeholder="输入验证码"></el-input><el-button>获取验证码</el-button>
            </div>
          </el-form-item>
        </el-form>


        <el-button style="margin-top: 5px" type="primary" @click="submit()">提交</el-button>
      </div>
      <div v-if="exist" class="resetpwd">
        <p>重新设置密码</p>
        <el-form :model="pwd" :rules="rules" ref="resetpwd">
          <el-form-item class="input" prop="userpwd">
            <el-input v-model="pwd.userpwd" type="password" placeholder="新密码" />
          </el-form-item>
          <el-form-item class="input" prop="userpwd2">
            <el-input v-model="pwd.userpwd2" type="password" placeholder="确认新密码" />
          </el-form-item>
        </el-form>
        <el-button style="margin-top: -10px" type="primary" @click="resetsub('resetpwd')">提交</el-button>
      </div>
    </div>

  </div>
</template>

<script>
import { fetchGet, fetchPost } from '@/api/http'
import { Md5 } from 'ts-md5'

export default {
  data() {
    const validatePass = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请输入密码'))
      } else if (value.length < 6) {
        callback(new Error('请输入6位以上的密码'))
      } else {
        if (this.pwd.userpwd2 !== '') {
          this.$refs.resetpwd.validateField('userpwd2')
          callback()
        }
      }
    }
    const validatePass2 = (rule, value, callback) => {
      if (value === '') {
        callback(new Error('请再次输入密码'))
      } else if (value !== this.pwd.userpwd) {
        callback(new Error('两次输入密码不一致'))
      } else {
        callback()
      }
    }
    return {
      usernum: '',
      userid: '',
      email: '',
      mode: '',
      exist: false,
      pwd: {
        userpwd: '',
        userpwd2: ''
      },
      rules: {
        userpwd: [{ validator: validatePass, trigger: 'blur' }],
        userpwd2: [{ validator: validatePass2, trigger: 'blur' }]
      }
    }
  },
  methods: {
    async submit() {
      if (this.usernum === '') {
        return false
      } else {
        await fetchGet('/forgetpwd', { usernum: this.usernum }).then(res => {
          if (res.data.status === 200) {
            this.exist = true
            this.userid = res.data.id
          } else {
            this.exist = false
            this.$message.error('用户名不存在!')
          }
        }).catch(err => {
          this.exist = false
          this.$message.error('出现错误')
        })

      }
    },
    async resetsub(formname) {
      this.$refs[formname].validate(async (valid) => {
        if (valid) {
          await fetchPost('/forgetpwd', {
            id: this.userid,
            userpwd: this.crypt(this.pwd.userpwd2 + ',c2hhMjU2,'),
            mode: this.mode,
            email: this.email
          }).then(res => {
            if (res.data.status === 200) {
              this.$router.replace('/login')
              this.$message.success('密码设置成功！')
            }
          })
        }
      })
    }
  }
}
</script>

<style scoped lang="less">
.main {
  width: fit-content;
  margin: 50px auto;

  .back {
    font-size: 20px;
    text-align: left;
    margin-bottom: 20px;
  }

  .forgetbox {
    width: 400px;
    height: 370px;

    background-color: #d0e2cb;
    border-radius: 10px;

    p {
      margin: 0;
      padding-top: 10px;
      font-size: 25px;
    }

    .inp_form {
      width: 220px;
      margin: 20px auto;

      .modeverify {
        display: flex;
        width: 100%;

        button {
          flex: 1;
          font-size: 14px;
        }
      }
    }
  }
}
</style>
