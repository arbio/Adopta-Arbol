<template>
  <div>
    <h1>Paso 1: Escoge tu Árbol</h1>
    <p>
      <button class="navbut c-button c-button--success u-high" @click="prev">« anterior</button>&nbsp;
      <button class="navbut c-button c-button--success u-high" @click="next">siguiente »</button>
    </p>
    <div id="showcase" class="o-container o-container--large">

    <div id="tree-drawer" class="o-drawer u-highest o-drawer--right o-drawer--visible">
        <table class="treelist c-table u-high">
            <thead class="c-table__head">
              <tr class="c-table__row c-table__row--heading">
                  <th class="c-table__cell">Adoptar</th>
                  <th class="c-table__cell">Especie</th>
              </tr>
            </thead>
            <tbody class="c-table__body">
              <tr class="c-table__row c-table__row--clickable" v-for="tree in this.$store.state.view" @click="select(tree.id)">
                  <td class="c-table__cell">
                    <a v-if="!in_cart(tree.id)" href="#" @click.stop="adopt(tree.id)">
                      <i class="fa fa-heart" aria-hidden="true"></i>
                    </a>
                    <a v-if="in_cart(tree.id)" href="#" @click.stop="$store.commit('dropIntent', tree.id)">
                      <i class="fa fa-times" aria-hidden="true"></i>
                    </a>
                  </td>
                  <td class="c-table__cell">{{ tree.common_name }}</td>
              </tr>
            </tbody>
        </table></div>
    </div>

    <v-map id="mapita" ref="mapita" :zoom=17 :center="[-12.1716094, -69.3869664]">
      <v-tilelayer :url="url" :attribution="attribution"></v-tilelayer>
      <v-marker v-for="tree in this.$store.state.view" :key="tree.id" :lat-lng="[tree.coord_lat, tree.coord_lon]" @l-click="select(tree.id)"></v-marker>
    </v-map>

    <nuxt-child :key="$route.params.id"/>
    <adoption-cart></adoption-cart>
  </div>
</template>

<script>
import Vue from 'vue'
import L from 'leaflet'
import Vue2Leaflet from 'vue2-leaflet'

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
    'adoption-cart': () => import('~/components/adoption-cart')
  },
  mounted: function () {
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
</style>
