<template>
  <div id="app">
    <img src="./assets/censarbol.png">
    <router-view/>
        {{ trees }}
  </div>
</template>

<script>

import axios from 'axios'

window.requests = axios.create({
    baseURL: 'http://localhost:5000/api'
})

export default {
  name: 'app',
  data: () => ( { trees : window.forest } )
}
</script>

<style>
#app {
  font-family: 'Avenir', Helvetica, Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
}

body {
    background-color: Peru;
}
</style>
