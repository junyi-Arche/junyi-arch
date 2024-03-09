<template>
    <div class="details">
        <div v-if="!error" class="main-box">
            <div class="bookBox">
                <div class="bookimg">
                    <img :src="this.bookdata.bookimgurl" :title="this.bookdata.bookname" />
                </div>
                <div class="bookDeBox">
                    <div class="de_top">
                        <h1>{{ this.bookdata.bookname }}</h1>
                        <div class="author_publisher">
                            <span>作者: {{ this.bookdata.author }}</span>
                            <span>出版社: {{ this.bookdata.publisher }}</span>
                        </div>
                    </div>
                    <div class="de_bottom">
                        <span><button @click="addtoshelf()">{{ hasbook }}</button></span>
                        <span><button @click="readbook(0)">开始阅读</button></span>
                    </div>
                </div>
            </div>
            <div class="desc">
                <p>{{ this.bookdata.bookdescri }}</p>
            </div>
            <div class="chapters">
                <ul>
                    <li>
                        <h3>章节内容</h3>
                    </li>
                    <li v-for="(item, index) in this.bookdata.bookchaptertitle" :key="index">
                        <a @click="readbook(index)" href="javascript:;">{{
                            item
                        }}</a>
                    </li>
                </ul>
            </div>
            <div class="recomend">
                <h3>推荐阅读</h3>
                <div class="bookrecomendbox">
                    <div class="book" v-for="(item, index) in recomendbooks" :key="index">
                        <div class="Bimg">
                            <router-link :to="{ path: '/main/bookdetail', query: { bid: item.id } }">
                                <img :src="item.bookimgurl" :title="item.bookname" />
                            </router-link>
                        </div>
                        <div class="bookinfo">
                            <p><router-link :to="{ path: '/main/bookdetail', query: { bid: item.id } }">{{ item.bookname
                            }}</router-link></p>
                            <span>作者: {{ item.author }}</span>
                        </div>
                    </div>
                </div>
            </div>
            <div class="conment">
                <div class="header">
                    <div class="des">
                        <span>圈子</span>
                        <span>{{ comUsernum }}人, 共{{ bookcomments.length }}条评论</span>
                        <button @click="(e) => {
                            this.$refs.usercomment.style.display = 'flex'
                            e.target.style.display = 'none'
                            this.$refs.publish.style.display = 'inline-block'
                            this.$refs.usercomment.children[1].children[0].focus()
                        }
                            " class="conmentBtn">
                            评论
                        </button>
                        <button ref="publish" @click="publish()" class="conmentBtn publish">发布</button>
                    </div>
                    <div ref="usercomment" class="user-coment">
                        <div class="com-user">{{ $store.state.userinfo.username }}</div>
                        <el-input name="usercomment" resize="none" :autosize="{ minRows: 2, maxRows: 4 }" maxlength="200"
                            show-word-limit type="textarea" class="usercom" v-model="usercomment"></el-input>
                    </div>
                </div>

                <div v-for="(item, index) in bookcomments" :key="item.comment" class="comments">
                    <div class="com-user user"></div>
                    <div class="com-warp">
                        <div class="userinfo">{{ item.username }}</div>
                        <div class="root-com">
                            <span>{{ item.comment }}</span>
                            <div class="com-info">
                                <div>{{ item.addtime }}</div>
                                <div></div>
                            </div>
                        </div>
                        <div v-if="islogin && item.userid === $store.state.userinfo.userid" class="oprate">
                            <el-dropdown trigger="click">
                                <i class="el-icon-more"></i>
                                <el-dropdown-menu slot="dropdown">
                                    <el-dropdown-item @click.native="deletecomment(item, index)">删除</el-dropdown-item>
                                    <el-dropdown-item>修改</el-dropdown-item>
                                </el-dropdown-menu>
                            </el-dropdown>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div v-else>
            <Errormain errortext="没有书籍数据"></Errormain>
        </div>
    </div>
</template>
  
<script>
import { fetchGet, fetchPost } from '@/api/http'
import { sendMsg } from '@/static/js/crossTagMsg'
import { mapMutations } from 'vuex'

export default {
    name: 'Bookdetail',
    data() {
        return {
            bookdata: {},
            recomendbooks: [],
            error: false,
            userhaving: 0,
            usercomment: '',
            bookcomments: []
        }
    },
    watch: {
        bookdata(newval, _oldval) {
            this.bookdata = newval
            if (Object.keys(this.bookdata).length === 0) {
                this.error = true
            } else {
                this.error = false
            }
        },
        '$route'(to, from) {
            if (to.query.bid != from.query.bid) {
                this.fetchBookDetail();
                this.$nextTick(() => {
                    window.scrollTo(0, 0)
                })
            }
        }
    },
    computed: {
        hasbook() {
            return this.userhaving == 1 ? '已加入书架' : '加入书架'
        },
        islogin() {
            const user = localStorage.getItem('currentuser')
            return user
        },
        comUsernum() {
            let userdict = {}
            this.bookcomments.forEach(item => {
                if (userdict[item.userid]) {
                    userdict[item.userid] += 1
                } else {
                    userdict[item.userid] = 1
                }
            })
            return Object.keys(userdict).length
        }
    },
    created() {
        this.fetchBookDetail()
    },
    methods: {
        ...mapMutations({ SET_BOOK: 'SET_BOOK', SET_BOOKCHAPTER: 'SET_BOOKCHAPTER' }),
        readbook(index) {
            this.$router.push({
                path: '/main/bookdetail/bookchapter',
                query: { bid: this.bookdata.id, cid: index }
            })
            window.scrollTo(0, 0)
            this.SET_BOOKCHAPTER(this.bookdata.bookchaptertitle)
        },
        async deletecomment(item, i) {
            let token = localStorage.getItem('ulog')
            await fetchPost('/delbookcomment', {
                utoken: token,
                comid: item.comid
            }).then(res => {
                if (res.data.status === 200) {
                    this.bookcomments.splice(i, 1)
                }
            })
        },
        async publish() {
            if (this.$store.state.userinfo.userid == '') {
                this.$confirm('请先登录', '提示', {
                    confirmButtonText: '确定',
                    cancelButtonText: '取消',
                    type: 'info'
                }).then(() => {
                    this.$router.push({ path: '/login', query: { returnUrl: this.$route.fullPath } })
                }).catch(() => {
                    return
                });
            } else {
                if (this.usercomment == '') {
                    this.$message.error('请输入评论')
                } else {
                    await fetchPost('/addbookcomment', {
                        con: this.usercomment,
                        b_id: this.bookdata.id,
                        utoken: localStorage.getItem('ulog')
                    }).then(res => {
                        if (res.data.status === 200) {
                            this.$message.success('评论成功')
                            this.bookcomments.unshift({
                                comid: res.data.comid,
                                userid: this.$store.state.userinfo.userid,
                                username: this.$store.state.userinfo.username,
                                comment: this.usercomment,
                                addtime: new Date().toLocaleString()
                            })
                            this.usercomment = ''
                        }
                    }).catch(err => {
                        console.log(err);
                        this.$message.error('评论失败')
                    })

                }
            }

        },
        async fetchBookDetail() {
            try {
                let bid = this.$route.query.bid
                const query = {
                    b_id: bid
                }
                if (localStorage.getItem('currentuser')) {
                    query.utoken = localStorage.getItem('ulog')
                    await fetchGet('/bookdetail', query).then(res => {
                        this.bookdata = res.data.bookdata
                        this.userhaving = res.data.userhaving == 1 ? 1 : 0
                        this.recomendbooks = res.data.recomends
                    })

                } else {
                    await fetchGet('/bookdetail', query).then(res => {
                        this.bookdata = res.data.bookdata
                        this.recomendbooks = res.data.recomends
                    })

                }
                await fetchGet('/getbookcomment', { b_id: bid }).then(res => {
                    if (res.data.status === 200) {
                        this.bookcomments = res.data.comments
                    }
                })

                window.document.title = this.bookdata.bookname
                this.SET_BOOK([this.bookdata.bookname, this.bookdata.author])
            } catch {
                this.error = true
                this.$message({
                    showClose: true,
                    duration: 1500,
                    type: 'error',
                    message: '数据加载失败'
                })
            }


        },
        async addtoshelf() {
            if (this.$store.state.userinfo.userid == '') {
                this.$message.error('请先登录')
            } else {
                if (this.userhaving == 1) {
                    this.$message.error('您已经加入书架')
                } else {
                    try {
                        await fetchPost('/addtoshelf', {
                            b_id: this.bookdata.id,
                            utoken: localStorage.getItem('ulog')
                        })
                        sendMsg('updateUserbookshelf')
                        this.$message.success('添加书架成功')
                        this.userhaving = 1
                    } catch (error) {
                        this.$message.error('添加书架失败')
                    }
                }
            }
        }
    },
    components: {
        Errormain: () => import('@/components/error/errorMain.vue')
    }
}
</script>
  
<style lang="less" scoped>
.main-box {
    width: 900px;
    margin: auto;
    text-align: left;

    .bookBox {
        margin-top: 30px;
        display: flex;
        background-color: #fff;

        .bookimg {
            padding: 10px;
            vertical-align: top;

            img {
                width: 130px;
                height: 150px;
            }
        }

        .bookDeBox {
            width: 100%;
            height: fit-content;

            .de_top {
                height: 50%;

                .author_publisher {
                    margin-top: 10px;

                    span {
                        font-size: smaller;
                        margin: 20px;
                    }
                }
            }

            .de_bottom {
                height: 50%;

                span {
                    display: inline-block;
                    margin: 10px 20px;
                }

                button {
                    width: 100px;
                    height: 30px;
                    background: #ccc8c8;
                    border: none;
                }
            }
        }
    }

    .desc {
        margin-top: 10px;
        width: 840px;
        padding: 30px;
        border: 2px solid rgb(170, 165, 165);
        display: block;
    }

    .chapters {
        width: 50%;
        margin-top: 20px;

        ul {
            list-style: none;

            li {
                padding: 6px 10px;
                width: 100%;
                border: 1px solid rgb(170, 165, 165);
            }
        }
    }

    .recomend {
        width: 100%;
        margin: 20px auto;
        border: 2px solid rgb(170, 165, 165);
        padding: 20px;

        h3 {
            text-align: center;
            padding: 6px 0;
            border-bottom: 1px solid rgb(170, 165, 165);
        }

        .bookrecomendbox {
            margin-top: 15px;
            display: grid;
            grid-template-columns: repeat(2, 1fr);
            gap: 20px;
            grid-auto-rows: 180px;

            .book {
                width: 100%;
                height: 100%;
                display: flex;

                .bookinfo {
                    flex: 70%;
                    padding: 10px;

                    p {
                        margin-bottom: 12px;
                        font-size: 18px;
                        font-weight: 550;
                    }
                }

                .Bimg {
                    flex: 30%;

                    img {
                        width: 100%;
                        height: 100%;
                    }
                }
            }
        }
    }

    .conment {
        margin: 30px auto 0;
        width: 80%;
        background-color: #fff;

        .header {
            width: 100%;
            position: relative;

            .des {
                height: 8%;
                display: flex;
                align-items: center;
                justify-content: left;

                span {
                    margin: 20px 0 20px 30px;
                }

                span:nth-child(1) {
                    font-size: larger;
                    position: relative;
                }

                span:nth-child(1)::after {
                    content: '';
                    display: inline;
                    position: absolute;
                    right: -15px;
                    top: 50%;
                    transform: translateY(-50%);
                    width: 2px;
                    height: 20px;
                    background-color: #ca2424;
                }

                .conmentBtn {
                    width: 100px;
                    display: inline-block;
                    border: none;
                    height: 40px;
                    position: absolute;
                    right: 10%;
                }

                .publish {
                    display: none;
                }
            }

            .header::after {
                content: '';
                display: inline-block;
                position: absolute;
                left: 50%;
                bottom: 0;
                transform: translateX(-50%);
                width: 95%;
                height: 1px;
                background-color: gray;
            }
        }

        @keyframes slidedown {
            0% {
                height: 1px;
                opacity: 0;
            }

            100% {
                height: 150px;
                opacity: 1;
            }
        }

        .user-coment {
            display: none;
            animation: slidedown 0.5s;
            background-color: rgba(210, 218, 199, 0.4);
            width: 100%;
            height: 135px;
            position: relative;
            align-items: center;

            .com-user {
                width: 80px;
                height: 80px;
                line-height: 80px;
                border-radius: 50%;
                margin-left: 30px;
                font-size: 10px;
                font-weight: 900;
                text-align: center;
                background-color: rgb(73, 144, 230);
            }

            .usercom {
                display: inline-block;
                position: absolute;
                font-size: 20px;
                left: 20%;
                top: 50%;
                transform: translateY(-50%);
                width: 70%;

                input {
                    min-height: 70px;
                }
            }
        }

        .comments {
            position: relative;
            display: flex;
            width: 100%;
            height: 120px;
            padding-top: 15px;
            background-color: #e5e8e9;

            .user {
                width: 60px;
                height: 60px;
            }

            .com-warp {
                padding-left: 20px;
                width: 100%;
                height: 90%;

                .userinfo {
                    color: #e94141;
                    font-weight: 600;
                    margin-bottom: 20px;
                }

                .root-com {
                    span {
                        font-weight: 550;
                    }

                    .com-info {
                        margin-top: 10px;
                    }
                }

                .oprate {
                    width: 20px;
                    height: 20px;
                    position: absolute;
                    bottom: 10px;
                    right: 35px;
                    font-size: 20px;
                }
            }
        }

        .comments::after {
            content: '';
            position: absolute;
            bottom: 0;
            left: 50%;

            width: 90%;
            height: 1px;
            background-color: gray;
            transform: translateX(-50%) scaleY(0.5)
        }
    }
}
</style>
  