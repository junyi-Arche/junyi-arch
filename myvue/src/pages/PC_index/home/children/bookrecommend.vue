<template>
  <div class="bookrecommend">
    <slot name="title"></slot>
    <div class="bookcon">
      <div class="left-con" v-for="item in midboxbooks.slice(0, 1)" :key="item.id">
        <router-link target="_blank" :to="{
          path: '/main/bookdetail',
          query: { bid: item.id, bname: item.bookname }
        }" class="bookname">{{ item.bookname }}</router-link>
        <p class="author">作者:{{ item.bookauthor }}</p>
        <p class="desc">
          {{ item.bookdescri.slice(0, 60) + '...' }}
        </p>

        <div class="bookimg">
          <router-link target="_blank" :to="{
            path: '/main/bookdetail',
            query: { bid: item.id, bname: item.bookname }
          }">
            <img v-if="item.bookimgurl" :title="item.bookname" :src="item.bookimgurl" />
            <div v-else class="noimg">
              <i class="el-icon-picture-outline"></i>
            </div>
          </router-link>
        </div>
      </div>

      <slot name="content"></slot>

      <div class="right-con">
        <h3>畅销榜</h3>
        <ul class="hot-list">
          <li @mouseenter="() => {
            hotbookindex = index
          }
            " :class="hotbookindex === index ? 'act-li' : ''" v-for="(item, index) in hotbookData" :key="item.id">
            <span>{{ index + 1 }}</span>
            <router-link target="_blank" :to="{
              path: '/main/bookdetail',
              query: { bid: item.id, bname: item.bookname }
            }">
              <div class="content">
                <img v-if="item.bookimgurl" class="hotbook-s" v-show="hotbookindex === index" :title="item.bookname"
                  :src="item.bookimgurl" />
                <div v-else v-show="hotbookindex === index" class="hot-misimg">
                  <i class="el-icon-picture-outline"></i>
                </div>
              </div>
            </router-link>
            <div class="bookinfo">
              <router-link class="bookn" target="_blank" :to="{
                path: '/main/bookdetail',
                query: { bid: item.id, bname: item.bookname }
              }">
                <span>{{ slicestr(item.bookname, 10) }}</span>
              </router-link>
              <div class="clickn">
                <span v-show="hotbookindex === index">点击</span>
              </div>
            </div>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Bookrecommend',
  props: ['midboxbooks', 'hotbookData'],
  data() {
    return {
      hotbookindex: 0
    }
  }
}
</script>

<style lang="less" scoped>
.bookrecommend {
  display: inline-block;

  a {
    text-decoration: none;
  }

  .title {
    margin-top: 50px;
    padding: 0;
    font-size: 30px;
  }

  .bookcon {
    width: 1000px;
    height: 500px;
    background-color: #fff;
    display: flex;

    .bookimg {
      text-align: center;
      margin: 10%;

      img {
        width: 150px;
        height: 200px;
      }

      .noimg {
        width: 180px;
        height: 200px;
        font-size: 50px;
        display: flex;
        align-items: center;
        justify-content: center;
        background-color: #909399;
        opacity: 0.1;
      }
    }



    .left-con::before,
    .mid-bookde::after {
      position: absolute;
      top: 0;
      right: 0;
      content: '';
      width: 1px;
      height: 100%;
      border-right: #909399 1px solid;
      transform: scaleX(0.2);
    }

    .left-con {
      position: relative;
      text-align: left;
      flex: 30%;
      height: 400px;
      padding: 50px;

      .author {
        margin-bottom: 15px;
      }

      .bookname {
        text-decoration: none;
        display: inline-block;
        font-weight: 300;
        font-size: 23px;
        font-family: 'Microsoft Yahei', arial, sans-serif;
        margin-bottom: 15px;
      }
    }

    .right-con {
      flex: 25%;
      height: 90%;
      padding: 20px;

      h3 {
        margin: 0;
        height: 30px;
        font: 20px 'Microsoft Yahei', arial, sans-serif;
      }

      .hot-list {
        height: 100%;
        font: 15px 'Microsoft Yahei', arial, sans-serif;
        display: grid;
        grid-template-columns: repeat(1, 1fr);
        grid-template-rows: repeat(11, 1fr);
        align-items: center;

        li {
          display: flex;
          position: relative;
          text-align: left;

          span {
            margin-right: 7px;
          }

          .clickn {
            margin-top: 9px;
          }

          .content {
            .hot-misimg {
              width: 90px;
              height: 100px;
              font-size: 50px;
              display: flex;
              align-items: center;
              justify-content: center;
              background-color: #909399;
              opacity: 0.1;
            }

            .hotbook-s {
              width: 100px;
              height: 110px;
              display: inline-block;
              vertical-align: middle;
            }
          }
        }

        li::after {
          position: absolute;
          bottom: 0;
          right: 0;
          content: '';
          width: 100%;
          height: 1px;
          border-bottom: #909399 1px solid;
          transform: scaleY(0.2);
        }
      }

      .hot-list li:last-child::after {
        content: '';
        display: none;
      }
    }
  }
}
</style>
