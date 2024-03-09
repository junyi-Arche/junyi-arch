<template>
  <div v-if="!loading">
    <ErrorMain v-if="error"></ErrorMain>
    <div v-else>
      <Bookmodel>
        <template v-slot:title>
          <h2 class="modelname">小说作品</h2>
        </template>
        <template v-slot:leftcon>
          <ul class="commend">
            <li @mouseenter="updateItem(1, 0, index)" v-for="(item, index) in rankbooks.novels.slice(0, 5)" :key="index">
              <div class="leftitems">
                <span>{{ index + 1 }}</span>
                <router-link target="_blank" v-show="top[0] == index"
                  :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                  <div class="leftimg">
                    <img :src="item.bookimgurl" :title="item.bookname" />
                  </div>
                </router-link>
                <div class="leftdes">
                  <router-link target="_blank" :to="{ path: '/main/bookdetail', query: { bid: item.id } }">{{
                    item.bookname
                  }}</router-link>
                  <p v-show="top[0] == index">
                    <span class="author">作者：{{ item.bookauthor }}</span><br />
                    <span class="visi">查看</span><br />
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </template>
        <template v-slot:middlecon>
          <ul class="commend">
            <li @mouseenter="updateItem(1, 1, index)" v-for="(item, index) in rankbooks.novels.slice(5, 10)" :key="index">
              <div class="leftitems">
                <span>{{ index + 1 }}</span>
                <router-link target="_blank" v-show="top[1] == index"
                  :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                  <div class="leftimg">
                    <img :src="item.bookimgurl" :title="item.bookname" />
                  </div>
                </router-link>
                <div class="leftdes">
                  <router-link target="_blank" to="">{{ item.bookname }}</router-link>
                  <p v-show="top[1] == index">
                    <span class="author">作者：{{ item.bookauthor }}</span><br />
                    <span class="visi">查看</span><br />
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </template>
        <template v-slot:rightcon>
          <ul class="commend">
            <li @mouseenter="updateItem(1, 2, index)" v-for="(item, index) in rankbooks.novels.slice(10, 15)"
              :key="index">
              <div class="leftitems">
                <span>{{ index + 1 }}</span>
                <router-link target="_blank" v-show="top[2] == index"
                  :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                  <div class="leftimg">
                    <img :src="item.bookimgurl" :title="item.bookname" />
                  </div>
                </router-link>
                <div class="leftdes">
                  <router-link target="_blank" :to="{ path: '/main/bookdetail', query: { bid: item.id } }">{{
                    item.bookname
                  }}</router-link>
                  <p v-show="top[2] == index">
                    <span class="author">作者：{{ item.bookauthor }}</span><br />
                    <span class="visi">查看</span><br />
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </template>
      </Bookmodel>
      <Bookmodel>
        <template v-slot:title>
          <h2 class="modelname">历史传记</h2>
        </template>
        <template v-slot:leftcon>
          <ul class="commend">
            <li @mouseenter="updateItem(2, 0, index)" v-for="(item, index) in rankbooks.histories.slice(0, 4)"
              :key="index">
              <div class="leftitems">
                <span>{{ index + 1 }}</span>
                <router-link target="_blank" v-show="next[0] == index"
                  :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                  <div class="leftimg">
                    <img :src="item.bookimgurl" :title="item.bookname" />
                  </div>
                </router-link>
                <div class="leftdes">
                  <router-link target="_blank" :to="{ path: '/main/bookdetail', query: { bid: item.id } }">{{
                    item.bookname
                  }}</router-link>
                  <p v-show="next[0] == index">
                    <span class="author">作者：{{ item.bookauthor }}</span><br />
                    <span class="visi">查看</span><br />
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </template>
        <template v-slot:middlecon>
          <ul class="commend">
            <li @mouseenter="updateItem(2, 1, index)" v-for="(item, index) in rankbooks.histories.slice(4, 10)"
              :key="index">
              <div class="leftitems">
                <span>{{ index + 1 }}</span>
                <router-link target="_blank" v-show="next[1] == index"
                  :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                  <div class="leftimg">
                    <img :src="item.bookimgurl" :title="item.bookname" />
                  </div>
                </router-link>
                <div class="leftdes">
                  <router-link target="_blank" :to="{ path: '/main/bookdetail', query: { bid: item.id } }">{{
                    item.bookname
                  }}</router-link>
                  <p v-show="next[1] == index">
                    <span class="author">作者：{{ item.bookauthor }}</span><br />
                    <span class="visi">查看</span><br />
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </template>
        <template v-slot:rightcon>
          <ul class="commend">
            <li @mouseenter="updateItem(2, 2, index)" v-for="(item, index) in rankbooks.histories.slice(10, 15)"
              :key="index">
              <div class="leftitems">
                <span>{{ index + 1 }}</span>
                <router-link target="_blank" v-show="next[2] == index"
                  :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                  <div class="leftimg">
                    <img :src="item.bookimgurl" :title="item.bookname" />
                  </div>
                </router-link>
                <div class="leftdes">
                  <router-link target="_blank" :to="{ path: '/main/bookdetail', query: { bid: item.id } }">{{
                    item.bookname
                  }}</router-link>
                  <p v-show="next[2] == index">
                    <span class="author">作者：{{ item.bookauthor }}</span><br />
                    <span class="visi">查看</span><br />
                  </p>
                </div>
              </div>
            </li>
          </ul>
        </template>
      </Bookmodel>
    </div>
  </div>
</template>

<script>
import { fetchGet } from '@/api/http';
import Bookmodel from './children/bookmodel.vue'
export default {
  data() {
    return {
      top: [0, 0, 0],
      next: [0, 0, 0],
      rankbooks: {},
      loading: true,
      error: false
    }
  },
  async created() {
    await fetchGet('/bookrank').then(res => {
      this.rankbooks = res.data
      this.loading = false
    }).catch(err => {
      this.loading = false
      this.error = true
    })
  },
  methods: {
    updateItem(item, i, val) {
      if (item == 1) {
        this.$set(this.top, i, val)
      } else if (item == 2) {
        this.$set(this.next, i, val)
      }

    }
  },
  components: {
    Bookmodel,
    ErrorMain: () => import('@/components/error/errorMain.vue')
  }
}
</script>

<style lang="less" scoped>
.modelname {
  margin: 30px 0;
}

.leftimg {
  img {
    width: 80px;
    height: 100px;
  }

}
</style>
