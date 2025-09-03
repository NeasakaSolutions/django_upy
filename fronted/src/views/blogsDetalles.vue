<script setup>
import Header from '@/components/Header.vue';
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { blogComposable } from '@/componsables/blogComponsable';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';

let route = useRoute();
const { dato, error } = blogComposable(route.params.slug);

let store = useAuthStore();

</script>

<template>
  <Header />
  <Fondo />

  <div class="container my-5 d-flex flex-wrap gap-4">
    <!-- Contenedor principal -->
    <div class="contenedor_blog_articulos flex-grow-1">

      <!-- Imagen del blog editable desde CSS si se desea -->
      <div class="img_art_blog_wrapper">
        <!--
        <img :src="dato.data?.imagen" alt="Imagen del blog" class="img_blog" />
        -->

        <div class="img_blog_wrapper" :style="{ backgroundImage: `url(${dato.data?.imagen})` }"></div>
      </div>

      <!-- Información general -->
      <div class="info_blog">
        <p><span>Fecha de publicación:</span> {{ dato.data?.fecha }}</p>
        <p><span>Nombre:</span> {{ dato.data?.nombre }}</p>
        <p><span>Categoria:</span> {{ dato.data?.categoria }}</p>
        <p><span>Creado por:</span> {{ dato.data?.user }}</p>
      </div>

      <!-- Descripción y PDF -->
      <div class="descripcion_blog">
        <p class="descripcion"><span>Descripcion:</span> {{ dato.data?.descripcion }}</p>
        <p><span>PDF:</span> <a :href="dato.data?.documento" target="_blank">Descargar PDF</a></p>
      </div>



    </div>

    <!-- Menú lateral -->
    <div class="contenedor_blog_menu">
      <ul class="mini_menu_config">
        <li class="logo">
          <router-link to='/' title="Home" class="navbar-brand">
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



