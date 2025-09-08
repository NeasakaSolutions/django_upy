<script setup>
import Header from '@/components/Header.vue';
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { Fancybox } from '@fancyapps/ui';
import "@fancyapps/ui/dist/fancybox.css";
import { useAuthStore } from '@/stores/authStore';

// Validaciones de superusuario para el menu lateral
let store = useAuthStore();

// Estado de la aplicación
const portadas = ref([]);
const modal_titulo = ref('');
const seccion = ref('');
const portada_id = ref(0);
const boton = ref('block');
const preloader = ref('none');
const preview_foto = ref(null); // Variable para la vista previa de la foto

// URL base de tu API de Django. Debes configurar esto en tu entorno.
const API_URL = import.meta.env.VITE_API_URL;

// Lógica de carga de datos
const cargarPortadas = async () => {
    try {
        const respuesta = await axios.get(`${API_URL}portadas`);
        portadas.value = respuesta.data.data;
    } catch (error) {
        console.error('Error al cargar las portadas:', error);
        alert('Ocurrió un error al cargar las portadas.');
    }
};

// Cargar los datos al montar el componente
onMounted(() => {
    cargarPortadas();
});

// Lógica para el modal de Editar
const editar = (modelo) => {
    modal_titulo.value = 'Editar';
    portada_id.value = modelo.id;
    seccion.value = modelo.seccion;
    preview_foto.value = modelo.foto; // Establece la foto actual como vista previa
};

// Manejar el cambio de archivo para la vista previa
const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            preview_foto.value = e.target.result;
        };
        reader.readAsDataURL(file);
    } else {
        preview_foto.value = null;
    }
};

// Enviar el formulario al API (solo para edición)
const enviar = async () => {
    boton.value = "none";
    preloader.value = "block";

    const formData = new FormData();
    formData.append('id', portada_id.value);
    formData.append('seccion', seccion.value);
    
    const file_foto = document.querySelector("#file_foto").files[0];
    if (file_foto) {
        formData.append('foto', file_foto);
    }
    
    try {
        await axios.post(`${API_URL}portadas/editar/foto`, formData);
        alert("Se modificó el registro exitosamente");
        // Llama a la nueva función para actualizar la lista de portadas
        await cargarPortadas();
        // Cierra el modal, ya que la página no se recargará
        window.location.href = '#close';
    } catch (err) {
        alert("Ocurrió un error inesperado: " + err);
    } finally {
        // Restablece el estado de los botones y el preloader
        boton.value = 'block';
        preloader.value = 'none';
    }
};

</script>

<template>
    <Header></Header>
    <Fondo></Fondo>
    <div class="container my-5 d-flex flex-wrap gap-4">
        <div class="contenedor_blog_articulos flex-grow-1">
            <h5 class="titulos my-3">Panel</h5>
            <div class="row">
                <div class="col-12 d-flex gap-2 mb-4">
                    
                    <div class="text-right my-5">
                        <a class="btn btn-outline-warning">
                            <router-link :to="{ name: 'panel' }" class="nav-link">Blogs</router-link>
                        </a>
                    </div>
                    <div class="text-right my-5">
                        <a class="btn btn-outline-warning">
                            <router-link :to="{ name: 'panelDocentes' }" class="nav-link">Principal</router-link>
                        </a>
                    </div>

                </div>
                <hr />
                
                <div class="col-12">
                    <div class="table-responsive">
                        <table class="table table-bordered table-striped table-hover align-middle text-center">
                            <thead class="table-warning">
                                <tr>
                                    <th>ID</th>
                                    <th>Sección</th>
                                    <th>Foto</th>
                                    <th>Acciones</th>
                                </tr>
                            </thead>
                            <tbody>
                                <tr v-for="(portada, index) in portadas" :key="index">
                                    <td>{{ portada.id }}</td>
                                    <td>{{ portada.seccion }}</td>
                                    <td class="text-center">
                                        <a :href="portada.foto" class="lightbox d-block" data-fancybox="portada-gallery">
                                            <img :src="portada.foto" :alt="portada.seccion" style="width: 100px;">
                                        </a>
                                    </td>
                                    <td class="text-center">
                                        <a href="#modal" title="Editar" @click="editar(portada)" class="text-warning">
                                            <i class="fas fa-edit"></i>
                                        </a>
                                        
                                    </td>
                                </tr>
                            </tbody>
                        </table>
                    </div>
                </div>
            </div>
        </div>

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

    <div class="modalmask" id="modal">
        <div class="modalbox rotate">
            <a href="#close" title="Cerrar" class="close">X</a>
            <h2>{{ modal_titulo }}</h2>
            <div class="modal-content-scrollable">
                <form @submit.prevent="enviar()">
                    <div class="form-panel">
                        <div class="row container">
                            <div class="col-12 col-lg-12">
                                <label class="form-label">Sección:</label>
                                <span class="form-control-plaintext fw-bold">{{ seccion }}</span>
                            </div>
                            <div class="col-12 col-lg-12">
                                <label for="file_foto" class="form-label fw-bold">Subir foto:</label>
                                <input type="file" id="file_foto" class="form-control" @change="handleFileChange" />
                            </div>
                            <div v-if="preview_foto" class="col-12 col-lg-12 text-center my-3">
                                <img :src="preview_foto" alt="Vista previa de la portada" style="max-width: 100%; height: auto; border: 1px solid #ccc; padding: 5px;">
                            </div>
                            <div class="col-12 text-center" :style="'display:' + boton">
                                <button class="btn btn-outline-warning" type="submit" title="Enviar">Enviar</button>
                            </div>
                            <div class="col-12 text-center" :style="'display:' + preloader">
                                <img src="/img/img/load.gif" alt="Cargando..." />
                            </div>
                        </div>
                    </div>
                </form>
            </div>
        </div>
    </div>
    <Fotter></Fotter>
</template>

<style scoped>
/* (Sección de estilos CSS sin cambios) */
/*--------------------------------------------------------------------------------- */
.modalmask {
    position: fixed;
    font-family: Arial, sans-serif;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.8);
    z-index: 99999;
    opacity: 0;
    -webkit-transition: opacity 400ms ease-in;
    -moz-transition: opacity 400ms ease-in;
    transition: opacity 400ms ease-in;
    pointer-events: none;
}

.modalmask:target {
    opacity: 1;
    pointer-events: auto;
}

/*Formato de la ventana*/
.modalbox {
    width: 600px;
    position: relative;
    padding: 5px 20px 13px 20px;
    background: #fff;
    border-radius: 3px;
    -webkit-transition: all 500ms ease-in;
    -moz-transition: all 500ms ease-in;
    transition: all 500ms ease-in;
}

/*Movimientos*/
.rotate {
    margin: 1% auto;
    -webkit-transform: scale(-5, -5);
    transform: scale(-5, -5);
}

.modalmask:target .rotate {
    transform: rotate(360deg) scale(1, 1);
    -webkit-transform: rotate(360deg) scale(1, 1);
}

/*Boton de cerrar*/
.close {
    background: #606061;
    color: #FFFFFF;
    line-height: 25px;
    position: absolute;
    right: 1px;
    text-align: center;
    top: 1px;
    width: 24px;
    text-decoration: none;
    font-weight: bold;
    border-radius: 3px;
}

.close:hover {
    background: #FAAC58;
    color: #222;
}

.form-panel input, .form-panel textarea {
    margin-bottom: 15px;
}

/* Estilo para el scrollbar en el contenido del modal */
.modal-content-scrollable {
    max-height: 70vh;
    overflow-y: auto;
    padding-right: 15px;
}

/* Estilos personalizados para el scrollbar (opcional) */
.modal-content-scrollable::-webkit-scrollbar {
    width: 8px;
}

.modal-content-scrollable::-webkit-scrollbar-thumb {
    background-color: #FAAC58;
    border-radius: 4px;
}

.modal-content-scrollable::-webkit-scrollbar-track {
    background-color: #f1f1f1;
}
</style>