<template>
  <div>
    <h1>Paso 1: Escoge tu Árbol</h1>
    <p>
      <button class="navbut c-button c-button--success u-high" @click="prev">« anterior</button>&nbsp;
      <button class="navbut c-button c-button--success u-high" @click="next">siguiente »</button>
    </p>
    <div id="showcase">
    <table class="treelist c-table u-high">
        <thead class="c-table__head">
          <tr class="c-table__row c-table__row--heading">
              <th class="c-table__cell">ID</th>
              <th class="c-table__cell">Código</th>
              <th class="c-table__cell">Especie</th>
              <th class="c-table__cell">⌀</th>
              <th class="c-table__cell">h</th>
              <th class="c-table__cell">Acciones</th>
          </tr>
        </thead>
        <tbody class="c-table__body">
          <tr class="c-table__row" v-for="tree in this.$store.state.view">
              <td class="c-table__cell">{{ tree.id }}</td>
              <td class="c-table__cell">{{ tree.code }}</td>
              <td class="c-table__cell">{{ tree.common_name }}</td>
              <td class="c-table__cell">{{ tree.diameter }} cm</td>
              <td class="c-table__cell">{{ tree.height }} m</td>
              <td class="c-table__cell">
                  <nuxt-link :to="{ path: '/trees/'+tree.id }">Ver</nuxt-link>
              </td>
          </tr>
        </tbody>
    </table>
    </div>
    <nuxt-child :key="$route.params.id"/>
    <p>
      <button class="navbut c-button c-button--success u-high" @click="prev">« anterior</button>&nbsp;
      <button class="navbut c-button c-button--success u-high" @click="next">siguiente »</button>
    </p>
  </div>
</template>

<script>
export default {
  mounted: function () {
    if (this.$store.state.page === undefined) {
      this.$store.commit('setPage', this.$route.query.page || 1)
    }
    this.$store.dispatch('getTrees')
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
    }
  }
}
</script>

<style>
.navbut {
    background-color: ForestGreen;
}

.treelist {
    border: 1px solid black;
}

button {
    width: 20%;
}

table {
    width: 100%;
    background-color: LightYellow;
}

#showcase {
    width: 80%;
    margin: auto;
}
</style>
