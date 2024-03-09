<template>
  <div class="bookrankmodel">

    <slot name="title"></slot>
    <div class="bookcon">
      <div class="left-con">
        <p class="headtitle"><span></span>编者推荐</p>
        <slot name="leftcon"></slot>
      </div>
      <div class="middle-con">
        <p class="headtitle"><span></span>书籍热销</p>
        <slot name="middlecon"></slot>
      </div>
      <div class="right-con">
        <p class="headtitle"><span></span>新书上榜</p>
        <slot name="rightcon"></slot>
      </div>
    </div>
  </div>
</template>

<script>
export default {}
</script>

<style lang="less" scoped>
.bookrankmodel {
  display: flex;
  flex-direction: column;
  justify-content: center;
  align-items: center;
}

.bookcon>div:nth-child(-n + 2)::after {
  position: absolute;
  top: 0;
  right: 0;
  content: '';
  width: 1px;
  height: 100%;
  border-right: #909399 1px solid;
  transform: scaleX(0.2);
}

.bookcon {
  width: 1000px;
  height: 500px;
  background-color: #fff;
  display: flex;

  .headtitle {
    display: inline-block;
    font-size: 22px;

    span {
      display: inline-block;
      width: 5px;
      height: 19px;
      vertical-align: middle;
      margin-right: 9px;
      background-color: #03a9f4;
      border-radius: 10px;
    }
  }

  .commend {
    height: 90%;
    display: grid;
    grid-template-rows: repeat(10, 1fr);
    margin-top: 10px;

    li {
      position: relative;
      display: flex;
      text-align: left;
      align-items: center;
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

    .leftitems {
      display: flex;
      line-height: 20px;
      max-inline-size: 2;

      span {
        margin-right: 9px;
      }

      .leftdes {
        p {
          font-size: 8px;
          margin: 0;
        }
      }
    }
  }

  .left-con,
  .middle-con,
  .right-con {
    padding: 20px;
    text-align: left;
    position: relative;
    flex: calc(100% / 3);
  }
}
</style>
