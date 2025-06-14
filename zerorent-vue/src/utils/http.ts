import axios from 'axios'

const instance = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000',
  timeout: 10000,
  headers: { 'Content-Type': 'application/json' }
})

// 请求拦截器
instance.interceptors.request.use(config => {
  // 可在此添加token等
  return config
})

// 响应拦截器
instance.interceptors.response.use(
  response => response.data,
  error => {
    return Promise.reject(error.response?.data || error.message)
  }
)

export default instance
