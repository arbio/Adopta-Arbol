import Vue from 'vue'
import Router from 'vue-router'
const routerOptions = [
  { path: '/', component: 'Home' },
  { path: '/about', component: 'About' },
  { path: '/tree/:id', component: 'Tree' },
  { path: '/cart', component: 'Cart' },
  { path: '/admin/trees', component: 'TreeList', props: true },
  { path: '/admin/trees/:id', component: 'TreeAdmin', props: true },
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
