<template>
  <div id="app">
    <ul id="nav" class="c-nav c-nav--inline c-nav--top u-high">

    <span class="c-nav__item">Adopta</span>

    <span class="c-nav__content u-window-box--none">
      <img class="o-image" src="./assets/censarbol.png">
    </span>

    <span class="c-nav__item">Árbol</span>

    <router-link to="/admin/trees">
    <span class="c-nav__item c-nav__item--right u-xsmall">
        {{ total }} árboles</span>
    </router-link>
    </ul>

    <br>

    <router-view :forest="forest"/>
  </div>
</template>

<script>
import Forest from './forest'

export default {
  name: 'app',
  data: () => ( { forest: [],
                  total: 'N/A' } ),
  watch: {
    '$route' (to, from) {
      if (to.query.page === undefined && from.query.page != undefined) {
        forest.page = 1
        forest.py_update()
      }
    }
  },
  mounted: function() {
    this.init()
  },
  methods: {
    init() {
        setTimeout( () => {
      window.forest = Forest(this.fetchData, this.$route.query.page)
        }, 300)
    },
    fetchData() {
      this.forest = forest.trees
      this.total = forest.total
    },
    prevPage() {
      forest.prevPage()
    },
    nextPage() {
      forest.nextPage()
    }
  }
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
    background-color: Peru;
}

#nav {
    background-color: #93c54b;
    border-bottom: 1px solid black;
}
</style>
