<script setup>
// Importaciones
import Header from '@/components/Header.vue'
//import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
</script>

<template>
  <Header></Header>

  <!-- Fondo fijo completo -->
  <div class="fondo_animado_videos"></div>

  <!-- Contenido encima del fondo -->
  <div class="contenido_videos">
    <div class="container contenedor_videos my-3">
      <div class="row">
        <div class="col d-flex justify-content-center">
          <h4>Reels</h4>
        </div>
        <hr class="estilo_hr" />
      </div>

      <div class="row d-flex justify-content-center pad_left">
        <div class="col">
          <iframe width="180" height="280" src="https://youtube.com/embed/u6gxfjSijYY?si=xsYJ5PWBmJkhmhsr" class="config_shorts"></iframe>
        </div>
        <div class="col">
          <iframe width="180" height="280" src="https://youtube.com/embed/yoEx8mcoOTA?si=h6rbM2Ai7pv4K8YG" class="config_shorts"></iframe>
        </div>
        <div class="col">
          <iframe width="180" height="280" src="https://youtube.com/embed/VbcmgSpTzJc?si=qITDbGLjHk8s-Xvu" class="config_shorts"></iframe>
        </div>
        <div class="col">
          <iframe width="180" height="280" src="https://www.youtube.com/embed/34owtDGx3ZY" class="config_shorts"></iframe>
        </div>
      </div>
    </div>

    <!-- Más contenido... -->

  </div>

  <Fotter />
</template>
