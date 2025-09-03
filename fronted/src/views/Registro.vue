<script setup>
// Importaciones
import Header from '@/components/Header.vue'
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { registroSchema } from '@/schemas/validacionesSchema';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { ref } from 'vue';
import { registroComposable } from '@/componsables/useSeguridadComposable';
import { useAuthStore } from '@/stores/authStore';

const store = useAuthStore();

let boton = ref('block');
let preloader = ref('none');

let nombre = ref('');
let correo = ref('');
let password = ref('');

const {sendData} = registroComposable();

let enviar = () => {
    boton.value = 'none';
    preloader.value = 'block';

    sendData({nombre: nombre.value, correo: correo.value, password: password.value});
};

</script>

<template>
  <Header></Header>
  <Fondo></Fondo>

  <div class="container my-5 d-flex flex-wrap gap-4">
    <!-- Contenedor principal -->
    <div class="contenedor_blog_articulos flex-grow-1">
      <img src="/img/blog-img/portada_blogs_2.png" alt="Imagen del blog" class="img_art" />
      <h5 class="titulos my-3">Registro</h5>
      <p class="subtitulos">Complete los campos solicitados:</p>

      <div class="cards_container_form">
        <div class="card_form3">
          <Form class="p-3" :validation-schema = "registroSchema" @submit = "enviar()">
            <div class="row mb-3">
              <div class="col-12 col-md-6">
                <label for="nombre" class="form-label texto_formulario">Nombre</label>
                <Field name="nombre" type="text" placeholder="Neasaka Pendragon"
                  class="form-control" v-model = "nombre" />
                  <ErrorMessage name = "nombre" class = "text text-warning" />
              </div>
              <div class="col-12 col-md-6 mt-3 mt-md-0">
                <label for="correo" class="form-label texto_formulario">Correo</label>
                <Field name="correo" type="email" placeholder="correo@correo.com"
                  class="form-control" v-model = "correo" />
                  <ErrorMessage name = "correo" class = "text text-warning" />
              </div>
            </div>

            <div class="row mb-3">
              <div class="col-12 col-md-6">
                <label for="password" class="form-label texto_formulario">Contraseña</label>
                <Field name="password" type="password" placeholder="*********"
                  class="form-control" v-model = "password" />
                  <ErrorMessage name = "password" class = "text text-warning" />
              </div>
            </div>

            
            <div class="row">
              <div class="col d-flex justify-content-center" v-if="boton === 'block'">
                <button type="submit" class="btn btn-warning btn_enviar color_btn_enviar">
                  <p class="subtitulos mb-0">Enviar</p>
                </button>
              </div>

              <div class="col d-flex justify-content-center" v-if="preloader === 'block'">
                <img src="/img/img/load.gif" />
              </div>


            </div>
          </Form>
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

  <Fotter></Fotter>
</template>

<style scoped>

</style>

