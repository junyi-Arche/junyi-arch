<template>
  <div class="userBooks">
    <div v-show="userbooks.length > 0" class="options">
      <div v-if="editMode" ref="optional" class="opbtnbox">
        <div @click="selectAll()" class="select opbtn"><a href="javascript:;">全选</a></div>
        <div @click="delselect()" class="del opbtn"><a href="javascript:;">删除</a></div>
      </div>
      <div class="mainbtn opbtn"><a href="javascript:;" @click="() => { this.editMode = !this.editMode }">{{ this.editMode
        ? '完成' : '编辑' }}</a></div>
    </div>
    <div class="maincontent">
      <div ref="userbooks" v-for="(item, index) in userbooks" :key="index" class="bookis">
        <input @change="switch_opcaticy(index)" v-if="editMode" :name="item.id" type="checkbox" class="isselect">
        <a class="bookimg-a" href="javascript:;" @click="todetail($event, item, index)"><img :src="item.bookimgurl"
            :title="item.bookname" />
        </a>
        <p>{{ item.bookname }}</p>
      </div>
    </div>
  </div>
</template>

<script>
import { fetchPost } from '@/api/http'
import { listenMsg, revlistenMsg } from '@/static/js/crossTagMsg'
export default {
  name: 'Userbooks',
  data() {
    return {
      editMode: false,
      userbooks: []
    }
  },
  watch: {
    editMode() {
      if (this.editMode) {
        this.$refs.userbooks.forEach(item => {
          item.style.opacity = '0.5'
        })
      } else {
        this.$refs.userbooks.forEach(item => {
          item.style.opacity = '1'
        })
      }
    }
  },
  mounted() {
    this.getuserbook()
    this.$nextTick(() => {
      listenMsg(msg => {
        if (msg.data.type === 'updateUserbookshelf') {
          this.getuserbook()
        }
      })
    })
  },
  methods: {
    delselect() {
      let dellist = []
      this.$refs.userbooks.forEach(item => {
        if (item.childNodes[0].checked) {
          dellist.push(item.childNodes[0].name)
        }
      })
      if (dellist.length === 0) {
        return
      }
      this.$confirm('此操作将永久删除该文件, 是否继续?', '提示', {
        confirmButtonText: '确定',
        cancelButtonText: '取消',
        type: 'warning'
      }).then(() => {
        let utoken = localStorage.getItem('ulog')
        fetchPost('/deleteUserbookshelf', { bookidList: dellist, utoken: utoken }).then(res => {
          if (res.data.status === 200) {
            location.reload(location.href)
            this.$message.success('删除成功')
          }
        }).catch(err => {
          console.log(err);
        })
      }).catch(() => {
        this.$message({
          type: 'info',
          message: '已取消删除'
        });
      });
    },
    selectAll() {
      const userbooks = this.$refs.userbooks
      userbooks.forEach(item => {
        item.childNodes[0].checked = true
        item.style.opacity = '1'
      })
    },
    todetail(e, item, i) {
      if (!this.editMode) {
        this.$router.push({ path: '/main/bookdetail', query: { bid: item.id } })
      } else {
        e.stopPropagation();
        e.preventDefault();
        const userbooks = this.$refs.userbooks
        const checkbox = userbooks[i].childNodes[0]
        if (checkbox.checked) {
          checkbox.checked = false
        } else {
          checkbox.checked = true
        }
        this.switch_opcaticy(i)
      }
    },
    switch_opcaticy(i) {
      const userbooks = this.$refs.userbooks
      const checkbox = userbooks[i].childNodes[0]
      if (checkbox.checked) {
        userbooks[i].style.opacity = '1'
      } else {
        userbooks[i].style.opacity = '0.5'
      }
    },
    async getuserbook() {
      const user = localStorage.getItem('ulog')
      if (user) {
        await fetchPost('/getuserbook', { user: user }).then(res => {
          if (res.data.status === 200) {
            this.userbooks = res.data.userbooks
          } else if (res.data.status === 403) {
            this.$router.push('/login')
          }
        }).catch(err => {
          console.log(err)
          this.$message.error('获取用户书架失败')
        })
      } else {
        this.$router.push('/login')
      }
    }
  }
}
</script>
<style lang="less" scoped>
.userBooks {
  height: 100%;

  .options {
    width: 100%;
    height: 55px;
    display: flex;
    justify-content: flex-end;
    align-items: center;

    .mainbtn {
      margin-right: 20px;
    }

    .opbtnbox {
      display: flex;
    }

    .opbtn {
      width: 80px;
      height: 30px;
      font-size: smaller;
      line-height: 30px;

      a {
        color: #1b62e6;
      }
    }

    .opbtn:hover {
      background-color: #b6d5dc;
    }
  }
}

.maincontent {
  width: 100%;
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  grid-template-rows: 1fr 1fr;
  grid-auto-rows: 200px;
  gap: 3px;

  .bookis {
    padding: 15px;
    position: relative;

    .bookimg-a {
      display: inline-block;
      position: relative;
    }

    .isselect {
      position: absolute;
      width: 20px;
      height: 20px;
      top: 10px;
      left: 28px;
      display: inline-block;
      cursor: pointer;
    }

    img {
      border-radius: 10%;
      width: 100px;
      height: 120px;
    }
  }
}
</style>
