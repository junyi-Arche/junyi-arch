// 滑动到底部加载更多
scrollHandle = function () {
  if (this.isloading || this.finished) return
  // 获取内容高度
  const scrollH = document.documentElement.scrollHeight
  // 获取窗口高度
  const innerH = window.innerHeight
  // 获取页面滚出去的内容高度
  const top = document.body.scrollTop || document.documentElement.scrollTop
  if (scrollH - top - innerH <= 10) {
    this.initBookList(this.page, this.pageSize)
  }
}
