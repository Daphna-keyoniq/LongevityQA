import axios from 'axios'

const api = axios.create({
    baseURL: 'http://172.161.85.236:8011',
})

export default api;