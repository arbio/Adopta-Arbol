<template>
<div v-if="tree">
  <div class="c-overlay c-overlay--visible" @click="closeTree()"></div>
    <div class="o-modal" v-if="tree.photos!==undefined">
      <div class="c-card">
        <header class="c-card__header c-card__item--info">
          <button @click="closeTree()" type="button" class="c-button c-button--close">&times;</button>
          <h1 class="c-heading">{{ tree.code }}</h1>
          <div class="c-heading__sub">{{ tree.height }}m de altura</div>
          <div class="c-heading__sub">{{ tree.diameter }}cm de diametro</div>
          <br>
        </header>

        <div class="c-card" v-if="!(currentPic) && tree.description">
          <div class="o-panel-container" style="height: 65vh">
            <div class="o-panel">

            <div class="o-grid o-grid--wrap o-grid--demo">
              <header class="c-card__header">
                <h2 class="c-heading u-center-block__content">{{ tree.common_name }}</h2>
              </header>
            </div>

              <carousel-3d ref="photoExplorer" :space="209" :controls-visible="true"
                  :disable3d="true" :width="200" :height="200" :loop="true">
              <slide v-for="(photo, url) of tree.photos" :key="url" :index="Object.getOwnPropertyNames(tree.photos).indexOf(url)">
                <a @click="show(url)">
                    <img height="200px" width="200px" :src="'data:image/jpeg;base64,' + photo" />
                </a>
              </slide>
              </carousel-3d>

              <div v-html="tree.description" class="c-card__body">
              </div>
            </div>
          </div>
        </div>

        <div class="o-panel-container" v-if="currentPic" style="height: 70vh">
          <div class="o-panel">
            <img class="o-image" :src="currentPic" @click="closePic()" />
          </div>
        </div>
        <footer class="c-card__footer">

        <div class="o-grid o-grid--demo">
          <div class="o-grid__cell">
            <div v-if="!(currentPic)" class="c-input-group u-display-block u-left">
              <h2 class="c-heading u-medium c-text--mono">{{ tree.scientific_name }}</h2>
            </div>
          </div>
          <div class="o-grid__cell">
            <div v-if="!(currentPic)" class="c-input-group u-right">
              <button @click="closeTree()" type="button" class="c-button c-button--brand">Cerrar</button>&nbsp;
              <button v-if="!in_cart(tree.id) && !(tree.adopted)" @click="adopt(tree.id)" class="c-button c-button--warning u-high">Adoptar</button>
              <button v-if="in_cart(tree.id)" @click="$store.commit('dropIntent', tree.id)" class="c-button">No deseo adoptar este árbol</button>
            </div>
            <div v-if="currentPic" class="c-input-group u-right">
              <button @click="closePic()" type="button" class="c-button c-button--success">Volver</button>&nbsp;
              <button @click="adopt(tree.id)" class="c-button c-button--warning u-high">Adoptar</button>
            </div>
          </div>
        </div>

        </footer>
      </div>
    </div>
</div>
</template>

<script>
import { Carousel3d, Slide } from 'vue-carousel-3d'
export default {
  validate ({ params }) {
    return !isNaN(+params.id)
  },
  name: 'tree-profile',
  data: () => ({
    currentPic: undefined
  }),
  components: {
    'carousel-3d': Carousel3d,
    'slide': Slide
  },
  updated: function () {
    if (this.$refs.photoExplorer !== undefined) {
      this.$refs.photoExplorer.goSlide(this.$refs.photoExplorer.currentIndex)
    }
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
    },
    canadopt: function (tree) {
      return !(this.in_cart(tree.id)) && !(tree.adopted)
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
    },
    closePic: function () {
      this.currentPic = undefined
    },
    show: function (url) {
      this.currentPic = '/pictures/' + url
    }
  }
}
</script>

<style scoped>
.o-modal {
    height: 92%;
}
</style>
