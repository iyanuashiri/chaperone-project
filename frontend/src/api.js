
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
  getQuizzes(){
    return this.execute('get', '/quizzes/')
  },
  createQuiz(quiz){
    return this.execute('post', '/quizzes/', quiz)
  },
  getQuiz(id){
    return this.execute('get', `/quizzes/${id}/`)
  },
  selectQuizOption(quizId, questionId, optionId) {
    return this.execute('post', `/quizzes/${quizId}/questions/${questionId}/select`, { option_id: optionId });
  },

  // --- Adaptive speed-bump game (math/logic) ---
  getChallenge(challengeType = 'math') {
    return this.execute('get', `/game/challenge/?challenge_type=${challengeType}`)
  },
  startGameSession(siteUrl = '') {
    return this.execute('post', '/game/session/', { source: 'frontend', site_url: siteUrl })
  },
  submitGameAnswer(sessionId, payload) {
    return this.execute('post', `/game/session/${sessionId}/answer/`, payload)
  },

  // --- Analytics ---
  getStatsSummary() {
    return this.execute('get', '/stats/summary')
  },
  getDailyStats(days = 30) {
    return this.execute('get', `/stats/daily?days=${days}`)
  },
  getSiteStats() {
    return this.execute('get', '/stats/sites')
  }
}