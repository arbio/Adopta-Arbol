<template>
  <div id="container">
    <h1>¡Gracias! Emisión de certificado</h1>
    <p v-if="$store.state.adoptions.length < 1">
    Por favor espera mientras emitimos el certificado.
    </p>
    <p>
    Hemos enviado tus certificados por correo electrónico.

    Encontrarás tus certificados a continuación:
    </p>
    <div v-for="adoption in $store.state.adoptions">
        <hr>
        <h2>Previsualización:</h2>
        <div v-for="cert in adoption.svg_certs">
          <object id="svg1" width="812" height="580" :data="'/' + cert" type="image/svg+xml"></object>
        </div>
        <hr>
        <h2>En pdf:</h2>
        <ul>
        <li v-for="cert in adoption.pdf_certs">
            <a :href="cert" target="_new" >{{ cert }}</a>
        </li>
        </ul>
    </div>
    </div>
  </div>
</template>
