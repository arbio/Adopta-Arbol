<template>
  <div>
    <h1>Paso 1: Escoge tu Árbol</h1>
    <p>
      <button class="navbut c-button c-button--success u-high" @click="prev">« anterior</button>&nbsp;
      <button class="navbut c-button c-button--success u-high" @click="next">siguiente »</button>
    </p>
    <div id="showcase" class="o-container o-container--large">
    <table class="treelist c-table u-high">
        <thead class="c-table__head">
          <tr class="c-table__row c-table__row--heading">
              <th class="c-table__cell">Adoptar</th>
              <th class="c-table__cell">Código</th>
              <th class="c-table__cell">Especie</th>
              <th class="c-table__cell">⌀</th>
              <th class="c-table__cell">h</th>
          </tr>
        </thead>
        <tbody class="c-table__body">
          <tr class="c-table__row c-table__row--clickable" v-for="tree in this.$store.state.view" @click="select(tree.id)">
              <td class="c-table__cell">
                <a v-if="!in_cart(tree.id)" href="#" @click.stop="adopt(tree.id)">
                  <i class="fa fa-life-ring" aria-hidden="true"></i>
                </a>
                <a v-if="in_cart(tree.id)" href="#" @click.stop="$store.commit('dropIntent', tree.id)">
                  <i class="fa fa-minus" aria-hidden="true"></i>
                </a>
              </td>
              <td class="c-table__cell">{{ tree.code }}</td>
              <td class="c-table__cell">{{ tree.common_name }}</td>
              <td class="c-table__cell">{{ tree.diameter }} cm</td>
              <td class="c-table__cell">{{ tree.height }} m</td>
          </tr>
        </tbody>
    </table>
    </div>
    <nuxt-child :key="$route.params.id"/>
    <adoption-cart></adoption-cart>
  </div>
</template>

<script>
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
  }
}
</script>

<style scoped>
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

</style>
