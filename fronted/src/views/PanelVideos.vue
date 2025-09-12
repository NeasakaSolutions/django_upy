<script setup>
import Header from '@/components/Header.vue';
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { ref, onMounted } from 'vue';
import axios from 'axios';
import { useAuthStore } from '@/stores/authStore';

// Validaciones de superusuario para el menu lateral
let store =useAuthStore();

const videos = ref([]);
const modal_titulo = ref('');
const video_id = ref(0);
const nombre = ref('');
const descripcion = ref('');
const id_youtube = ref('');
const video_file = ref(null);
const video_url_preview = ref(null);
const boton = ref('block');
const preloader = ref('none');

// Modal reactivo
const mostrarModal = ref(false);

// URL base de la API
const API_URL = import.meta.env.VITE_API_URL;

// --- Funciones ---
const cargarVideos = async () => {
    try {
        const respuesta = await axios.get(`${API_URL}videos`);
        videos.value = respuesta.data.data;
        console.log("Datos de videos recibidos:", videos.value);
    } catch (error) {
        console.error('Error al cargar los videos:', error);
        alert('Ocurrió un error al cargar los videos.');
    }
};

onMounted(() => {
    cargarVideos();
});

const crear = () => {
    modal_titulo.value = 'Añadir Nuevo Video';
    video_id.value = 0;
    nombre.value = '';
    descripcion.value = '';
    id_youtube.value = '';
    video_file.value = null;
    video_url_preview.value = null;
    mostrarModal.value = true;
};

const editar = (video) => {
    modal_titulo.value = 'Editar Video';
    video_id.value = video.id;
    nombre.value = video.nombre;
    descripcion.value = video.descripcion;
    id_youtube.value = video.id_youtube ? video.id_youtube.split('/').pop() : '';
    video_url_preview.value = video.video_url;
    video_file.value = null;
    mostrarModal.value = true;
};

const cerrarModal = () => {
    mostrarModal.value = false;
};

const handleFileChange = (event) => {
    video_file.value = event.target.files[0];
    if (video_file.value) {
        video_url_preview.value = URL.createObjectURL(video_file.value);
    }
};

const enviar = async () => {
    boton.value = "none";
    preloader.value = "block";

    const formData = new FormData();
    formData.append('nombre', nombre.value);
    formData.append('descripcion', descripcion.value);
    formData.append('id_youtube', id_youtube.value);
    if (video_file.value) formData.append('video', video_file.value);

    try {
        if (video_id.value) {
            await axios.put(`${API_URL}videos/${video_id.value}`, formData);
            alert("Se modificó el registro exitosamente");
        } else {
            await axios.post(`${API_URL}videos`, formData);
            alert("Se creó el registro exitosamente");
        }
        await cargarVideos();
        cerrarModal();
    } catch (err) {
        const errorMsg = err.response?.data?.error || "Ocurrió un error inesperado.";
        alert(`Error: ${errorMsg}`);
    } finally {
        boton.value = 'block';
        preloader.value = 'none';
    }
};

const eliminar = async (id) => {
    if (!confirm('¿Estás seguro de que quieres eliminar este video?')) return;
    try {
        await axios.delete(`${API_URL}videos/${id}`);
        alert("Video eliminado exitosamente.");
        await cargarVideos();
    } catch (error) {
        console.error(error.response || error);
        alert('Error al eliminar el video: ' + (error.response?.data?.message || error.message));
    }
};
</script>

<template>
<Header />
<Fondo />

<div class="container my-5 d-flex flex-wrap gap-4">
    <div class="contenedor_blog_articulos flex-grow-1">
        <h5 class="titulos my-3">Panel de Videos</h5>
        <div class="row">
            <div class="col-12 d-flex justify-content-end mb-4">
                <button @click="crear" class="btn btn-outline-warning">Añadir Video</button>
            </div>
            <hr />

            <div class="col-12">
                <div class="table-responsive">
                    <table class="table table-bordered table-striped table-hover align-middle text-center">
                        <thead class="table-warning">
                            <tr>
                                <th>ID</th>
                                <th>Nombre</th>
                                <th>Video</th>
                                <th>Acciones</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr v-if="videos.length === 0">
                                <td colspan="4">No hay videos para mostrar.</td>
                            </tr>
                            <tr v-for="video in videos" :key="video.id">
                                <td>{{ video.id }}</td>
                                <td>{{ video.nombre }}</td>
                                <td class="text-center">
                                    <video v-if="video.video_url.includes('uploads/videos')" width="160" height="90" :src="video.video_url" controls></video>
                                    <iframe v-else width="160" height="90" :src="video.video_url" frameborder="0" allowfullscreen></iframe>
                                </td>
                                <td class="text-center">
                                    <a href="#" @click.prevent="editar(video)" class="text-warning">
                                        <i class="fas fa-edit"></i>
                                    </a>
                                    &nbsp;&nbsp;
                                    <a href="#" @click.prevent="eliminar(video.id)" class="text-danger">
                                        <i class="fas fa-trash"></i>
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

<!-- Modal -->
<div v-if="mostrarModal" class="modalmask">
    <div class="modalbox rotate">
        <button @click="cerrarModal" class="close">X</button>
        <h2>{{ modal_titulo }}</h2>
        <div class="modal-content-scrollable">
            <form @submit.prevent="enviar">
                <div class="form-panel">
                    <div class="row container">
                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">Nombre:</label>
                            <input type="text" v-model="nombre" class="form-control" required />
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">Descripción:</label>
                            <textarea v-model="descripcion" class="form-control" rows="4"></textarea>
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">Link o ID de YouTube:</label>
                            <input type="text" v-model="id_youtube" class="form-control" />
                        </div>
                        <div class="col-12 mb-3">
                            <label class="form-label fw-bold">O subir archivo de video:</label>
                            <input type="file" @change="handleFileChange" accept="video/*" class="form-control" />
                        </div>
                        <div v-if="video_url_preview" class="col-12 text-center my-3">
                            <h6 class="fw-bold">Video Actual:</h6>
                            <video v-if="video_url_preview.includes('uploads/videos')" width="320" height="180" :src="video_url_preview" controls></video>
                            <iframe v-else width="320" height="180" :src="video_url_preview" frameborder="0" allowfullscreen></iframe>
                        </div>
                        <div class="col-12 text-center" :style="'display:' + boton">
                            <button class="btn btn-outline-warning" type="submit">Enviar</button>
                        </div>
                        <div class="col-12 text-center" :style="'display:' + preloader">
                            <img src="/img/img/load.gif" alt="Cargando..." />
                        </div>
                        <div class="col-12 text-center mt-3">
                            <button type="button" class="btn btn-outline-secondary" @click="cerrarModal">Cerrar</button>
                        </div>
                    </div>
                </div>
            </form>
        </div>
    </div>
</div>

<Fotter />
</template>

<style scoped>
.contenedor_blog_articulos{ width: 70%; }


.modalmask {
    position: fixed;
    top:0; left:0; right:0; bottom:0;
    background: rgba(0,0,0,0.8);
    z-index:9999;
    display:flex;
    align-items:center;
    justify-content:center;
}

.modalbox {
    width: 600px;
    padding:13px 20px;
    background:#fff;
    border-radius:3px;
    position:relative;
}

.close {
    background:#606061;
    color:#fff;
    line-height:25px;
    position:absolute;
    right:5px;
    top:5px;
    width:24px;
    border-radius:3px;
    font-weight:bold;
    cursor:pointer;
}
.close:hover { background:#FAAC58; color:#222; }

.modal-content-scrollable { max-height:70vh; overflow-y:auto; padding-right:15px; }
.modal-content-scrollable::-webkit-scrollbar { width:8px; }
.modal-content-scrollable::-webkit-scrollbar-thumb { background-color:#FAAC58; border-radius:4px; }
.modal-content-scrollable::-webkit-scrollbar-track { background-color:#f1f1f1; }
</style>


