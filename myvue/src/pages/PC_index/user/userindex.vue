<template>
  <div class="user-main">
    <div class="outbox">
      <div class="topcon">
        <div class="user">
          <div class="userimg"></div>
          <span>{{ $store.state.userinfo.username }}</span>
        </div>
        <div class="right-box">
          <p class="uid">ID: {{ $store.state.userinfo.userid }}</p>
          <p>余额: 0</p>
        </div>
      </div>
      <div class="content">
        <ul>
          <li @click="() => {
            this.comname = 'Userbooks'
          }
            ">
            <a href="javascript:;">拥有书籍</a>
          </li>
          <li @click="() => {
            this.comname = 'Userscan'
          }
            ">
            <a href="javascript:;">历史浏览</a>
          </li>
          <li @click="() => {
            this.comname = 'UserVip'
          }
            ">
            <a href="javascript:;">会员充值</a>
          </li>
        </ul>
        <component :is="comname"></component>
      </div>

    </div>
  </div>
</template>

<script>
import UserVip from './children/userVip.vue'
import Userscan from './children/userscan.vue'
import Userbooks from './children/userbooks.vue'
export default {
  data() {
    return {
      comname: 'Userbooks'
    }
  },
  methods: {
    changeCom(index) {
      if (index === 0) {
        this.comname = 'userdetail'
      } else if (index === 1) {
        this.comname = 'userbooks'
      } else if (index === 2) {
        this.comname = 'extention'
      }
    }
  },
  components: { Userbooks, UserVip, Userscan }
}
</script>

<style lang="less" scoped>
* {
  margin: 0;
  padding: 0;
}

.user-main {
  width: 1200px;
  margin: auto;
  position: relative;
}

.outbox {
  height: 700px;
  max-width: 90%;
  margin: auto;
  background-color: rgb(221, 231, 232);

  .topcon {
    overflow: hidden;

    .right-box {
      text-align: left;
      height: min-content;
      margin: 20px 10px;

      .uid {
        font-size: 25px;
      }
    }

    .user {
      width: min-content;
      height: min-content;
      padding: 20px;
      float: left;
      position: relative;

      span {
        font-size: 30px;
      }

      .userimg {
        font-size: 30px;
        width: 100px;
        height: 100px;
        line-height: 100px;
        border: 5px solid rgb(175, 169, 169);
        border-radius: 50%;
        margin: auto;
        background-color: #fff;
      }

      .userimg::after {
        content: '+';
        width: 40px;
        height: 40px;
        line-height: 40px;
        display: inline-block;
        border-radius: 20%;
        background-color: #ccc;
      }

      .userimg:hover {
        color: #dde5ba;
      }
    }
  }

  .content {
    margin: auto;

    ul {
      background-color: #fff;
      width: 100%;
      height: 50px;
      line-height: 50px;
      list-style: none;

      li {
        width: calc(100% / 3);
        float: left;

        a {
          font-size: 20px;
        }
      }

      li:hover {
        background-color: #bde6bb;
      }
    }
  }
}
</style>
