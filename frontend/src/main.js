import Vue from 'vue'
import App from './App'
import router from './router'
import I_like_python from './test'

Vue.config.productionTip = false

/* eslint-disable no-new */
new Vue({
  el: '#app',
  router,
  render: h => h(App)
})

I_like_python()
