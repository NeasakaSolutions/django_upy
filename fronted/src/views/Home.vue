<!--Cargar referencias javascript-->
<script setup>
// Importaciones
import Header from '@/components/Header.vue';
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { Form, Field } from 'vee-validate';
import { getPortadaById } from '@/services/portadaService';
import { onMounted, ref } from 'vue';
import { useAuthStore } from '@/stores/authStore';
import { getDatosDocentes } from '@/services/docentesService';
import { getDatosLaboratorios } from '@/services/laboratoriosService';
import { getDatosColaboradores } from '@/services/colaboradoresService';

// Variables reactivas
let portadas = ref([]); // Ahora es un array para las 3 portadas
let store = useAuthStore();
let id_portada = ref(2); // ID de la portada que se va a editar
let boton = ref('block');
let preloader = ref('none');

// Cargar las portadas al montar el componente
onMounted(async () => {
  try {
    const portada1 = await getPortadaById(2);
    const portada2 = await getPortadaById(3);
    const portada3 = await getPortadaById(4);
    portadas.value = [portada1, portada2, portada3];
  } catch (error) {
    console.error("Error al cargar las portadas:", error);
  }
});

// Función para cambiar el ID de la portada a editar
const cambiarID = (id) => {
  id_portada.value = id;
};

// Función para enviar la foto
const enviar = async () => {
  boton.value = "none";
  preloader.value = "block";

  let file_imagen = document.querySelector("#file_imagen").files[0];
  let formData = new FormData();
  formData.append('foto', file_imagen);
  formData.append('id', id_portada.value); // Usa la variable reactiva

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

// Cards de docentes:
let datos = ref([]);
let labs = ref([]);
let logos = ref([]);

onMounted(async() => {
    // Docentes
    datos.value = await getDatosDocentes();
    // Laboratorios
    labs.value = await getDatosLaboratorios();
    // Colaboradores
    logos.value = await getDatosColaboradores();

});

</script>

<!--Codigo fuente de la aplicacion-->
<template>
    <Header></Header>
    <Fondo></Fondo>

    
        <div class="container contenedor">

            <div class="row mt-5">
                <div class="col">
                    <div class="carousel slide carousel-light carousel-fade" id="mi-carousel" data-bs-ride="carousel">
                    <div class="carousel-indicators">
                        <button v-for="(portada, index) in portadas" :key="index" type="button" :class="{ active: index === 0 }"
                        data-bs-target="#mi-carousel" :data-bs-slide-to="index" :aria-label="'Slide ' + (index + 1)"></button>
                    </div>
                    <div class="carousel-inner">
                        <div class="carousel-item" v-for="(portada, index) in portadas" :key="portada.id" :class="{ active: index === 0 }" data-bs-interval="5000">
                        <img class="img-fluid w-100 carousel_img img_transparencia" :src="portada.imagen" alt="Imagen de propaganda">
                        <div class="degradado"></div>
                        <div class="carousel-caption d-none d-md-block">
                            <h5><strong>{{ portada.titulo }}</strong></h5>
                            <p>{{ portada.descripcion }}</p>
                        </div>
                        </div>
                    </div>
                    <button class="carousel-control-prev d-none d-md-block" type="button" data-bs-target="#mi-carousel" data-bs-slide="prev">
                        <span class="carousel-control-prev-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Anterior</span>
                    </button>
                    <button class="carousel-control-next d-none d-md-block" type="button" data-bs-target="#mi-carousel" data-bs-slide="next">
                        <span class="carousel-control-next-icon" aria-hidden="true"></span>
                        <span class="visually-hidden">Siguiente</span>
                    </button>
                    </div>
                </div>
                </div>

            <!--Configuracion para editar portada-->
            <div v-if="store.authId != null" class="cards_container_form">
                <div class="card_form3 p-4 rounded">
                    <Form @submit="enviar()">
                    <div class="form-panel mb-3">
                        <div class="row">
                        <div class="col-12">
                            <label for="select_portada" class="form-label fw-bold">Seleccionar portada a editar:</label>
                            <select class="form-select mb-3" id="select_portada" @change="cambiarID($event.target.value)">
                            <option value="2">Portada 1</option>
                            <option value="3">Portada 2</option>
                            <option value="4">Portada 3</option>
                            </select>
                            <label for="file_imagen" class="form-label fw-bold">Editar foto:</label>
                            <Field name="imagen" type="file" id="file_imagen" class="form-control" />
                        </div>
                        </div>
                    </div>

                    <div class="col-12 text-center" :style="'display:' + boton">
                        <button class="btn btn-outline-warning" type="submit" title="Enviar">
                        Enviar
                        </button>
                    </div>
                    <div class="col-12 text-center" :style="'display:' + preloader">
                        <img src="/img/img/load.gif" alt="Cargando"/>
                    </div>
                    </Form>
                </div>
                </div>



            <!-- Configuracion de la seccion de colaboradores -->
            <div class="row my-5">
                <div class="col">
                    <h4 class="titulos">Colaboradores</h4>
                    <p class="subtitulos">Gracias por confiar en nosotros.</p>
                </div>
            </div>

            <!-- Configuración de los logotipos -->
            <div class="container my-5">

                <div class="row justify-content-center text-center g-3">

                    <div class="col-6 col-sm-4 col-md-3 col-lg-2" v-for="(logo, index) in logos.data" :key="index">
                        <button class="btn btn-outline-dark btn_logo w-100" :class="index % 2 === 0 ? 'bg_color_3' : 'bg_color_4'">
                            <img class="svg_colab img-fluid" :src="logo.imagen" :alt="logo.nombre">
                        </button>
                    </div>


                    <!--
                    <div class="col-6 col-sm-4 col-md-3 col-lg-2" v-for="(logo, index) in logos.data" :key="index">
                        <button class="btn btn-outline-dark btn_logo color_btn w-100" :class="index % 2 === 0 ? 'bg_color_1' : 'bg_color_2'">
                            <img class="svg_colab img-fluid" :src="logo.imagen" :alt="logo.nombre">
                        </button>
                    </div>
                    -->
                    

                    <!--
                    <div class="col-6 col-sm-4 col-md-3 col-lg-2">
                        <button class="btn btn-outline-dark btn_logo color_btn w-100">
                            <img class="svg_colab img-fluid" src="/img/Logos/AURA_LOGO.svg">
                        </button>
                    </div>
                    -->
                </div>
            </div>


            <!-- Configuracion de la seccion de laboratorios-->
            <div class="row my-5">
                <div class="col">
                    <h4 class="titulos">Laboratorios.</h4>
                    <p class="subtitulos">Tu arsenal comienza aquí.</p>
                </div>
            </div>

            <!-- Laboratorios (3 en total) -->
            <!--<div class="row my-5 g-4">-->
            <div class="row my-5 g-4 justify-content-center">
                <!-- Laboratorios -->
                <div class="col-12 col-md-6 col-lg-4" v-for="(lab, index) in labs.data" :key="index">
                    <div class="card card_radius h-100 small-card" :class="index % 2 === 0 ? 'bg_color_2' : 'bg_color_1'">
                        <img class="img-card-top card_img img-fluid" :src="lab.imagen" alt="dato.nombre">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title card_title text-center">{{ lab.nombre }}</h5>
                            <p class="card-text card_text text-justify d-none d-md-block">{{ lab.descripcion }}</p>
                        </div>
                    </div>
                </div>

                <!--
                <div class="col-12 col-md-6 col-lg-4">
                    <div class="card card_radius h-100 bg_color_2 small-card">
                        <img class="img-card-top card_img img-fluid" src="/img/blog-img/LAB_CINCO.jpg"
                            alt="Imagen del laboratorio dos">
                        <div class="card-body d-flex flex-column">
                            <h5 class="card-title card_title text-center">Laboratorio Dos</h5>
                            <p class="card-text card_text text-justify d-none d-md-block">
                                Lorem ipsum dolor sit amet consectetur
                                adipisicing elit. Exercitationem ex nostrum iusto ab quis dicta excepturi inventore
                                debitis at similique quaerat est obcaecati tempora saepe possimus, sed veritatis! Iste,
                                doloremque
                            </p>
                        </div>
                    </div>
                </div>
                -->
                
            </div>

            <div class="d-none d-lg-block">
                <!-- Seccion donde se tendra informacion general de los profesores -->
                <div class="row my-5">
                    <div class="col">
                        <h5 class="titulos">Docentes destacados</h5>
                    </div>
                </div>

                <!-- Configuracion de la primer seccion -->
                <div class="row mt-3 my-5 g-4">

                    <div class="row mt-3 my-5 g-4">
                    <div
                        v-for="(dato, index) in datos.data"
                        :key="index"
                        class="col-12 col-sm-6 col-md-4 col-lg-2 d-flex justify-content-center mb-4">
                        <div class="card card_profesor card_radius" :class="index % 2 === 0 ? 'bg_color_1' : 'bg_color_2'">
                            <img class="card-img-top card_img_profesor" :src="dato.imagen" :alt="dato.nombre" />
                            <div class="card-body">
                                <h5 class="card-title card_title_profesor">{{ dato.nombre }}</h5>
                                <h6 class="card-subtitle text-muted card_subtitle_profesor">{{ dato.area }}</h6>
                            </div>
                        </div>
                    </div>
                    </div>

                    <!--
                    <div class="row mt-3 my-5 g-4">
                    <div
                        v-for="(dato, index) in datos.data"
                        :key="index"
                        class="col-12 col-sm-6 col-md-4 col-lg-2 d-flex justify-content-center mb-4">
                        <div class="card card_profesor card_radius bg_color_1">
                            <img class="card-img-top card_img_profesor" :src="dato.imagen" :alt="dato.nombre" />
                            <div class="card-body">
                                <h5 class="card-title card_title_profesor">{{ dato.nombre }}</h5>
                                <h6 class="card-subtitle text-muted card_subtitle_profesor">{{ dato.area }}</h6>
                            </div>
                        </div>
                    </div>
                    </div>
                    -->

                </div>
            </div>


        </div>

    

    <Fotter></Fotter>
</template>

<!--Cargar los estilos-->
<style scoped>
.bg_color_1 {
    background-color:  #7b3fbf;
}

.bg_color_2 {
    background-color: #ffeb3b;
}

/* Para los botones con bg_color_1 */

.bg_color_3 {
    background-color:  #7b3fbf;
}

.bg_color_4 {
    background-color: #ffeb3b;
}

/* Para los botones con bg_color_1 */
.bg_color_3:hover {
  background-color: transparent !important;
  /* La propiedad !important se usa para asegurar que se aplique el hover, 
     ya que la clase .bg_color_1 puede tener una especificidad alta */
}

/* Para los botones con bg_color_2 */
.bg_color_4:hover {
  background-color: transparent !important;
}

</style>