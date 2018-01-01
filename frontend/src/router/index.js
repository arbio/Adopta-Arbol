import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
  { path: '/ver', component: 'TreeList', props: true },
  { path: '/cart', component: 'Cart' },
  { path: '/tree/:id', component: 'TreeAdmin', props: true },
  { path: '*', component: 'NotFound' }
]
const routes = routerOptions.map(route => {
  return {
    ...route,
    component: () => import(`@/components/${route.component}.vue`)
  }
})
Vue.use(Router)
export default new Router({
  routes,
  mode: 'history'
})
