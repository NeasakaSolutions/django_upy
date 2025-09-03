<script setup>
import Header from '@/components/Header.vue'
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { blogsComposable } from '@/componsables/blogsComponsable';
import { watchEffect } from 'vue';
import { useAuthStore } from '@/stores/authStore';

const { datos, categorias, error } = blogsComposable();

let store = useAuthStore();

watchEffect(() => {
  if(error.value){
    window.location = "/error";
  }
});
</script>

<template>
  <Header />
  <Fondo />

  <div class="container my-5 d-flex flex-wrap gap-4">
    <!-- Contenedor principal -->
    <div class="contenedor_blog_articulos flex-grow-1">
      <img src="/img/blog-img/portada_blogs_2.png" alt="Imagen del blog" class="img_art" />
      <h5 class="titulos my-3">Todos nuestros posts</h5>

      <div class="cards_container3">
        <div v-for="(dato, index) in datos.data" :key="index" class="card_item3">
          <router-link :to="{ name: 'blogsDetalle', params: { slug: dato.slug } }" class="card_link3">
            <img :src="dato.imagen" alt="Imagen del blog" class="card_image3" />
            <h6 class="card_title3">{{ dato.nombre }}</h6>
          </router-link>
        </div>
      </div>
    </div>

    <!-- Menú lateral -->
    <div class="contenedor_blog_menu">
      <ul class="mini_menu_config">
        <li class="logo">
          <router-link to="/" title="Home" class="navbar-brand">
            <img alt="Logotipo" src="/img/core-img/favicon.ico" class="logo_img" />
          </router-link>
        </li>
        <li v-if="store.authId == null">
          <router-link :to="{ name: 'login' }">Iniciar sesión</router-link>
        </li>
        <li v-else>
          <router-link :to="{ name: 'panel' }">Panel</router-link>
        </li>
        <li><router-link :to="{ name: 'blogs' }">Inicio</router-link></li>
        <li><router-link :to="{ name: 'BlogsGeneral' }">Blogs</router-link></li>
        <li><router-link :to="{ name: 'contacto' }">Contacto</router-link></li>
      </ul>
    </div>
  </div>

  <Fotter />
</template>

<style scoped>
</style>
