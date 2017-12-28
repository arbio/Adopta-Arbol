import Vue from 'vue'
import App from './App'
import router from './router'
import iLikePython from './test'

Vue.config.productionTip = false

iLikePython()

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
