<template>
  <div class="u-centered">
    <div class="c-card">
      <div class="c-card__item c-card__item--info">
      <h2>  banner  </h2>
      </div>
    </div>

    <div class="c-card">
      <div class="c-card__item c-card__item--success c-card__item--divider">
      <h2>Árboles certificados: {{ this.$store.state.total }}</h2>
      <h2>Árboles adoptados: {{ this.$store.state.currently_adopted }}</h2>
      <nuxt-link to="/trees" class="c-button c-button--warning u-higher">¡Ayúdanos a llegar a {{ this.$store.state.target }}!</nuxt-link>
      <br><br>
      </div>
      <div class="c-card__item c-card__item--error c-card__item--divider">
      <h4 class="text-center">Adopta árboles nativos amazónicos certificados por &nbsp;<a class="lead label label-large label-success" data-toggle="popover" data-title="Arbio realiza el censo de verificación del buen estado de los árboles para que sean 'certificados'." data-content="Arbio trabaja en la conservación de 916 hectáreas de bosque amazónico en Tambopata, Madre de Dios, generando soluciones económicamente viables y sostenibles para los guardianes del bosque.">ARBIO</a></h4>
      </div>
    </div>

    <div class="c-card">
      <div class="c-card__item">
          <p>Una iniciativa de:</p>
          <br>
          <div>
            <a href="http://arbioperu.org/"><img class="img-responsive" src="/static/images/logos/arbio.jpg"></a>
            <p>Asociación para la Resiliencia del Bosque frente a la Inter-Oceánica</p>
          </div><!--
          --><div>
            <a href="http://somosazucar.org/"><img class="img-responsive" src="/static/images/logos/somosazucar.png"></a>
            <br>
            <p>Tecnología Libre para la Educación Pública</p>
            <br>
          </div>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  mounted: function () {
    if (this.$store.state.page === undefined) {
      this.$store.commit('setPage', this.$route.query.page || 1)
    }
    this.$store.dispatch('getTrees')
  }
}
</script>

<style scoped>
.c-card__item {
    padding-left: 2em;
}
</style>
