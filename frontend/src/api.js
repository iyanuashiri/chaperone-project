
import axios from 'axios'

const client = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  json: true,
})

export default {
  async execute (method, resource, data) {
    let accessToken = localStorage.getItem('accessToken')
    return client({
      method,
      url: resource,
      data,
      headers: {
        Authorization: `Bearer ${accessToken}`
      }
    }).then(req => {
      return req.data
    })
  },
  
  getAssociations() {
    return this.execute('get', '/associations/')
  },
  getAssociation(id){
    return this.execute('get', `/associations/${id}/`)
  },
  updateCorrectAssociation(id) {
    return this.execute('put', `/associations/${id}/correct/`)
  },
  updateIncorrectAssociation(id) {
    return this.execute('put', `/associations/${id}/incorrect/`)
  },
  getUrls() {
    return this.execute('get', '/urls/')
  },
  createUrl(url){
    return this.execute('post', '/urls/', url)
  },
  deleteUrl(id){
    return this.execute('delete', `/urls/${id}/`)
  },
}