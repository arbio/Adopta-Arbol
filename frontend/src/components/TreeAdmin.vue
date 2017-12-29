<template>
  <div>
      <h1>{{ name }}</h1>
  </div>
</template>

<script>
export default {
  name: 'TreeAdmin',
  props: ['tree'],
  data: function() {
      return { "name": "Nombre" }
  },
}
</script>
