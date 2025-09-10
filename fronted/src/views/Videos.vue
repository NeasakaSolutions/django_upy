<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'
import Header from '@/components/Header.vue'
import Fotter from '@/components/Fotter.vue'
import Fondo from '@/components/Fondo.vue';

const API_URL = import.meta.env.VITE_API_URL;
const videos = ref([]);

const getVideos = async () => {
  try {
    const response = await axios.get(`${API_URL}videos`);
    videos.value = response.data?.data || [];
    console.log("Datos de videos recibidos:", videos.value);
  } catch (error) {
    console.error("Error al obtener los videos:", error);
  }
};

onMounted(getVideos);
</script>

<template>
  <Header></Header>
  <Fondo></Fondo>

  <div class="contenido_videos">
    
      <div class="row">
        <div class="col d-flex justify-content-center">
          <h4>Videos</h4>
        </div>
        <hr class="estilo_hr" />
      </div>

      <div v-if="videos.length > 0">
        <div v-for="video in videos" :key="video.id" class="container contenedor_videos my-3">
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
              <!-- Si es YouTube -->
              <iframe
                v-if="video.video_url.includes('youtube.com')"
                class="config_videos"
                width="560"
                height="315"
                :src="video.video_url"
                title="YouTube video player"
                allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share"
                referrerpolicy="strict-origin-when-cross-origin"
                allowfullscreen
              ></iframe>

              <!-- Si es video local -->
              <video
                v-else
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

      <div v-else class="col">
        <p>No se encontraron videos para mostrar.</p>
      </div>
    
  </div>

  <Fotter></Fotter>
</template>



