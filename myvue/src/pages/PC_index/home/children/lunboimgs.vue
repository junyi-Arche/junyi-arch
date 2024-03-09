<template>
  <div id="lbbg" class="lunbo" v-if="flag">
    <div class="comment-text">
      <span class="title-txt">{{ this.lunbodata[bookindex].bookname }}</span>
      <p class="con-txt" style="color: black">
        {{ slicestr(this.lunbodata[this.bookindex].bookdescri, 100) }}
      </p>
    </div>
    <div class="main-imgs">
      <ul :style="groupStyle" class="slider-list">
        <li @mouseenter="mouseon(index)" @mouseleave="autolunbo()" ref="lunboimgs" v-for="(item, index) in this.lunbodata"
          v-show="showimgs(index)" :key="index">
          <router-link :class="index == bookindex ? 'active' : ''" target="_blank" :to="{
            path: '/main/bookdetail',
            query: { bid: item.id, bname: item.bookname }
          }">
            <img :src="item.bookimgurl" :title="item.bookname" />
          </router-link>
        </li>
      </ul>
    </div>

    <div ref="indicators" class="indicator">
      <span :class="index == 0 ? 'dot-active' : ''" v-for="(item, index) in this.lunbodata.length / 5"
        :key="item.id"></span>
    </div>
    <div class="left-btn" @click="backup"></div>
    <div class="right-btn" @click="forward"></div>
  </div>
</template>

<script>
export default {
  name: 'Lunboimgs',
  props: ['lunbodata'],
  data() {
    return {
      flag: false,
      timer: '',
      pageindex: 0,
      bookindex: 0
    }
  },
  watch: {
    lunbodata() {
      if (this.lunbodata.length > 0) {
        this.flag = true
      }
    }
  },
  computed: {
    groupStyle() {
      return {
        'transition-duration': '500ms'
      }
    }
  },
  activated() {
    this.autolunbo()
  },
  deactivated() {
    clearInterval(this.timer)
  },
  destroyed() {
    clearInterval(this.timer)
  },
  methods: {
    /**
     * @author junyi
     * @param {number} index 图片的索引值
     * @return {boolean}
     */
    showimgs(index) {
      if (index < 5 && this.pageindex === 0) {
        return true
      } else if (index >= 5 && this.pageindex > 0) {
        return true
      } else {
        return false
      }
    },
    mouseon(index) {
      clearInterval(this.timer)
      this.resetallAct()
      this.bookindex = index
      this.$refs.lunboimgs[index].childNodes[0].classList = 'active'
    },
    changeIcon(index) {
      const doms = {
        indicators: this.$refs.indicators.childNodes
      }
      document.querySelector('.dot-active').classList.remove('dot-active')
      doms.indicators[index].classList.add('dot-active')
    },
    resetallAct() {
      const lis = this.$refs.lunboimgs
      if (lis){
        for (var i = 0; i < lis.length; i++) {
        lis[i].childNodes[0].classList = ''
      }
      }
      
    },
    autolunbo() {
      this.timer = setInterval(() => {
        this.resetallAct()
        this.bookindex++
        if (this.pageindex === 0 && this.bookindex > 4) {
          this.bookindex = 0
        } else if (this.pageindex === 1 && this.bookindex > 9) {
          this.bookindex = 5
        }
        this.$refs.lunboimgs[this.bookindex].childNodes[0].classList = 'active'
      }, 2000)
    },
    forward() {
      if (this.pageindex >= 1) {
        this.pageindex = 0
      } else {
        this.pageindex++
      }
      this.adjustset()
    },
    backup() {
      if (this.pageindex <= 0) {
        this.pageindex = 1
      } else {
        this.pageindex--
      }
      this.adjustset()
    },
    adjustset() {
      clearInterval(this.timer)
      this.bookindex = this.pageindex * 5
      this.changeIcon(this.pageindex)
      this.autolunbo()
    }
  }
}
</script>

<style lang="less" scoped>
.lunbo {
  max-width: 1800px;
  height: 400px;
  margin: auto;
  position: relative;
  background-color: #5d7986;

  .main-imgs {
    width: 800px;
    position: absolute;
    bottom: 50px;
    left: 50%;
    transform: translateX(-50%);
  }

  .comment-text {
    width: 800px;
    margin: auto;
    padding-top: 20px;

    .title-txt {
      font-size: 30px;
      color: #fff;
    }

    .con-txt {
      margin-top: 20px;
    }
  }

  .slider-list {
    display: flex;
    position: relative;
    list-style: none;

    li {
      animation: fade-in-out 0.7s ease-in-out 1;

      @keyframes fade-in-out {
        0% {
          opacity: 0.2;
        }

        100% {
          opacity: 1;
        }
      }
    }

    @keyframes scaleimg {
      0% {
        scale: 1;
      }

      100% {
        scale: 1.1;
      }
    }

    .active {
      box-shadow: 0px 0px 10px 5px rgba(0, 0, 0, 0.3);
      animation: scaleimg 0.4s ease-in-out 1;
      scale: 1.1;
    }

    a {
      display: inline-block;
      margin: 0 10px;
    }

    img {
      width: 140px;
      height: 180px;
    }
  }

  .left-btn,
  .right-btn {
    width: 50px;
    height: 100px;
    line-height: 100px;
    position: absolute;
    top: 50%;
    transform: translateY(-50%);
    opacity: 0.3;
  }

  .left-btn {
    left: 100px;
  }

  .right-btn {
    right: 100px;
  }

  .left-btn::after {
    content: '<';
  }

  .right-btn::after {
    content: '>';
  }

  .right-btn::after,
  .left-btn::after {
    width: 50px;
    height: 100px;
    display: block;
    font-size: 70px;
    background-color: #ccc;
  }

  .left-btn:hover,
  .right-btn:hover {
    color: #000;
    opacity: 0.6;
  }

  .indicator {
    position: absolute;
    bottom: 10px;
    display: flex;
    left: 50%;
    transform: translateX(-50%);
    z-index: 1;

    span {
      width: 5px;
      height: 5px;
      border: 1px solid #ccc;
      border-radius: 50%;
      margin: 0 3px;
    }

    .dot-active {
      background: #fff;
      border-color: #fff;
    }
  }
}
</style>
