<template>
<div v-if="tree">
  <div class="c-overlay c-overlay--visible" @click="closeTree()"></div>
    <div class="o-modal" v-if="tree.photos!==undefined">
        <header class="c-card__header c-card__item--info">
          <button @click="closeTree()" type="button" class="c-button c-button--close">&times;</button>

          <div v-if="!(currentPic)"  style="position: absolute; top: 30px; right: 50px" >
            <button v-if="!in_cart(tree.id) && !(tree.adopted)" @click="adopt(tree.id)" class="c-button c-button--warning u-high">Adoptar</button>
            <button v-if="in_cart(tree.id)" @click="$store.commit('dropIntent', tree.id)" class="c-button">No deseo adoptar este árbol</button>
          </div>
          <div v-if="currentPic"  style="position: absolute; top: 30px; right: 50px" >
            <button @click="closePic()" type="button" class="c-button c-button--success">Volver</button>&nbsp;
          </div>

          <h1 class="c-heading">{{ tree.common_name }}</h1>
          <div class="c-heading__sub">{{ tree.height }}m de altura</div>
          <div class="c-heading__sub">{{ tree.diameter }}cm de diametro</div>
          <br>

        </header>

        <div  v-if="!(currentPic) && tree.description" class="o-panel-container" style="height: 80vh">
          <div class="o-panel" style="height: 100%">

            <carousel-3d ref="photoExplorer" :space="209" :controls-visible="true"
                :disable3d="true" :width="200" :height="200" :loop="true">
            <slide v-for="(photo, url) of tree.photos" :key="url" :index="Object.getOwnPropertyNames(tree.photos).indexOf(url)">
              <a @click="show(url)">
                  <img height="200px" width="200px" :src="'data:image/jpeg;base64,' + photo" />
              </a>
            </slide>
            </carousel-3d>

            <h2 class="c-heading">{{ tree.scientific_name }}</h2>
            <h2 class="c-heading u-medium c-text--mono">{{ tree.family }}</h2>
            <div v-html="tree.description" class="c-card__body">
            </div>
          </div>
        </div>

        <div class="o-panel-container" v-if="currentPic" style="height: 80vh">
          <div class="o-panel">
            <img class="o-image" :src="currentPic" @click="closePic()" />
          </div>
        </div>

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
