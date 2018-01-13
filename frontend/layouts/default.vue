<template>
  <div id="app">
    <ul id="nav" class="c-nav c-nav--inline c-nav--top u-high">

    <router-link to="/">
    <span style="color:white" class="c-nav__item">Adopta</span>
    </router-link>

    <span class="c-nav__content u-window-box--none">
      <img class="o-image" src="~/assets/censarbol.png">
    </span>

    <router-link to="/">
    <span style="color:white" class="c-nav__item">Árbol</span>
    </router-link>

    <router-link to="/trees">
    <span id="infobox" class="c-nav__item c-nav__item--right u-xsmall">
        {{ this.$store.state.total }} árboles</span>
    </router-link>
    </ul>

    <br>

    <nuxt/>
  </div>
</template>

<style>
#app {
  font-family: 'Noto Mono', 'Lucida Console', Monaco, monospace;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  text-align: center;
  color: #2c3e50;
  margin-top: 60px;
  /* background: no-repeat center center;
  background-image: url("/static/images/bg-index.jpg"); */
}

body {
  margin-top: 70px;
  background: repeat-y center center radial-gradient(circle, white, Peru);
  overflow:hidden;
}

.o-drawer {
    z-index: 100;
    padding-top: 60px;
}

#nav {
    background-color: #93c54b;
    border-bottom: 1px solid black;
}

#infobox {
    position: absolute;
    right: 0px;
}
</style>
