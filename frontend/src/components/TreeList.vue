<template>
  <div>
    <h1>Paso 1: Escoge tu Árbol</h1>
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
          <tr class="c-table__row" v-for="tree in forest.trees">
              <td class="c-table__cell">{{ tree.id }}</td>
              <td class="c-table__cell">{{ tree.code }}</td>
              <td class="c-table__cell">{{ tree.common_name }}</td>
              <td class="c-table__cell">{{ tree.diameter }} cm</td>
              <td class="c-table__cell">{{ tree.height }} m</td>
              <td class="c-table__cell">
                  <router-link :forest="tree" :to="{ path: 'tree/'+tree.id}">Ver</router-link>
              </td>
          </tr>
        </tbody>
    </table>
    </div>
    <p>
      <button class="navbut c-button c-button--success u-high" @click="prev">« Anterior</button>&nbsp;
      <button class="navbut c-button c-button--success u-high" @click="next">Siguiente »</button>
    </p>
  </div>
</template>

<script>
export default {
  name: 'TreeList',
  props: ['forest', 'page'],
  methods: {
      prev: function () {
        this.$parent.prevPage()
        this.$router.push({ query: { page: forest.page }})
      },
      next: function () {
        this.$parent.nextPage()
        this.$router.push({ query: { page: forest.page }})
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
