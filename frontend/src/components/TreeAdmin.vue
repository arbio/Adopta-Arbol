<template>
  <div>
      <h1>{{ tree.common_name }}</h1>
      {{ tree }}
  </div>
</template>

<script>
export default {
  name: 'TreeAdmin',
  computed: {
      tree: function() {
          var that = this
          return this.forest.trees.find(
                  function(tree){
                      return tree.id==that.$route.params.id
                  })
      }
  },
  props: 
      ['forest']
}
</script>
