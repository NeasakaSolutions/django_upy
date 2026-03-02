<script setup>
import Fondo from '@/components/Fondo.vue';
</script>

<template>
  <Fondo />

  <section class="about-area section-padding-80 error-404">
    <div class="container">
      <div class="row">
        <div class="col-12">
          <div class="section-heading">
            <h3>Ups, página no encontrada</h3>
          </div>
        </div>
      </div>

      <div class="row">
        <div class="col-12">
          <h6 class="sub-heading pb-5">Error 404</h6>
        </div>
      </div>

      <div class="row">
        <div class="col-12 centrado">
          <img class="mb-70 text-center" src="/img/img/404.gif" alt="Error 404" />
        </div>
      </div>
    </div>
  </section>
</template>

<style scoped>
.error-404 {
  color: white; /* Letras blancas */
  text-align: center;
}

.error-404 h3 {
  font-size: 2.2rem;
  font-weight: bold;
}

.error-404 .sub-heading {
  font-size: 1.4rem;
  opacity: 0.9;
}

.centrado img {
  max-width: 350px;
  width: 100%;
}
</style>
