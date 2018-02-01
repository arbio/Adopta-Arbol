<template>
<div>
  <div id="adoption_container">
    <div id="tree-list" v-if="$store.state.cart.length" class="o-drawer u-highest o-drawer--bottom o-drawer--visible">
     <div class="c-card">
       <header class="c-card__header">
         <div class="o-grid">
            <div class="o-grid__cell o-grid__cell--width-50">
              <div class="o-grid-text">{{ total }} árboles seleccionados</div>
            </div>
            <div class="o-grid__cell o-grid__cell--width-50">
              <div class="o-grid-text">
              <nuxt-link to="/adopt">
                <a class="c-button c-button--block c-button--warning u-xlarge">Continuar</a>
              </nuxt-link>
              </div>
            </div>
         </div>
       </header>
       <br>
       <table class="treelist c-card__item c-table c-table--condensed u-high">
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
           <tr class="c-table__row  c-table__row--clickable" v-for="id in this.$store.state.cart" @click="select(id)">
             <td class="c-table__cell"><a href="#" @click.stop="$store.commit('dropIntent', tree(id).id)">
               <i class="fa fa-times" aria-hidden="true"></i>
             </a></td>
             <td class="c-table__cell">{{ tree(id).code }}</td>
             <td class="c-table__cell">{{ tree(id).common_name }}</td>
             <td class="c-table__cell">{{ tree(id).diameter }} cm</td>
             <td class="c-table__cell">{{ tree(id).height }} m</td>
           </tr>
         </tbody>
       </table>
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
#adoption_container {
    position: fixed;
    bottom: 0px;
    left: 0%;
    right: 0%;
    z-index: 100;
    margin-left: 0px;
}
#tree-profile {
    position: fixed;
    padding-top: 60px;
}    
#tree-list {
    position: fixed;
    width: 50vw;
    margin-left: 25vw;
}
.c-table__cell {
    display: block;
    text-align: center;
}
</style>
