<script setup>
import Header from '@/components/Header.vue'
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { getPortadaById } from '@/services/portadaService';
import { Form, Field } from 'vee-validate';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { onMounted ,ref } from 'vue';

let datos = ref([]);
let portada = ref(null)
let store = useAuthStore();

onMounted(async() => {
  // Portadas
  portada.value = await getPortadaById(5)

  let respuesta = await fetch(`${import.meta.env.VITE_API_URL}docentes`, {
    headers: {'content-type': 'application/json'}
  });
  const datosJSON = await respuesta.json();
  datos.value = datosJSON.data;
});

let route = useRoute();
let boton = ref('block');
let preloader = ref('none');
const ID_PORTADA = 5;

let enviar = async () => {
  boton.value = "none";
  preloader.value = "block";

  let file_imagen = document.querySelector("#file_imagen").files[0];
  let formData = new FormData();
  formData.append('foto', file_imagen);
  formData.append('id', ID_PORTADA); // aquí le pasas la ID fija

  try {
    let resp = await fetch(`${import.meta.env.VITE_API_URL}portadas/editar/foto`, {
      method: 'POST',
      body: formData,
      headers: {
        'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`
      }
    });

    if (resp.status === 200) {
      alert("Se modificó el registro");
      window.location.reload();
    } else {
      alert("Ocurrió un error al modificar el registro");
      boton.value = "block";
      preloader.value = "none";
    }
  } catch (err) {
    alert("Ocurrió un error inesperado");
    boton.value = "block";
    preloader.value = "none";
  }
};

</script>

<template>
<Header></Header>
<Fondo></Fondo>
<div class="container my-5 d-flex flex-wrap gap-4">
    <!-- Contenedor principal -->
    <div class="contenedor_blog_articulos flex-grow-1">
        <!--
      <img src="/img/blog-img/portada_blogs_2.png" alt="Imagen del blog" class="img_art" />
        -->
      <img v-if="portada" :src="portada.imagen" alt="Imagen del blog" class="img_art" />

        <!--Configuracion para editar portada-->
        <div v-if="store.authId != null" class="cards_container_form">
        <div class="card_form3 p-4 rounded">

          <Form @submit="enviar()">
            <div class="form-panel mb-3">
              <div class="row">
                <div class="col-12">
                  <label for="file_imagen" class="form-label fw-bold">Editar portada:</label>
                  <Field name="imagen" type="file" id="file_imagen" class="form-control" />
                </div>
              </div>
            </div>

            <!--Configuracion de los botones-->
            <div class="col-12 text-center" :style="'display:'+boton">
                <button class="btn btn-outline-warning" type="submit" title="Enviar">
                Enviar
                </button>
            </div>
            <div class="col-12 text-center" :style="'display:'+preloader">
                <img src="/img/img/load.gif" />
            </div>
          </Form>
        </div>

        

          <div class="d-flex align-items-center gap-3 my-5">
            <div class="col-3">
                <div class="text-right my-5">
                    <a href="#modal2" @click="crear()" class="btn btn-outline-warning text-nowrap">
                        <i class="fas fa-plus"></i> Crear Docente
                    </a>
                </div>
            </div>

            <div class="col-2">
                <div class="text-right my-5">
                  <a class="btn btn-outline-warning">
                      <router-link :to = "{name: 'panel'}" class="nav-link">Blogs</router-link>
                  </a>
                </div>
            </div>

          </div>

        

        <hr />

        <!--Configuracion de la tabla-->
        <div class="col-12">
          <div class="table-respopnsive">
            <table class="table table-bordered table-striped table-hover aling-middle text-center">

              <thead class="table-warning">
                <tr>
                  <th>ID</th>
                  <th>Nombre</th>
                  <th>Area</th>
                  <th>Foto</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="(dato, index) in datos" :key="index">
                  <td>{{  dato.id }}</td>
                  <td>{{  dato.nombre }}</td>
                  <td>{{  dato.area }}</td>
                  <td class="text-center">
                    <a :href="dato.imagen" class="lightbox d-block" data-fancybox="image-gallery">
                      <img :src="dato.imagen" :alt="dato.nombre" style="width: 100px;"></img>
                    </a>
                  </td>
      
                <td class="text-center">
                  <!--AQUI VAN LOS BOTONES DE FONT AWESOME-->
                  <router-link :to="{name: 'panel_editar_foto', params:{id:dato.id}}" title="Editar foto">
                    <i class="fa-solid fa-image"></i>
                  </router-link>
                  &nbsp;&nbsp;
                  <a href="#modal2" title="Editar" @click="editar(dato)">
                    <i class="fas fa-edit"></i>
                  </a>
                  &nbsp;&nbsp;
                  <router-link to="#" @click.navigate="eliminar(dato.id)" title="Eliminar">
                    <i class="fas fa-trash"></i>
                  </router-link>
                  &nbsp;&nbsp;
                </td>
                </tr>
              </tbody>

            </table>
          </div>
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