<template>
  <div class="o-drawer u-highest o-drawer--right o-drawer--visible">
    <div class="c-card">
      <header class="c-card__header">
        <h2 class="c-heading">
          {{ tree.code }}
          <div class="c-heading__sub">{{ tree.common_name }}</div>
          <div class="c-heading__sub">{{ tree.scientific_name }}</div>
        </h2>
      </header>
      <div class="c-card__body">
        {{ tree }}
      </div>
      <footer class="c-card__footer">
        <div class="c-input-group">
          <button class="c-button c-button--block">Adoptar</button>
        </div>
      </footer>
    </div>
  </div>
</template>

<script>
export default {
  name: 'TreeAdmin',
  computed: {
      tree: async function() {
              return this.forest.__get__(this.$route.params.id)
      }
  },
  props: 
      ['forest']
}
</script>
