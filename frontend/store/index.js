import Vue from 'vue'
import Vuex from 'vuex'

const createStore = () => {
  return new Vuex.Store({
    state: {
      counter: 0,
      total: '...',
      trees: {},
      view: [],
      num_pages: 1,
      page: undefined,
      cart: [],
      adoptions: [],
      years: 3
    },
    getters: {
      totalCost: function (state) {
        var cost = 0
        for (var id of state.cart) {
          cost = cost + state.trees[id].cost
        }
        return cost * state.years
      }
    },
    actions: {
      async getTrees ({ commit, state }) {
        let { data } = await this.$axios.get('trees',
          {'params': {
            'results_per_page': 9,
            'page': state.page}}
        )
        commit('setView', data)
      },
      async getTree ({ commit, state }, id) {
        let { data } = await this.$axios.get('trees/' + id)
        commit('setTree', data)
      },
      async postAdopt ({ commit, state, getters }) {
        let { data } = await this.$axios.post('trees/adopt',
          {'params': {
            'trees': state.cart,
            'years': state.years,
            'amount': getters.totalCost
          }}
        )
        commit('adoptResult', data)
      }
    },
    mutations: {
      adoptResult (state, result) {
        state.adoptions.push(result)
      },
      setTree (state, tree) {
        Vue.set(state.trees, tree.id, tree)
      },
      setView (state, data) {
        state.view = data.objects
        state.total = data.num_results
        state.num_pages = data.total_pages
        for (var id in state.view) {
          var tree = state.view[id]
          if (!(tree.id in state.trees)) {
            Vue.set(state.trees, tree.id, tree)
          }
        }
      },
      setPage (state, page) {
        state.page = page
      },
      nextPage (state) {
        state.page++
      },
      prevPage (state) {
        state.page--
      },
      setYears (state, years) {
        state.years = years
      },
      intentAdopt (state, id) {
        if (!(state.cart.includes(id))) {
          state.cart.push(id)
        }
      },
      dropIntent (state, id) {
        if (state.cart.includes(id)) {
          state.cart.splice(state.cart.indexOf(id), 1)
        }
      }
    }
  })
}

export default createStore
