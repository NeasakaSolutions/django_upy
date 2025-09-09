<script setup>
// Importaciones
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Header from '@/components/Header.vue'
import Fotter from '@/components/Fotter.vue'

const API_URL = import.meta.env.VITE_API_URL;

const videos = ref([]);

const getVideos = async () => {
    try {
        // Usa `axios.get` con la URL construida de forma similar a tu ejemplo
        const response = await axios.get(`${API_URL}videos`);
        
        // Asigna el array de datos dentro de la clave 'data' de la respuesta
        videos.value = response.data.data;
        
        // Opcional: Para verificar que se reciben los datos
        console.log("Datos de videos recibidos:", videos.value);
    } catch (error) {
        console.error("Error al obtener los videos:", error);
    }
};

onMounted(() => {
    getVideos();
});
</script>

<template>
  <Header></Header>

  <div class="fondo_animado_videos"></div>

  <div class="contenido_videos">
    <div class="container contenedor_videos my-3">
      <div class="row">
        <div class="col d-flex justify-content-center">
          <h4>Videos</h4>
        </div>
        <hr class="estilo_hr" />
      </div>

      <div v-for="video in videos" :key="video.id">
        <div class="container contenedor_videos my-3">
          <div class="row">
            <div class="col d-flex justify-content-center">
              <h5 class="title_video"><strong>{{ video.nombre }}</strong></h5>
            </div>
          </div>
          <div class="row">
            <div class="col d-flex justify-content-center">
              <p class="text_video">{{ video.descripcion }}</p>
            </div>
          </div>
          <div class="row">
            <div class="col d-flex justify-content-center">
              <iframe
                v-if="video.id_youtube"
                class="config_videos"
                width="560"
                height="315"
                :src="video.video_url"
                title="YouTube video player"
                frameborder="0"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen
              ></iframe>

              <video
                v-else-if="video.video"
                :src="video.video_url"
                class="config_videos"
                width="560"
                height="315"
                controls
              ></video>
            </div>
          </div>
        </div>
      </div>

      <div v-if="!videos || videos.length === 0" class="col">
        <p>No se encontraron videos para mostrar.</p>
      </div>
    </div>
  </div>

  <Fotter />
</template>


