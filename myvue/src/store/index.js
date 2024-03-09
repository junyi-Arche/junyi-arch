import Vuex from 'vuex'
import Vue from 'vue'

Vue.use(Vuex)
const store = new Vuex.Store({
  state: {
    userinfo: {
      username: '',
      userid: ''
    },
    bookdata: {
      chapter: '',
      bookname: '',
      author: ''
    }
  },
  mutations: {
    SET_USER: (state, data) => {
      state.userinfo.username = data
    },
    SET_USERID: (state, data) => {
      state.userinfo.userid = data
    },
    SET_BOOK: (state, data)=>{
      state.bookdata.bookname = data[0]
      state.bookdata.author = data[1]
    },
    SET_BOOKCHAPTER: (state, data) => {
      state.bookdata.chapter = data
    }
  },
  actions: {
    updateState({ commit }, payload) {
      commit('SET_USER', payload.username)
      commit('SET_USERID', payload.userid)
    },
    deleteState({ commit }) {
      commit('SET_USER', '')
      commit('SET_USERID', '')
    },
    updateBookinfo({ commit }, payload) {
      commit('SET_BOOKCHAPTER', payload.chapter),
      commit('SET_BOOK', [payload.bookname,payload.author])
    }
  }
})
export default store
