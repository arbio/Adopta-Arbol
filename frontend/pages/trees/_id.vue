<template>
<div v-if="tree">
  <div class="c-overlay c-overlay--visible"></div>
    <div class="o-modal">
      <div class="c-card">
        <header class="c-card__header">
          <button @click="closeTree()" type="button" class="c-button c-button--close">&times;</button>
          <h1 class="c-heading">{{ tree.code }}</h1>
          <div class="c-heading__sub">{{ tree.height }}m de altura</div>
          <div class="c-heading__sub">{{ tree.diameter }}cm de diametro</div>
        </h2>
        </header>
        <div class="c-card__body">
          <div class="c-card__item c-card__item--info o-media">
            <div class="o-media__body">
              <h2 class="c-heading">{{ tree.scientific_name }}<br><span class="c-heading__sub">{{ tree.common_name }}</span></h2>
              <h2 class="c-heading"><br><span class="c-heading__sub">Notas</span></h2>
              <p class="c-paragraph">
                {{ tree.notes }}
              </p>
              <h2 class="c-heading"><br><span class="c-heading__sub">Observaciones</span></h2>
              <p class="c-paragraph">
                {{ tree.observation }}
              </p>
            </div>
            <div class="o-grid o-grid--wrap o-grid--demo">
              <div v-for="photo in tree.photos" class="o-grid__cell o-grid__cell--width-50">
                <div class="o-grid-text">
                    <img :src="'data:image/jpeg;base64,' + photo" />
                </div>
              </div>
            </div>
          </div>
          <br>
          <div class="c-card" v-if="tree.description">
            <header class="c-card__header">
              <h2 class="c-heading">{{ tree.common_name }}</h2>
            </header>
            <div v-html="tree.description" class="c-card__body">
            </div>
          </div>
        </div>
        <footer class="c-card__footer">
        <div class="c-input-group u-display-block u-right">
          <button @click="closeTree()" type="button" class="c-button c-button--brand">Cerrar</button>&nbsp;
          <button v-if="!in_cart(tree.id)" @click="adopt(tree.id)" class="c-button c-button--warning u-high">Adoptar</button>
          <button v-if="in_cart(tree.id)" @click="$store.commit('dropIntent', tree.id)" class="c-button">No deseo adoptar este árbol</button>
        </div>
        </footer>
      </div>
    </div>
</div>
</template>

<script>
export default {
  validate ({ params }) {
    return !isNaN(+params.id)
  },
  created: function () {
    if (!(this.tree)) {
      this.$store.dispatch('getTree', this.$route.params.id)
    } else if (this.tree['description'] === undefined) {
      this.$store.dispatch('getTree', this.$route.params.id)
    }
  },
  computed: {
    tree: function () {
      return this.$store.state.trees[this.$route.params.id]
    }
  },
  methods: {
    in_cart: function (id) {
      return this.$store.state.cart.includes(id)
    },
    adopt: function (id) {
      this.$store.commit('intentAdopt', id)
      this.closeTree()
    },
    closeTree: function () {
      this.$router.push({
        path: '/trees',
        query: { page: this.$store.state.page } })
    }
  }
}
</script>

<style scoped>
</style>
