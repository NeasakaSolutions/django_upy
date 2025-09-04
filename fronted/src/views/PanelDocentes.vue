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
      </div>
    </div>
</div>
<Fotter></Fotter>
</template>

<style scoped>
</style>