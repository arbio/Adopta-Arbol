<template>
  <div id="container">
    <h1>Paso 2: Personaliza tu Adopción</h1>
    <p>
    ¡Felicidades! has seleccionado {{ total }} árboles para adoptar. A continuación podrás personalizar los certificados de adopción que serán emitidos.
    </p>

    <div class="o-grid o-grid--demo">
      <div class="o-grid__cell">
        <div class="c-card">
          <div v-for="id in this.$store.state.cart" class="c-card__item">
              <label class="c-card__item"><b>{{tree(id).cost}} USD</b> : {{tree(id).common_name}} <i>({{tree(id).code}})</i></label>
          </div>
        </div>
      </div>
      <div class="o-grid__cell">
        <div class="c-card">
          <div class="formulario c-card__item">
              <div class="c-card__item c-card__item--success">
                <label class="c-label">
                  Nombre de quien adopta:
                  <input class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  Número de ID tributaria:
                  <input class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  Email:
                  <input class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  País:
                  <input class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-field c-field--choice">
                  <input v-model="isGift" type="checkbox">&nbsp;
                  <i class="fa fa-gift fa-3x" aria-hidden="true"></i> Obsequio
                  
                </label>
              </div>
              <div v-show="isGift" class="c-card__item c-card__item--info">
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
      </div>
    </div>

    <div class="o-container o-container--medium">
        <div id="checkout" class="c-card">
          <div class="c-card__item c-card__item--error u-large">
             Costo total: {{ totalCost }} USD.
          </div>
        </div>

        <nuxt-link to="/confirm">
          <a class="c-button c-button--block c-button--warning u-high u-xlarge">Finalizar</a>
        </nuxt-link>
    </div>
  </div>
</template>

<script>
export default {
  data: () => ({
    isGift: false
  }),
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
.c-hint {
    color: lightgrey;
}
.formulario {
    padding: 0px;
}
#checkout {
    text-align: right;
}
</style>
