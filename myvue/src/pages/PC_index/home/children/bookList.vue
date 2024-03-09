<template>
  <div class="bookList">
    <ErrorIndex errortext="页面数据加载失败" v-if="err"></ErrorIndex>
    <div v-else>
      <Lunboimgs :lunbodata="mainbookData.lunboData"></Lunboimgs>
      <div v-if="flag" class="bookbox">
        <Bookrecommend :midboxbooks="mainbookData['storyData']['stories']"
          :hotbookData="mainbookData.storyData.hotbookData">
          <template v-slot:title>
            <p class="title">网络小说</p>
          </template>
          <template v-slot:content>
            <ul class="mid-con">
              <li v-for="item in mainbookData['storyData']['stories'].slice(1, 5)" :key="item.id" class="mid-bookde">
                <router-link target="_blank" :to="{
                  path: '/main/bookdetail',
                  query: { bid: item.id, bname: item.bookname }
                }">
                  <img class="mid-img" v-if="item.bookimgurl" :title="item.bookname" :src="item.bookimgurl" alt="" />
                  <div v-else class="misimg">
                    <i class="el-icon-picture-outline"></i>
                  </div>
                  <br />
                  <span class="bookex line2">{{ slicestr(item.bookname, 8) }}</span><br />
                </router-link>
                <span>{{ slicestr(item.bookauthor, 8) }}</span>
              </li>
            </ul>
          </template>
        </Bookrecommend>
        <Bookrecommend :midboxbooks="mainbookData['netvols']['novels']" :hotbookData="mainbookData.netvols.hotnovels">
          <template v-slot:title>
            <p class="title">热门频道</p>
          </template>
          <template v-slot:content>
            <ul class="next-mid-con">
              <li v-for="item in mainbookData['netvols']['novels'].slice(1, 7)" :key="item.id" class="mid-bookde">
                <router-link target="_blank" :to="{
                  path: '/main/bookdetail',
                  query: { bid: item.id, bname: item.bookname }
                }">
                  <span class="bookex">
                    {{ slicestr(item.bookname, 8) }}
                  </span> </router-link> <br />
                <p>{{ slicestr(item.bookauthor, 8) }}</p>
                <br />
                <p>{{ slicestr(item.bookdescri, 25) }}</p>
              </li>
            </ul>
          </template>
        </Bookrecommend>
      </div>
    </div>
  </div>
</template>

<script>
import Lunboimgs from './lunboimgs.vue'
import Bookrecommend from './bookrecommend.vue'
import { fetchGet } from '@/api/http'

export default {
  name: 'BookList',
  data() {
    return {
      flag: false,
      err: false,
      mainbookData: []
    }
  },
  watch: {
    mainbookData: function (newval, _oldval) {
      this.mainbookData = newval
      this.flag = true
    }
  },
  created() {
    this.initbooks()
  },
  methods: {
    async initbooks() {
      try {
        const res = await fetchGet('/books')
        this.mainbookData = res.data.bookdata
      } catch (error) {
        this.$message({
          showClose: true,
          duration: 1500,
          type: 'error',
          message: '服务器连接失败，请检查网络'
        })
        this.err = true
      }
    }
  },
  components: {
    Lunboimgs,
    Bookrecommend,
    ErrorIndex: () => import('@/components/error/errorMain.vue')
  }
}
</script>

<style lang="less" scoped>
.bookList {
  width: 100%;
  margin: auto;

}

.mid-con {
  flex: 35%;
  width: 100%;
  height: 500px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(50%, 2fr));
  grid-auto-rows: 250px;
}

.line2 {
  margin-bottom: 10px;
}

.mid-con li:nth-child(-n + 2)::before,
.next-mid-con li:nth-child(-n + 4)::before {
  position: absolute;
  bottom: 0;
  right: 0;
  content: '';
  width: 100%;
  height: 1px;
  border-bottom: #909399 1px solid;
  transform: scaleY(0.2);
}

.next-mid-con {
  flex: 40%;
  height: 500px;
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(50%, 1fr));
  grid-template-rows: repeat(auto-fit, minmax(33%, 1fr));
}

.mid-bookde {
  padding: 13px;
  position: relative;
  text-align: left;

  .mid-img {
    display: flex;
    width: 108px;
    height: 130px;
    margin: auto;
  }

  p {
    font-size: smaller;
    display: inline-block;
    margin-top: 7px;
  }

  .bookex {
    font-size: 15px;
    font-weight: 700;
    color: black;
  }

}

.misimg {
  width: 108px;
  height: 120px;
  margin: 20px auto 0;
  font-size: 50px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #909399;
  opacity: 0.1;
}

.bookbox {
  max-width: 1600px;
  margin: auto;

  .title {
    margin-bottom: 20px;
  }
}
</style>
