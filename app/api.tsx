import axios from 'axios'

const api = axios.create({
    baseURL: 'http://172.161.85.236:8012',
})

export default api;