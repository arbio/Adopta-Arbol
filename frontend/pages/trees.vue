<template>
  <div id="container">
    <h1>Paso 1: Escoge tu Árbol</h1>

    <v-map id="mapita" ref="mapita" :zoom=17 :center="[-12.1716094, -69.3869664]">
      <v-tilelayer :url="url" :attribution="attribution"></v-tilelayer>
      <template v-for="(tree,index) in this.$store.state.view">
          <v-marker :ref="'mark' + tree.id" v-if="tree.coord_lat" :key="tree.id" :lat-lng="[tree.coord_lat, tree.coord_lon]" @l-click="pick(index)" :icon="right_icon(tree)">
              <v-popup :content="tree.common_name"></v-popup>
          </v-marker>
      </template>
    </v-map>

    <nuxt-child :key="$route.params.id"/>
    <adoption-cart></adoption-cart>

    <div id="carousel">
      <carousel-3d ref="treeExplorer" :width="400" :height="390" :loop="false"
          :on-slide-change="onSlideChanged"
          :display="5"
          :count="this.$store.state.view.length"
          inverse-scaling="400">
      <slide v-for="(tree, index) in this.$store.state.view" :key="tree.id" :index="index">
        <div class="c-card">
          <div class="c-card__item o-media">
            <div class="o-media__image o-media__image--top">
                <template v-if="!(tree.adopted)">
                    <a v-if="!in_cart(tree.id)" href="#" @click.stop="adopt(tree.id)">
                      <i class="fa fa-heart-o fa-3x heart-enabled" aria-hidden="true"></i>
                    </a>
                    <a v-if="in_cart(tree.id)" href="#" @click.stop="$store.commit('dropIntent', tree.id)">
                      <i class="fa fa-heart-o fa-3x blink" aria-hidden="true"></i>
                    </a>
                </template>
                <template v-if="tree.adopted">
                    <i class="fa fa-heart heart-disabled fa-3x" aria-hidden="true"></i>
                </template>
            </div>
            <div class="o-media__body">
                <h2 class="c-heading">{{ tree.common_name }}</h2>
              <p class="c-paragraph">
              {{ tree.family }}
              </p>
            </div>

          </div>
          <figure>
              <img width="200px" height="200px" class="o-image" :src="tree.thumbnail" />
              <div class="statuscaption" v-if="tree.adopted">
                  ¡Adoptado!
              </div>
              <div class="selectedcaption" v-if="in_cart(tree.id)">
                  ** Seleccionado **
              </div>
              <figcaption>
                  {{ tree.scientific_name }}
                  <div class="c-input-group u-display-block u-right">
                    <button style="width: 120px;" @click="select(tree.id)" class="c-button c-button--info">Detalles</button>
                  </div>
              </figcaption>
          </figure>
        </div>
      </slide>
      </carousel-3d>
    </div>

    <GlobalEvents @keyup.left="prevItem"
                  @keyup.right="nextItem"
                  @keyup.page-up="prevPage"
                  @keyup.page-down="nextPage" />
  </div>
</template>

<script>
import L from 'leaflet'
import Vue2Leaflet from 'vue2-leaflet'
import { Carousel3d, Slide } from 'vue-carousel-3d'
import GlobalEvents from 'vue-global-events'

// Build icon assets.
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.imagePath = ''
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('~/assets/censarbol.png'),
  iconUrl: require('~/assets/censarbol.png'),
  shadowUrl: require('~/assets/censarbol_sombra.png')
})

export default {
  name: 'tree-selector',
  components: {
    'adoption-cart': () => import('~/components/adoption-cart'),
    'v-map': Vue2Leaflet.Map,
    'v-tilelayer': Vue2Leaflet.TileLayer,
    'v-marker': Vue2Leaflet.Marker,
    'v-popup': Vue2Leaflet.Popup,
    'GlobalEvents': GlobalEvents,
    'carousel-3d': Carousel3d,
    'slide': Slide
  },
  mounted: function () {
    if (this.$refs.mapita !== undefined) {
      var map = this.$refs.mapita.mapObject
      map.removeControl(map.zoomControl)
      if (this.$store.state.page === undefined) {
        this.$store.commit('setPage', this.$route.query.page || 1)
      }
      this.$store.dispatch('getTrees')
    }
  },
  updated: function () {
    if (this.$refs.treeExplorer !== undefined) {
      this.$refs.treeExplorer.goSlide(this.$refs.treeExplorer.currentIndex)
    }
    if (this.$refs.mapita && this.$store.state.view[0]) {
      var map = this.$refs.mapita.mapObject
      var lat = this.current_tree.coord_lat
      var lon = this.current_tree.coord_lon
      map.panTo(new L.LatLng(Number(lat) - 0.0015, lon))
      map.setMaxZoom(17)
      map.keyboard.disable()
    }
  },
  computed: {
    current_tree: function () {
      return this.$store.state.view[this.$refs.treeExplorer.currentIndex]
    }
  },
  methods: {
    onSlideChanged: function () {
      if (this.$refs.mapita !== undefined) {
        var map = this.$refs.mapita.mapObject
        var markerRef = this.$refs['mark' + this.current_tree.id]
        if (markerRef !== undefined) {
          var marker = markerRef[0].mapObject
          marker.openPopup()
          marker._icon.style.outline = 'Lime dotted 2px'
          setTimeout(function () {
            if (marker._icon !== null) {
              marker._icon.style.outline = 'none'
            }
          }, 1000)
        }
        var lat = this.current_tree.coord_lat
        var lon = this.current_tree.coord_lon
        map.panTo(new L.LatLng(Number(lat) - 0.0015, lon))
      }
    },
    prevItem: function () {
      if (this.$refs.treeExplorer.isPrevPossible) {
        this.$refs.treeExplorer.goPrev()
      } else {
        if (this.$store.state.page !== 1) {
          this.prevPage()
          this.$refs.treeExplorer.goSlide(this.$refs.treeExplorer.count - 1)
        }
      }
    },
    nextItem: function () {
      if (this.$refs.treeExplorer.isNextPossible) {
        this.$refs.treeExplorer.goNext()
      } else {
        if (Number(this.$store.state.page) !== this.$store.state.num_pages) {
          this.$refs.treeExplorer.goSlide(0)
          this.nextPage()
        }
      }
    },
    prevPage: function () {
      if (this.$store.state.page > 1) {
        this.$store.commit('prevPage')
        this.$router.push({ query: { page: this.$store.state.page } })
        this.$store.dispatch('getTrees')
      }
    },
    nextPage: function () {
      if (this.$store.state.page < this.$store.state.num_pages) {
        this.$store.commit('nextPage')
        this.$router.push({ query: { page: this.$store.state.page } })
        this.$store.dispatch('getTrees')
      }
    },
    pick: function (id) {
      this.$refs.treeExplorer.goSlide(id)
    },
    select: function (id) {
      this.$router.push({
        path: '/trees/' + id,
        query: { page: this.$store.state.page } })
    },
    adopt: function (id) {
      this.$store.commit('intentAdopt', id)
    },
    in_cart: function (id) {
      return this.$store.state.cart.includes(id)
    },
    right_icon: function (tree) {
      if (tree.adopted) {
        let options = Object.assign({}, L.Icon.Default.prototype.options)
        options.iconUrl = require('~/assets/censarbol_adopted.png')
        let icon = L.icon(options)
        return icon
      } else {
        console.log(L.Icon.Default)
        console.log(L.Icon.Default.prototype.options)
        return L.icon.Default
      }
    }
  },
  data () {
    return {
      zoom: 17,
      center: [-12.1716094, -69.3869664],
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community',
      prevMarker: ''
    }
  }
}
</script>

<style scoped>

@import "~leaflet/dist/leaflet.css";

#container {
    text-align: center;
}

#mapita {
    z-index: -5000;
    position: fixed;
    top: 50px;
    left: 0px;
    right: 0px;
    bottom: 0px;
}

h1 {
    color: white;
}

.treelist {
    background-color: LightYellow;
}

.navbut {
    background-color: ForestGreen;
}

button {
    width: 20%;
}

.c-table__cell {
    display: block;
    text-align: center;
}

.heart-enabled {
    color: DeepPink;
}

.heart-disabled {
    color: Pink;
}

#carousel {
    position: fixed;
    bottom: 0px;
    left: 0px;
    width: 100%;
}

.carousel-3d-container figure {
  margin:0;
}

.carousel-3d-container .selectedcaption {
  font-weight: bold;
  position: absolute;
  background-color: DeepPink;
  opacity: 0.7;
  left: -20px;
  transform: rotate(-6deg);
  color: #fff;
  text-align: center;
  top: 150px;
  padding: 15px;
  min-width: 120%;
  box-sizing: border-box;
}

.carousel-3d-container .statuscaption {
  font-weight: bold;
  position: absolute;
  background-color: ForestGreen;
  opacity: 0.7;
  left: -20px;
  transform: rotate(7deg);
  color: #fff;
  text-align: center;
  top: 150px;
  padding: 15px;
  min-width: 120%;
  box-sizing: border-box;
}

.carousel-3d-container figcaption {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.5);
  color: #fff;
  bottom: 0;
  position: absolute;
  bottom: 0;
  padding: 15px;
  min-width: 100%;
  box-sizing: border-box;
}
@keyframes blink {
  0% { color: Deeppink; }
  50% { color: pink; transform: scale(1.2, 1.2) }
  100% { color: Deeppink; }
}
.blink {
  animation: blink 1s linear infinite;
}
</style>
