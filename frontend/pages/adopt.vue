<template>
  <div id="container">
    <h1>Paso 2 (opcional): Personaliza tu Adopción</h1>
    <p>
    ¡Felicidades! has seleccionado {{ total }} árboles para adoptar. A continuación podrás personalizar los certificados de adopción que serán emitidos.
    </p>

    <div class="o-container o-container--medium">
        <div class="c-card">
          <div v-for="id in this.$store.state.cart" class="c-card__item">
          <label class="c-card__item"><b>{{tree(id).cost}} USD</b> : Adoptar {{tree(id).common_name}} <i>({{tree(id).code}})</i> por 1 año</label>
          </div>
          <div class="formulario c-card__item">
              <div class="c-card__item c-card__item--success">
                <label class="c-field c-field--choice">
                  <input type="checkbox"> Es un obsequio
                </label>
                <label class="c-label">
                  De:
                  <input class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  Para:
                  <input class="c-field c-field--label">
                  <div class="c-hint">Siempre te lo agradecerá</div>
                </label>
                <label class="c-label">
                  Mensaje:
                  <textarea class="c-field" placeholder="Escribe un mensaje o dedicatoria..."></textarea>
                  <div class="c-hint">Siempre te lo agradecerá</div>
                </label>
              </div>
          </div>
        </div>

        <div id="checkout" class="c-card">
          <div class="c-card__item c-card__item--info">
             Costo total: {{ totalCost }} USD.
          </div>
        </div>

        <nuxt-link to="/confirm">
          <a class="c-button c-button--block c-button--warning u-high">Finalizar</a>
        </nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  components: {
    'adoption-cart': () => import('~/components/adoption-cart')
  },
  methods: {
    tree: function (id) {
      return this.$store.state.trees[id]
    }
  },
  computed: {
    total: function () {
      return this.$store.state.cart.length
    },
    totalCost: function () {
      var cost = 0
      for (var id of this.$store.state.cart) {
        cost = cost + this.$store.state.trees[id].cost
      }
      return cost
    }
  }
}
</script>

<style scoped>
.c-card {
    margin-bottom: 30px;
}
.formulario {
    padding: 0px;
}
#checkout {
    text-align: right;
}
</style>
