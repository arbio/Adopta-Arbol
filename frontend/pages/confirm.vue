<template>
  <div id="container">
    <h1>Paso Final: Selecciona medio de pago</h1>
    <p>
    Para concretar tu adopción y emitir tu certificado es necesario recibir una donación.
    </p>
    <div class="c-card o-container o-container--xsmall">
      <header class="c-card__item u-centered">
        <h1 class="c-heading">{{ $store.getters.totalCost }} USD</h1>
      </h2>
      </header>
    </div>
    <p class="c-paragraph">
      <object id="svg1" width="812" height="580" data="/cert/image.svg" type="image/svg+xml"></object>
    </p>
    <p>
    Elige a continuación:
    </p>
    <p>
    <button @click="$store.dispatch('postAdopt')" class="c-button c-button--info c-button--block u-large">Emitir certificado de prueba</button>
    </p>
  </div>
</template>

<script>
export default {
}
</script>
