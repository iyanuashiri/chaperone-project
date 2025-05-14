
import axios from 'axios'

const client = axios.create({
  baseURL: 'http://127.0.0.1:8000/api/v1/',
  json: true,
})

export default {
  async execute (method, resource, data) {
    // let accessToken = localStorage.getItem('authToken')
    let accessToken = '6f346cef273f199002b9495ae16e8ce6193b145f'

    return client({
      method,
      url: resource,
      data,
      headers: {
        Authorization: `Token ${accessToken}`
      }
    }).then(req => {
      return req.data
    })
  },
  createAssociation(data) {
    return this.execute('post', '/associations/', data)
  },
  getAssociations() {
    return this.execute('get', '/associations/')
  },
  getAssociation(id){
    return this.execute('get', `/associations/${id}/`)
  },
  updateAssociation(id, data) {
    return this.execute('put', `/associations/${id}/`, data)
  },

}