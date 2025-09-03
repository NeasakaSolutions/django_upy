<script setup>
// Importaciones
import Header from '@/components/Header.vue';
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { useAuthStore } from '@/stores/authStore';
import { ref, onMounted } from 'vue';
import { useRoute } from 'vue-router';
import { Form, Field } from 'vee-validate';

// Store
const store = useAuthStore()

let route = useRoute();
let datos = ref({});
let boton = ref('block')
let preloader = ref('none')

onMounted(async()=>{
    let respuesta = await fetch(import.meta.env.VITE_API_URL+'blogs/'+route.params.id, 
    {headers: {'content-type': 'application/json'}})
    datos.value = await respuesta.json();
});

let enviar=async()=>{
    boton.value="none";
    preloader.value="block";
    let file_foto = document.querySelector("#file_foto").files[0];
    let formData = new FormData();
    formData.append('foto', file_foto);
    formData.append('id', route.params.id);
    try{
        let resp = await fetch(`${import.meta.env.VITE_API_URL}blogs/editar/foto`, 
            {
                method: 'POST',
                body: formData,
                headers: {'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`}
            })
            if(resp.status == 200){
                alert("Se modificó el registro")
                //window.location="panel/editar/foto/"+route.params.id;
                window.location.reload();
            }
    } catch (err){
        alert("Ocurrió un error inseperado")
        window.location="panel/editar/foto/"+route.params.id;
    }
};

</script>

<template>
  <Header></Header>
  <Fondo></Fondo>

  <div class="container my-5 d-flex flex-wrap gap-4">
    
    <!-- Contenedor principal -->
    <main class="contenedor_blog_articulos flex-grow-1">
      <img 
        src="/img/blog-img/portada_blogs_2.png" 
        alt="Imagen del blog" 
        class="img_art mb-3" 
      />
      <h5 class="titulos mb-4">Editar foto: {{ datos.data?.nombre }}</h5>

      <div class="cards_container_form">
        <div class="card_form3 p-4 rounded">

          <Form @submit="enviar()">
            <div class="form-panel mb-3">
              <div class="row">
                <div class="col-12">
                    <img :src="datos.data?.imagen" style="width: 200px;"/>
                </div>
                <div class="col-12">
                  <label for="file_foto" class="form-label fw-bold">Subir foto:</label>
                  <Field name="foto" type="file" id="file_foto" class="form-control" />
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
      </div>
    </main>

    <!-- Menú lateral -->
    <aside class="contenedor_blog_menu">
      <ul class="mini_menu_config list-unstyled p-0">
        <li class="logo mb-4 text-center">
          <router-link to="/" title="Home" class="navbar-brand">
            <img src="/img/core-img/favicon.ico" alt="Logotipo" class="logo_img" />
          </router-link>
        </li>
        <li v-if="!store.authId" class="mb-2">
          <router-link :to="{ name: 'login' }">Iniciar sesión</router-link>
        </li>
        <li v-else class="mb-2">
          <router-link :to="{ name: 'panel' }">Panel</router-link>
        </li>
        <li class="mb-2">
          <router-link :to="{ name: 'blogs' }">Inicio</router-link>
        </li>
        <li class="mb-2">
          <router-link :to="{ name: 'BlogsGeneral' }">Blogs</router-link>
        </li>
        <li>
          <router-link :to="{ name: 'contacto' }">Contacto</router-link>
        </li>
      </ul>
    </aside>

  </div>

  <Fotter />
</template>

<style scoped>

</style>

