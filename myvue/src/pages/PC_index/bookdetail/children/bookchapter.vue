<template>
    <div class="chapteroutbox">
        <div class="menu">
            <ul class="charpter_t_list">
                <li v-for="item, index in chaptername" :key="index"><a :class="cid == index ? 'active' : ''"
                        href="javascript:;" :title="item" @click="changeChapter(index)"><span>{{ index + 1 + '.' }}</span>
                        {{ slicestr(item, 15) }}</a></li>
            </ul>
        </div>
        <div class="container">
            <p class="text-top">正文</p>
            <p class="text-chapter">{{ chaptername[this.$route.query.cid] }}</p>
            <p class="text-book"><span>{{ bookname }}</span><span>作者: {{ author }}</span></p>
            <div class="mainchaptercontent">
                <p v-for="item in chapterdata">{{ item }}</p>
            </div>
        </div>
    </div>
</template>
<script>
import { fetchGet } from '@/api/http'
import router from '@/router';
import { mapMutations } from 'vuex';
export default {
    data() {
        return {
            cid: this.$route.query.cid,
            chaptername: [],
            chapterdata: [],
            bookname: '',
            author: ''
        };
    },
    created() {
        this.inita();
        this.chaptername = this.$store.state.bookdata.chapter;
        this.bookname = this.$store.state.bookdata.bookname;
        this.author = this.$store.state.bookdata.author;
    },
    updated() {
        window.document.title = this.bookname + '-' + this.chaptername[this.cid];
    },
    methods: {
        ...mapMutations({ SET_BOOKCHAPTER: 'SET_BOOKCHAPTER' }),
        async inita() {
            this.chapterdata = [];
            await fetchGet('/BookChapterContent/' + this.$route.query.bid, { cid: this.cid }).then(res => {
                res.data.content.split('\n').forEach(item => {
                    this.chapterdata.push(item);
                });
            }).catch(err => {
                console.log(err);
            });
        },
        changeChapter(i) {
            if (i == this.cid) {
                return
            }
            this.cid = i
            this.$router.replace({
                path: '/main/bookdetail/bookchapter',
                query: {
                    bid: this.$route.query.bid,
                    cid: i
                }
            })
            this.inita()
        }
    },
    components: { router }
}
</script>

<style lang="less" scoped>
.chapteroutbox {
    width: 1100px;
    margin: auto;
    position: relative;

    .menu {
        position: relative;
        position: absolute;
        left: -300px;
        top: 50px;
        background-color: rgb(219, 193, 193);
        width: 300px;
        height: fit-content;

        .charpter_t_list {
            display: grid;
            grid-template-columns: repeat(1, 2fr);
            grid-auto-rows: 50px;

            li {
                font-weight: 550;
                text-align: left;
                padding-left: 20px;
                line-height: 50px;
                position: relative;

                .active {
                    color: gray;
                }

                a:hover {
                    color: rgb(131, 187, 236);
                }

                span {
                    border: 3px rgba(228, 228, 85, 0.5) solid;
                    border-radius: 50%;
                    background-color: aliceblue;
                }
            }

            li:after {
                position: absolute;
                top: 0;
                left: 50%;
                transform: translateX(-50%) scaleY(0.1);
                content: '';
                width: 100%;
                height: 1px;
                background-color: black;
            }
        }
    }

    .menu::after {
        content: '';
        display: inline-block;
        position: absolute;
        top: 0;
        left: 0;
        width: 10px;
        height: 200px;
        background-color: rgb(250, 219, 219);
    }

    .container {
        .text-top {
            text-align: left;
        }

        .text-chapter {
            font-size: 6ex;
            font-weight: 600px;
            margin: 18px 0;
        }

        .text-book {
            font-size: 18px;
            margin-bottom: 10px;
            font-weight: 600;
            color: rgb(206, 151, 151);

            span {
                margin: 0 10px;
            }
        }
    }

    .mainchaptercontent {
        width: 90%;
        margin: auto;
        line-height: 38px;
        background: rgba(0, 0, 0, 0) url(https://a.dushu.com/img/lines.png) repeat-y scroll 0 0;

        p {
            font-size: 20px;
            font-weight: 650;
            text-align: left;
        }
    }
}
</style>