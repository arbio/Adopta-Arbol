import Vuex from 'vuex'

const createStore = () => {
  return new Vuex.Store({
    state: {
      counter: 0,
      total: '...',
      trees: {},
      view: [],
      num_pages: 1,
      page: 1,
      cart: []
    },
    actions: {
      async getTrees ({ commit, state }) {
        let { data } = await this.$axios.get('trees',
          {'params': {
            'results_per_page': 12,
            'page': state.page}}
        )
        commit('setView', data)
      }
    },
    mutations: {
      setView (state, data) {
        state.view = data.objects
        state.total = data.num_results
        state.num_pages = data.total_pages
        for (var id in state.view) {
          var tree = state.view[id]
          if (!(tree.id in state.trees)) {
            state.trees[tree.id] = tree
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
      }
    }
  })
}

export default createStore
