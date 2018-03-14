<template>
<div>
  <div id="adoption_container">
    <div id="tree-list" v-if="$store.state.cart.length" class="o-drawer u-highest o-drawer--right o-drawer--visible">

     <div class="c-card">
       <header class="c-card__header">
          <div class="o-grid-text">{{ total }} árboles seleccionados</div>
       </header>
           <table class="treelist c-card__item c-table c-table--condensed">
             <thead class="c-table__head">
               <tr class="c-table__row c-table__row--heading">
                   <th class="c-table__cell">Especie</th>
                   <th class="c-table__cell">h</th>
               </tr>
             </thead>
             <tbody class="c-table__body">
               <tr class="c-table__row  c-table__row--clickable" v-for="id in this.$store.state.cart" @click="select(id)">
                 <td class="c-table__cell">{{ tree(id).common_name }}</td>
                 <td class="c-table__cell">{{ tree(id).height }} m</td>
               </tr>
             </tbody>
           </table>
       <footer class="c-card__footer">
          <nuxt-link to="/adopt">
            <a class="c-button c-button--block c-button--warning u-xlarge">Continuar</a>
          </nuxt-link>
       </footer>
     </div>

    </div>
  </div>
</div>
</template>

<script>
export default {
  methods: {
    tree: function (id) {
      return this.$store.state.trees[id]
    },
    select: function (id) {
      this.$router.push({
        path: '/trees/' + id,
        query: { page: this.$store.state.page } })
    }
  },
  computed: {
    total: function () {
      return this.$store.state.cart.length
    }
  }
}
</script>

<style scoped>
#tree-list {
    position: fixed;
    height: auto;
}
.c-table__cell {
    display: block;
    text-align: center;
}
.blink {
  color: Deeppink;
}
</style>
