<template>
  <div class="searchsrank">
    <div v-if="searchdata.length" class="itembooks">
      <div v-for="item in searchdata" :key="item.id" class="book-item">
        <router-link target="_blank"
          :to="{ path: '/main/bookdetail', query: { bid: item.id, bname: item.bookname } }"><img :src="item.bookimgurl"
            :title="item.bookname" /></router-link>
        <div class="bookdes">
          <h2>{{ item.bookname }}</h2>
          <p>{{ item.bookauthor }}</p><br>
          <span>{{ item.bookdescri }}</span>
        </div>
      </div>
    </div>
    <ErrorMain v-else></ErrorMain>
  </div>
</template>

<script>
import { fetchPost } from '@/api/http'

export default {
  data() {
    return {
      searchdata: []
    }
  },
  watch: {
    '$route'(to, from) {
      if (to.query.bn != from.query.bn) {
        this.fetchData();
      }
    },
  },
  created() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      await fetchPost('/searchbook', {
        bn: this.$route.query.bn
      }).then(res => {
        if (res.data.status === 200) {
          this.searchdata = res.data.searchbooks
        } else {
          this.searchdata = []
        }
      }).catch(err => {
        this.$message.error('搜索失败')
      })
    }
  },
  components: {
    ErrorMain: () => import('@/components/error/errorMain.vue')
  }

}
</script>

<style lang="less" scoped>
.itembooks {
  margin: auto;
  width: 800px;

  .book-item {
    display: flex;
    padding: 20px;
    margin: 30px 0;
    border: 2px black solid;

    img {
      width: 160px;
      height: 200px;
    }

    .bookdes {
      flex: 70%;

      h2 {
        margin-bottom: 13px;
      }

    }
  }
}
</style>
