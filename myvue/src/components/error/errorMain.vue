<template>
  <div>
    <div class="errtext">
      <el-empty :description="this.errortext"> </el-empty>
    </div>
  </div>
</template>

<script>
export default {
  props: ['errortext']
}
</script>

<style lang="less" scoped>
.errtext {
  width: 100%;
  height: 100%;
  font-size: 50px;
  font-family: 'Times New Roman', Times, serif;
}
</style>
