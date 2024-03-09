<template>
  <el-skeleton class="bookitem" style="display: inline-block; width: 100%; height:100%">
    <template slot="template">
      <div style="display: flex">
        <el-skeleton-item variant="image" style="width: 150px; height: 180px" />
        <div style="width: 200px; justify-items: center; margin: auto">
          <el-skeleton-item variant="text" style="width: 150px" />
          <el-skeleton-item variant="text" style="width: 30%" />
        </div>
      </div>
    </template>
  </el-skeleton>
</template>
<script>
export default {}
</script>
<style lang="less" scoped></style>
