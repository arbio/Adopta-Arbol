<template>
  <div id="container">
    <h1>Paso 1: Escoge tu Árbol</h1>
    <p>
      <button class="navbut c-button c-button--success u-high" @click="prev">« anterior</button>&nbsp;
      <button class="navbut c-button c-button--success u-high" @click="next">siguiente »</button>
    </p>
    <div id="showcase" class="o-container o-container--large">

    </div>

    <v-map id="mapita" ref="mapita" :zoom=17 :center="[-12.1716094, -69.3869664]">
      <v-tilelayer :url="url" :attribution="attribution"></v-tilelayer>
      <template v-for="tree in this.$store.state.view">
      <v-marker v-if="tree.coord_lat" :key="tree.id" :lat-lng="[tree.coord_lat, tree.coord_lon]" @l-click="select(tree.id)"></v-marker>
      </template>
    </v-map>

    <nuxt-child :key="$route.params.id"/>
    <adoption-cart></adoption-cart>

    <div id="carousel">
      <carousel-3d :width="300" :height="390" :loop="true"
          :controls-visible="true" :controls-prev-html="'&#10092;'" :controls-next-html="'&#10093;'" 
          :controls-width="30" :controls-height="60"
          :display="this.$store.state.view.length"
          :count="this.$store.state.total">
      <slide v-for="(tree, index) in this.$store.state.view" :key="tree.id" :index="index">
        <div class="c-card">
          <div class="c-card__item o-media">
            <div class="o-media__image o-media__image--top">
                <a v-if="!in_cart(tree.id)" href="#" @click.stop="adopt(tree.id)">
                  <i class="fa fa-heart" aria-hidden="true"></i>
                </a>
                <a v-if="in_cart(tree.id)" href="#" @click.stop="$store.commit('dropIntent', tree.id)">
                  <i class="fa fa-times" aria-hidden="true"></i>
                </a>
            </div>
            <div class="o-media__body">
                <h2 class="c-heading">{{ tree.common_name }}</h2>
              <p class="c-paragraph">
              {{ tree.family }}
              </p>
            </div>

          </div>
          <figure>
              <a @click="select(tree.id)">
                  <img class="o-image" :src="tree.thumbnail" />
              </a>
              <figcaption>
                  {{ tree.scientific_name }}
              </figcaption>
          </figure>
        </div>

      </slide>
      </carousel-3d>
    </div>

    <GlobalEvents @keyup.left="prev"
                  @keyup.right="next" />
  </div>
</template>

<script>
import Vue from 'vue'
import L from 'leaflet'
import Vue2Leaflet from 'vue2-leaflet'
import { Carousel3d, Slide } from 'vue-carousel-3d'
import GlobalEvents from 'vue-global-events'

// Build icon assets.
delete L.Icon.Default.prototype._getIconUrl
L.Icon.Default.imagePath = ''
L.Icon.Default.mergeOptions({
  iconRetinaUrl: require('leaflet/dist/images/marker-icon-2x.png'),
  iconUrl: require('leaflet/dist/images/marker-icon.png'),
  shadowUrl: require('leaflet/dist/images/marker-shadow.png')
})

Vue.component('v-map', Vue2Leaflet.Map)
Vue.component('v-tilelayer', Vue2Leaflet.TileLayer)
Vue.component('v-marker', Vue2Leaflet.Marker)

export default {
  components: {
    'adoption-cart': () => import('~/components/adoption-cart'),
    GlobalEvents,
    Carousel3d,
    Slide
  },
  mounted: function () {
    var map = this.$refs.mapita.mapObject
    map.removeControl(map.zoomControl)
    if (this.$store.state.page === undefined) {
      this.$store.commit('setPage', this.$route.query.page || 1)
    }
    this.$store.dispatch('getTrees')
  },
  updated: function () {
    if (this.$refs.mapita && this.$store.state.view[0]) {
      var map = this.$refs.mapita.mapObject
      var lat = this.$store.state.view[0].coord_lat
      var lon = this.$store.state.view[0].coord_lon
      map.panTo(new L.LatLng(lat, lon))
      map.setMaxZoom(17)
    }
  },
  methods: {
    prev: function () {
      if (this.$store.state.page > 1) {
        this.$store.commit('prevPage')
        this.$router.push({ query: { page: this.$store.state.page } })
        this.$store.dispatch('getTrees')
      }
    },
    next: function () {
      if (this.$store.state.page < this.$store.state.num_pages) {
        this.$store.commit('nextPage')
        this.$router.push({ query: { page: this.$store.state.page } })
        this.$store.dispatch('getTrees')
      }
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
    }
  },
  data () {
    return {
      zoom: 17,
      center: [-12.1716094, -69.3869664],
      url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
      attribution: 'Tiles &copy; Esri &mdash; Source: Esri, i-cubed, USDA, USGS, AEX, GeoEye, Getmapping, Aerogrid, IGN, IGP, UPR-EGP, and the GIS User Community'
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

#tree-drawer {
    top: 60px;
    height: auto;
    opacity: 0.5;
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

.fa-heart {
    color: DeepPink;
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

.carousel-3d-container figcaption {
  position: absolute;
  background-color: rgba(0, 0, 0, 0.5);
  color: #fff;
  bottom: 0;
  position: absolute;
  bottom: 0;
  padding: 15px;
  font-size: 12px;
  min-width: 100%;
  box-sizing: border-box;
}
</style>
