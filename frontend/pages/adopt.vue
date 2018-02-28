<template>
  <div id="container">
    <h1>Paso 2: Personaliza tu Adopción</h1>
    <p>
    ¡Felicidades! has seleccionado {{ total }} árboles para adoptar. A continuación podrás personalizar los certificados de adopción que serán emitidos.
    </p>

    <form name="adoption_form" ref="adoption_form" @submit.prevent="confirm">
    <div class="o-grid o-grid--demo">
      <div class="o-grid__cell">
        <div class="c-card">
          <div v-for="id in this.$store.state.cart" class="c-card__item">
              <label class="c-card__item"><b>{{tree(id).cost}} USD</b>/a : {{tree(id).common_name}} <i>({{tree(id).code}})</i></label>
          </div>
        </div>
      </div>
      <div class="o-grid__cell">
        <div class="c-card">
          <div class="formulario c-card__item">
              <div class="c-card__item c-card__item--success">
                <label class="c-label">
                  Nombre de quien adopta:
                  <input v-model.lazy="sponsor" class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  Número de ID tributaria:
                  <input v-model.lazy="taxid" class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  Email:
                  <input v-model.lazy="email" class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  País:
                  <input v-model.lazy="country" class="c-field c-field--label">
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
                  <input v-model.lazy="giftFrom" class="c-field c-field--label">
                  <div class="c-hint">¡Gracias!</div>
                </label>
                <label class="c-label">
                  Para:
                  <input v-model.lazy="giftTo" class="c-field c-field--label">
                  <div class="c-hint">Te lo agradecerá</div>
                </label>
                <label class="c-label">
                  Mensaje:
                  <textarea v-model.lazy="giftDedication" class="c-field" placeholder="Escribe un mensaje o dedicatoria..."></textarea>
                </label>
              </div>
          </div>
        </div>
      </div>
    </div>

    <div class="o-container o-container--medium">
        <div id="checkout" class="c-card">
          <div class="c-card__item c-card__item--error u-large">
            <div class="o-grid o-grid--demo">
              <div id="por_label" class="o-grid__cell o-grid__cell--width-10 u-center-block">
                <div class="o-grid-text u-center-block__content u-center-block__content--vertical">Por</div>
              </div>
              <div style="padding:0px" class="o-grid__cell o-grid__cell--width-10">
                <select v-model="years" id="year_select" class="c-field">
                  <option v-for="i in [1,2,3,4,5,6,7,8,9,10]" v-bind:selected="i=='3'" v-bind:value="i">{{ i }}</option>
                </select>
              </div>
              <div class="o-grid__cell o-grid__cell--width-20 u-center-block">
                 <div class="o-grid-text u-center-block__content u-center-block__content--vertical">años.</div>
              </div>
              <div class="o-grid__cell o-grid__cell--width-70 u-center-block">
                 <div class="o-grid-text u-absolute-center">Costo total: {{ $store.getters.totalCost }} USD.</div>
              </div>
            </div>
          </div>
        </div>

        <input type="submit" class="c-button c-button--block c-button--warning u-high u-xlarge" value="Finalizar" />
    </div>
    </form>
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
    },
    confirm: function (event) {
      this.$router.push('/confirm')
    }
  },
  computed: {
    sponsor: {
      get: function () {
        return this.$store.state.sponsor
      },
      set: function (sponsor) {
        this.$store.commit('setSponsor', sponsor)
      }
    },
    taxid: {
      get: function () {
        return this.$store.state.taxid
      },
      set: function (taxid) {
        this.$store.commit('setTaxid', taxid)
      }
    },
    email: {
      get: function () {
        return this.$store.state.email
      },
      set: function (email) {
        this.$store.commit('setEmail', email)
      }
    },
    country: {
      get: function () {
        return this.$store.state.country
      },
      set: function (country) {
        this.$store.commit('setCountry', country)
      }
    },
    giftFrom: {
      get: function () {
        return this.$store.state.giftFrom
      },
      set: function (giftFrom) {
        this.$store.commit('setGiftFrom', giftFrom)
      }
    },
    giftTo: {
      get: function () {
        return this.$store.state.giftTo
      },
      set: function (giftTo) {
        this.$store.commit('setGiftTo', giftTo)
      }
    },
    giftDedication: {
      get: function () {
        return this.$store.state.giftDedication
      },
      set: function (giftDedication) {
        this.$store.commit('setGiftDedication', giftDedication)
      }
    },
    years: {
      get: function () {
        return this.$store.state.years
      },
      set: function (y) {
        this.$store.commit('setYears', y)
      }
    },
    total: function () {
      return this.$store.state.cart.length
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
#year_select {
    text-align-last: right;
    width: 3em;
}
#por_label {
    padding-right: 0px;
    text-align: right;
}
option {
    direction: rtl;
}
</style>
