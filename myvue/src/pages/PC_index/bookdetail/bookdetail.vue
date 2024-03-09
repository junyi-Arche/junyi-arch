<template>
  <div>
    <component :is="comName"></component>
  </div>
</template>

<script>
export default {
  data() {
    return {
      chapterNames: []
    }
  },
  computed: {
    comName() {
      return this.$route.name
    }
  },
  components: {
    Bookdetail: () => import('./children/detailMain.vue'),
    Bookchapter: () => import('./children/bookchapter.vue')
  }
}
</script>

<style lang="less" scoped></style>