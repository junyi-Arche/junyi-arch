import axios from 'axios'
import qs from 'qs'

axios.defaults.timeout = 5000
axios.defaults.baseURL = '/api'

axios.interceptors.request.use(
  (config) => {
    if (config.method === 'post') {
      config.data = qs.stringify(config.data)
    }
    return config
  },
  (error) => {
    console.log('error params')
    return Promise.reject(error)
  }
)

axios.interceptors.response.use(
  (res) => {
    if (!res.data.success) {
      return Promise.resolve(res)
    }
    return res
  },
  (error) => {
    console.log('Network error')
    status = false
    return Promise.reject(error)
  }
)

export function fetchPost(url, params, headers = {}) {
  return new Promise((resolve, reject) => {
    if (status) {
      axios
        .post(url, params, { headers })
        .then(
          (response) => {
            resolve(response)
          },
          (err) => {
            reject(err)
          }
        )
        .catch((error) => {
          reject(error)
        })
    } else {
      reject(new Error("无法连接服务器"))
    }

  })
}

export function fetchGet(url, params) {
  return new Promise((resolve, reject) => {
    if (status) {
      axios
        .get(url, { params: params })
        .then(
          (response) => {
            resolve(response)
          },
          (err) => {
            reject(err)
          }
        )
        .catch((error) => {
          reject(error)
        })
    } else {
      reject(new Error("无法连接服务器"))
    }

  })
}
export let status = true

export default {
  fetchGet,
  fetchPost
}
