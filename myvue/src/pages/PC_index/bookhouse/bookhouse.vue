<template>
  <div class="bookdata">
    <Errormain v-if="error || empty" errortext="数据为空"></Errormain>
    <div v-else class="main_container">
      <div class="category" v-show="!error && !empty">
        <ul ref="category">
          <li v-for="item, index in category" :key="item.catekey">
            <a @click="catechange($event, 1)" href="javascript:;">{{ item.catekey }}</a>
            <ol v-show="currentcate == item.catekey" v-for="(item1, index1) in item.valuesList" :key="index1">
              <li><a href='javascript:;' @click.stop="initBookList(1, item1, 2, 1)">{{
                item1 }}</a></li>
            </ol>
          </li>
        </ul>
      </div>
      <div class="right_box">
        <div ref="booklist" class="bookdetail">
          <Loadmore v-show="isloading" v-for="item in 15" :key="item.id"></Loadmore>
          <div class="bookitem" v-for="item in booklist" :key="item.id">
            <router-link class="bookimgcontainer" target="_blank"
              :to="{ path: '/main/bookdetail', query: { bid: item.id, bname: item.bookname } }">
              <div class="bookimg" v-if="item.bookimgurl">
                <img :title="item.bookname" :src="item.bookimgurl" />
              </div>
              <div v-else class="noimg">
                <i class="el-icon-picture-outline"></i>
              </div>
            </router-link>
            <div class="detail">
              <router-link target="_blank"
                :to="{ path: '/main/bookdetail', query: { bid: item.id, bname: item.bookname } }">
                <div class="title">
                  <h3>{{ slicestr(item.bookname, 10) }}</h3>
                </div>
              </router-link>
              <div class="b-desc">
                <span>{{ item.author }}</span>
                <h4>{{ slicestr(item.bookdescri, 62) }}</h4>
              </div>
            </div>
          </div>
        </div>
        <div class="pages-com">
          <ol ref="pbtn">
            <div class="pagebtn">
              <a @click="switchpage(1, true)" href="javascript:;">首页</a>
            </div>
            <div class="pagebtn">
              <a @click="switchpage(0, false)" href="javascript:;">上一页</a>
            </div>
            <div class="more" v-show="c_page >= 5">...</div>
            <li :class="c_page == index ? 'act' : ''"
              v-if="c_page > 4 ? (c_page - 2 <= index && index <= c_page + 2) : index <= 5" v-for="index in page"
              :key="index">
              <a @click="catetype(index, false)" href="javascript:;">{{ index }}</a>
            </li>
            <div class="more" v-show="c_page < maxpage - 2">...</div>
            <div class="pagebtn">
              <a @click="switchpage(1)" href="javascript:;">下一页</a>
            </div>
            <div class="pagebtn">
              <a @click="switchpage(maxpage, true)" href="javascript:;">尾页</a>
            </div>
          </ol>
        </div>
      </div>

    </div>
  </div>
</template>

<script>
import http from '@/api/http'
import Loadmore from '@/components/load/loadmore.vue'
import pako from 'pako'
import { MyData } from '@/static/js/proto/bookStack_pb'
export default {
  name: 'Bookrank',
  data() {
    return {
      maxpage: 0,
      c_page: 1,
      page: [],
      booklist: [],
      isloading: false,
      empty: false,
      category: [],
      currentcate: '',
      error: false
    }
  },
  created() {
    this.initBookList(1, 0, 0, 1)
  },
  watch: {
    maxpage(newval, _oldval) {
      this.maxpage = newval
      this.page = []
      for (var i = 1; i <= this.maxpage; i++) {
        this.page.push(i)
      }
    },
    c_page(newval, _oldval) {
      this.c_page = newval
      const actli = this.$refs.pbtn.querySelector('.act')
      actli.classList.remove('act')
      this.$nextTick(() => {
        window.scrollTo(0, 0)
      })
    }
  },
  methods: {
    catetype(i) {
      if (this.currentcate == '') {
        this.initBookList(i, this.currentcate, 0)
        return null
      }
      for (var j = 0; j < this.category.length; j++) {
        if (this.category[j].catekey == this.currentcate) {
          this.initBookList(i, this.currentcate, 1)
          return null
        }
      }
      this.initBookList(i, this.currentcate, 2)
    },

    catechange(e, p) {
      this.c_page = 1
      const catebtn = this.$refs.category.querySelectorAll('.checked')
      if (catebtn.length) {
        catebtn[0].classList.remove('checked')
      }
      e.target.parentNode.classList.add('checked')
      this.currentcate = e.target.innerText
      this.initBookList(p, e.target.innerText, 1, 1)
    },
    switchpage(page, flag) {
      if (flag) {
        if (page == this.c_page) {
          return
        }
        this.c_page = page
        this.catetype(page)
      } else {
        if (page) {
          if (this.c_page >= this.maxpage) {
            return null
          } else {
            this.c_page++
          }
        } else {
          if (this.c_page === 1) {
            return null
          } else {
            this.c_page--
          }
        }
        this.catetype(this.c_page)
      }
    },
    /**
     * Initializes the book list.
     *
     * @param {number} p - The current page.
     * @param {string} c - The category.
     * @param {boolean} f - The flag for first time.
     * @param {boolean} s - The flag for second category.
     * @return {null} A promise that resolves when the book list is initialized.
     */
    async initBookList(p, c, s, f) {
      this.booklist = []
      this.c_page = p
      let reqdata
      this.isloading = true
      reqdata = { _page: p }
      switch (s) {
        case 0:
          break
        case 1:
          reqdata['category'] = c
          break
        case 2:
          reqdata['scategory'] = c
          break
      }
      switch (f) {
        case 1:
          reqdata['f'] = ''
          break
      }

      try {
        await http.fetchGet('/bookdata', reqdata).then(res => {
          const byteCharacters = atob(res.data);
          const byteNumbers = new Array(byteCharacters.length);
          for (let i = 0; i < byteCharacters.length; i++) {
            byteNumbers[i] = byteCharacters.charCodeAt(i);
          }
          const byteArray = new Uint8Array(byteNumbers);
          const decompressedData = pako.inflate(byteArray)
          const finaldata = MyData.deserializeBinary(decompressedData).toObject()
          const bookdata = finaldata.bookdataList
          if (f) {
            this.maxpage = finaldata.mpage
            if (s == 0) {
              const categorieslist = finaldata.category.categoryMapList
              var catelist = []
              categorieslist.forEach(ele => {
                catelist.push(ele.categoryItems.categoryListList[0])
              });
              this.category = catelist
            }
          }
          this.booklist = bookdata
          this.empty = bookdata.length === 0
        })
        this.isloading = false
      } catch (error) {
        this.isloading = false
        this.error = true
      }
    }
  },
  components: {
    Loadmore,
    Errormain: () => import('@/components/error/errorMain.vue')
  }
}
</script>

<style scoped lang="less">
.bookdata {
  width: 1400px;
  margin: auto;
  position: relative;

  .main_container {
    display: flex;
    height: 200%;
  }

}

.pages-com {
  display: flex;
  justify-content: center;
  align-items: center;
  position: absolute;
  left: 50%;
  bottom: -90px;
  transform: translateX(-50%);

  ol {
    list-style: none;
    display: flex;

    li,
    .pagebtn,
    .more {
      border-radius: 5px;
      width: 50px;
      height: 50px;
      line-height: 50px;
      background-color: #fff;
      margin: 10px 7px;
    }

    .pagebtn {
      a {
        color: #000;
      }

      width: 100px;
    }

    .act {
      background-color: #d1cbcb;

      a {
        pointer-events: none;
      }
    }
  }
}

.right_box {
  flex: 85%;
  position: relative;
  margin-bottom: 90px;
}

.category>ul:empty {
  border: none;
  overflow: hidden;
}

.category {
  margin-top: 20px;
  flex: 15%;

  ul {
    width: 80%;
    margin: auto;
    list-style: none;
    border: #909399 solid 1px;
    background-color: #f1f4e6;

    .subcate {
      display: none;
    }

    li {
      width: 100%;
      padding: 5px 0;
      font-size: 20px;
      border-top: 1px solid #909399;

      a:hover {
        color: #e3a2a2;
      }

      ol {
        list-style: none;
        background-color: #fff;

        li {
          opacity: 0.5;

          a:focus {
            color: #000;
          }
        }
      }
    }

    .checked {
      background-color: #9bb7da;
      text-decoration: none;
    }
  }
}

.bookdetail {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  grid-auto-rows: 180px;
  margin: 30px auto 0;

  .bookitem {
    display: flex;
    background-color: #fff;
    color: #000;
    text-decoration: none;
    height: 100%;

    .bookimgcontainer {
      width: 35%;
    }

    .bookimg {
      height: 100%;

      img {
        width: 100%;
        height: 100%;
      }
    }

    .noimg {
      width: 100%;
      height: 100%;
      font-size: 50px;
      display: flex;
      align-items: center;
      justify-content: center;
      background-color: #909399;
      opacity: 0.1;
    }

    .detail {
      width: 65%;
      margin: 0 auto;
      text-align: left;
      padding: 10px;

      .title {
        margin: 5px 0;
      }

      .b-desc {
        color: #9e9e9e;

        span {
          text-align: left;
          display: inline-block;
        }

        font: 12px 'Microsoft Yahei',
        arial,
        sans-serif;
        font-weight: lighter;

        h4 {
          margin-bottom: 0;
        }
      }
    }
  }

  .bookitem:hover {
    box-shadow: 0 2px 12px 0 rgba(0, 0, 0, 0.1)
  }
}
</style>
