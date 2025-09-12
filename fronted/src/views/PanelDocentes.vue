<script setup>
import Header from '@/components/Header.vue';
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { getPortadaById } from '@/services/portadaService';
import { Form, Field } from 'vee-validate';
import { useRoute } from 'vue-router';
import { useAuthStore } from '@/stores/authStore';
import { onMounted, ref } from 'vue';
import axios from 'axios';
import { Fancybox } from '@fancyapps/ui';
import "@fancyapps/ui/dist/fancybox.css";

// Estado reactivo para docentes y la interfaz de usuario
let datos = ref([]);
let modal_titulo = ref('');
let nombre = ref('');
let area = ref('');
let docente_id = ref(0);
let boton = ref('block');
let preloader = ref('none');
let imagen_preview = ref(''); // Variable para la vista previa de la imagen
let modal_abierto = ref(false); // Nuevo estado para controlar la visibilidad del modal

// Estado reactivo para la nueva tabla de laboratorios
let laboratorios = ref([]);
let lab_nombre = ref('');
let lab_descripcion = ref('');
let lab_id = ref(0);
let lab_imagen_preview = ref('');
let lab_modal_abierto = ref(false);
let lab_modal_titulo = ref('');

// --- NUEVO ESTADO PARA COLABORADORES ---
let colaboradores = ref([]);
let col_nombre = ref('');
let col_id = ref(0);
let col_imagen_preview = ref('');
let col_modal_abierto = ref(false);
let col_modal_titulo = ref('');

// Estado reactivo para portadas (sin cambios)
let portada = ref(null);
let store = useAuthStore();
const ID_PORTADA = 5;

// Función para cargar los datos de los docentes desde la API
const cargarDocentes = async () => {
    try {
        let respuesta = await fetch(`${import.meta.env.VITE_API_URL}docentes`);
        const datosJSON = await respuesta.json();
        datos.value = datosJSON.data;
    } catch (error) {
        console.error("Error al cargar los docentes:", error);
    }
};

// --- LÓGICA CRUD DE DOCENTES (SIN CAMBIOS) ---
const cerrarModal = () => {
    modal_abierto.value = false;
};

const enviarDocente = async () => {
    boton.value = 'none';
    preloader.value = 'block';

    const formData = new FormData();
    formData.append('nombre', nombre.value);
    formData.append('area', area.value);
    const file_foto = document.querySelector("#file_foto").files[0];
    if (file_foto) {
        formData.append('foto', file_foto);
    }

    if (modal_titulo.value === 'Crear Docente') {
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}docentes`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Se creó el docente exitosamente.");
            cerrarModal();
            cargarDocentes();
        } catch (err) {
            alert("Ocurrió un error al crear el docente: " + err);
        }
    } else if (modal_titulo.value === 'Editar Docente') {
        try {
            await axios.put(`${import.meta.env.VITE_API_URL}docentes/${docente_id.value}`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Se modificó el docente exitosamente.");
            cerrarModal();
            cargarDocentes();
        } catch (err) {
            alert("Ocurrió un error al editar el docente: " + err);
        }
    }

    boton.value = 'block';
    preloader.value = 'none';
};

const crear = () => {
    modal_titulo.value = 'Crear Docente';
    nombre.value = '';
    area.value = '';
    imagen_preview.value = '';
    modal_abierto.value = true;
};

const editar = (docente) => {
    modal_titulo.value = 'Editar Docente';
    docente_id.value = docente.id;
    nombre.value = docente.nombre;
    area.value = docente.area;
    imagen_preview.value = docente.imagen;
    modal_abierto.value = true;
};

const handleFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            imagen_preview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

const eliminar = async (id) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este docente?")) {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}docentes/${id}`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}` }
            });
            alert("Se eliminó el docente exitosamente.");
            cargarDocentes();
        } catch (err) {
            alert("Ocurrió un error al eliminar el docente: " + err);
        }
    }
};

// --- LÓGICA CRUD DE LABORATORIOS ---
const cargarLaboratorios = async () => {
    try {
        let respuesta = await fetch(`${import.meta.env.VITE_API_URL}laboratorios`);
        const datosJSON = await respuesta.json();
        laboratorios.value = datosJSON.data;
    } catch (error) {
        console.error("Error al cargar los laboratorios:", error);
    }
};

const crearLab = () => {
    lab_modal_titulo.value = 'Crear Laboratorio';
    lab_nombre.value = '';
    lab_descripcion.value = '';
    lab_imagen_preview.value = '';
    lab_modal_abierto.value = true;
};

const editarLab = (laboratorio) => {
    lab_modal_titulo.value = 'Editar Laboratorio';
    lab_id.value = laboratorio.id;
    lab_nombre.value = laboratorio.nombre;
    lab_descripcion.value = laboratorio.descripcion;
    lab_imagen_preview.value = laboratorio.imagen;
    lab_modal_abierto.value = true;
};

const enviarLaboratorio = async () => {
    boton.value = 'none';
    preloader.value = 'block';

    const formData = new FormData();
    formData.append('nombre', lab_nombre.value);
    formData.append('descripcion', lab_descripcion.value);
    const file_foto = document.querySelector("#file_lab_foto").files[0];
    if (file_foto) {
        formData.append('foto', file_foto);
    }

    if (lab_modal_titulo.value === 'Crear Laboratorio') {
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}laboratorios`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Se creó el laboratorio exitosamente.");
            cerrarLabModal();
            cargarLaboratorios();
        } catch (err) {
            alert("Ocurrió un error al crear el laboratorio: " + err);
        }
    } else if (lab_modal_titulo.value === 'Editar Laboratorio') {
        try {
            await axios.put(`${import.meta.env.VITE_API_URL}laboratorios/${lab_id.value}`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Se modificó el laboratorio exitosamente.");
            cerrarLabModal();
            cargarLaboratorios();
        } catch (err) {
            alert("Ocurrió un error al editar el laboratorio: " + err);
        }
    }

    boton.value = 'block';
    preloader.value = 'none';
};

const eliminarLab = async (id) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este laboratorio?")) {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}laboratorios/${id}`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}` }
            });
            alert("Se eliminó el laboratorio exitosamente.");
            cargarLaboratorios();
        } catch (err) {
            alert("Ocurrió un error al eliminar el laboratorio: " + err);
        }
    }
};

const cerrarLabModal = () => {
    lab_modal_abierto.value = false;
};

const handleLabFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            lab_imagen_preview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

// --- NUEVA LÓGICA CRUD DE COLABORADORES ---
const cargarColaboradores = async () => {
    try {
        const respuesta = await fetch(`${import.meta.env.VITE_API_URL}colaboradores`);
        const datosJSON = await respuesta.json();
        colaboradores.value = datosJSON.data;
    } catch (error) {
        console.error("Error al cargar los colaboradores:", error);
    }
};

const crearCol = () => {
    col_modal_titulo.value = 'Crear Colaborador';
    col_nombre.value = '';
    col_imagen_preview.value = '';
    col_modal_abierto.value = true;
};

const editarCol = (colaborador) => {
    col_modal_titulo.value = 'Editar Colaborador';
    col_id.value = colaborador.id;
    col_nombre.value = colaborador.nombre;
    // Usa la propiedad "foto" que viene de la API
    col_imagen_preview.value = colaborador.foto;
    col_modal_abierto.value = true;
};

const enviarColaborador = async () => {
    boton.value = 'none';
    preloader.value = 'block';

    const formData = new FormData();
    formData.append('nombre', col_nombre.value);
    const file_foto = document.querySelector("#file_col_foto").files[0];
    if (file_foto) {
        formData.append('foto', file_foto);
    }

    if (col_modal_titulo.value === 'Crear Colaborador') {
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}colaboradores`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Se creó el colaborador exitosamente.");
            cerrarColModal();
            cargarColaboradores();
        } catch (err) {
            alert("Ocurrió un error al crear el colaborador: " + err);
        }
    } else if (col_modal_titulo.value === 'Editar Colaborador') {
        try {
            await axios.put(`${import.meta.env.VITE_API_URL}colaboradores/${col_id.value}`, formData, {
                headers: {
                    'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`,
                    'Content-Type': 'multipart/form-data'
                }
            });
            alert("Se modificó el colaborador exitosamente.");
            cerrarColModal();
            cargarColaboradores();
        } catch (err) {
            alert("Ocurrió un error al editar el colaborador: " + err);
        }
    }

    boton.value = 'block';
    preloader.value = 'none';
};

const eliminarCol = async (id) => {
    if (window.confirm("¿Estás seguro de que quieres eliminar este colaborador?")) {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}colaboradores/${id}`, {
                headers: { 'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}` }
            });
            alert("Se eliminó el colaborador exitosamente.");
            cargarColaboradores();
        } catch (err) {
            alert("Ocurrió un error al eliminar el colaborador: " + err);
        }
    }
};

const cerrarColModal = () => {
    col_modal_abierto.value = false;
};

const handleColFileChange = (event) => {
    const file = event.target.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = (e) => {
            col_imagen_preview.value = e.target.result;
        };
        reader.readAsDataURL(file);
    }
};

// Carga de datos al montar el componente
onMounted(async () => {
    portada.value = await getPortadaById(ID_PORTADA);
    cargarDocentes();
    cargarLaboratorios();
    cargarColaboradores();
});

// Limitar descripcion:
const truncate = (text, length = 100) => {
  if (!text) return '';
  return text.length > length ? text.substring(0, length) + '...' : text;
};
</script>

<template>
<Header></Header>
<Fondo></Fondo>
<div class="container my-5 d-flex flex-wrap gap-4">
    <div class="contenedor_blog_articulos flex-grow-1">
        
         <h5 class="titulos my-3">Panel de la página principal</h5>

        <div class="d-flex align-items-center gap-3 my-5">
            <div class="col-3">
                <div class="text-right my-5">
                    <a @click.prevent="crear()" class="btn btn-outline-warning text-nowrap">
                        <i class="fas fa-plus"></i> Crear Docente
                    </a>
                </div>
            </div>
             <div class="col-3">
                <div class="text-right my-5">
                    <a @click.prevent="crearCol()" class="btn btn-outline-warning text-nowrap">
                        <i class="fas fa-plus"></i> Crear Colaborador
                    </a>
                </div>
            </div>
            <div class="col-2">
                <div class="text-right my-5">
                    <a class="btn btn-outline-warning">
                        <router-link :to="{ name: 'panel' }" class="nav-link">Blogs</router-link>
                    </a>
                </div>
            </div>
            <div class="col-2">
                <div class="text-right my-5">
                    <a class="btn btn-outline-warning">
                        <router-link :to="{ name: 'panelPortadas' }" class="nav-link">Portadas</router-link>
                    </a>
                </div>
            </div>
        </div>

        <hr />

        <div class="col-12">
            <h3>Gestión de Docentes</h3>
            <div class="table-responsive">
                <table class="table table-bordered table-striped table-hover align-middle text-center">
                    <thead class="table-warning">
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Área</th>
                            <th>Foto</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(dato, index) in datos" :key="index">
                            <td>{{ dato.id }}</td>
                            <td>{{ dato.nombre }}</td>
                            <td>{{ dato.area }}</td>
                            <td class="text-center">
                                <a :href="dato.imagen" class="lightbox d-block" data-fancybox="image-gallery">
                                    <img :src="dato.imagen" :alt="dato.nombre" style="width: 100px;">
                                </a>
                            </td>
                            <td class="text-center">
                                <a href="#" @click.prevent="editar(dato)" title="Editar" class="text-warning">
                                    <i class="fas fa-edit"></i>
                                </a>
                                &nbsp;&nbsp;
                                <a href="#" @click.prevent="eliminar(dato.id)" title="Eliminar" class="text-danger">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <hr />

        <div class="col-12">
            <h3>Gestión de Laboratorios</h3>
            <div class="col-3">
                <div class="text-right my-5">
                    <a @click.prevent="crearLab()" class="btn btn-outline-warning text-nowrap">
                        <i class="fas fa-plus"></i> Crear Laboratorio
                    </a>
                </div>
            </div>
            <div class="table-responsive">
                <table class="table table-bordered table-striped table-hover align-middle text-center">
                    <thead class="table-warning">
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Descripción</th>
                            <th>Foto</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(lab, index) in laboratorios" :key="index">
                            <td>{{ lab.id }}</td>
                            <td>{{ lab.nombre }}</td>
                            <td>{{ truncate(lab.descripcion, 50) }}</td>
                            <td class="text-center">
                                <a :href="lab.imagen" class="lightbox d-block" data-fancybox="lab-image-gallery">
                                    <img :src="lab.imagen" :alt="lab.nombre" style="width: 100px;">
                                </a>
                            </td>
                            <td class="text-center">
                                <a href="#" @click.prevent="editarLab(lab)" title="Editar" class="text-warning">
                                    <i class="fas fa-edit"></i>
                                </a>
                                &nbsp;&nbsp;
                                <a href="#" @click.prevent="eliminarLab(lab.id)" title="Eliminar" class="text-danger">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
            </div>
        </div>

        <hr />

        <div class="col-12">
            <h3>Gestión de Colaboradores</h3>
            <div class="text-right my-3">
                <a @click.prevent="crearCol()" class="btn btn-outline-warning text-nowrap">
                    <i class="fas fa-plus"></i> Crear Colaborador
                </a>
            </div>
            <div class="table-responsive">
                <table class="table table-bordered table-striped table-hover align-middle text-center">
                    <thead class="table-warning">
                        <tr>
                            <th>ID</th>
                            <th>Nombre</th>
                            <th>Logo</th>
                            <th>Acciones</th>
                        </tr>
                    </thead>
                    <tbody>
                        <tr v-for="(col, index) in colaboradores" :key="index">
                            <td>{{ col.id }}</td>
                            <td>{{ col.nombre }}</td>
                            <td class="text-center">
                                <a :href="col.imagen" class="lightbox d-block" data-fancybox="col-image-gallery">
                                    <img :src="col.imagen" :alt="col.nombre" style="width: 100px;">
                                </a>
                            </td>
                            <td class="text-center">
                                <a href="#" @click.prevent="editarCol(col)" title="Editar" class="text-warning">
                                    <i class="fas fa-edit"></i>
                                </a>
                                &nbsp;&nbsp;
                                <a href="#" @click.prevent="eliminarCol(col.id)" title="Eliminar" class="text-danger">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </td>
                        </tr>
                    </tbody>
                </table>
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

<Fotter></Fotter>

<div class="modalmask" v-if="modal_abierto">
    <div class="modalbox rotate">
        <a @click.prevent="cerrarModal()" title="Cerrar" class="close">X</a>
        <h2>{{ modal_titulo }}</h2>
        <Form @submit="enviarDocente()">
            <div class="form-panel">
                <div class="row container">
                    <div class="col-12 col-lg-12">
                        <label for="nombre" class="form-label fw-bold">Nombre</label>
                        <Field type="text" name="nombre" v-model="nombre" placeholder="Nombre del docente" class="form-control" />
                    </div>
                    <div class="col-12 col-lg-12 mt-3">
                        <label for="area" class="form-label fw-bold">Área</label>
                        <Field as="textarea" name="area" v-model="area" placeholder="Área del docente" class="form-control" />
                    </div>
                    <div class="col-12 col-lg-12 mt-3">
                        <label for="file_foto" class="form-label fw-bold">
                            {{ modal_titulo === 'Crear Docente' ? 'Subir foto:' : 'Cambiar foto:' }}
                        </label>
                        <input type="file" name="foto" id="file_foto" class="form-control" @change="handleFileChange" />
                        <div v-if="imagen_preview" class="mt-3 text-center">
                            <label class="form-label fw-bold">Vista previa:</label>
                            <img :src="imagen_preview" alt="Vista previa de la foto" class="img-fluid rounded" style="max-height: 100px; display: block; margin: 0 auto;" />
                        </div>
                    </div>
                    <div class="col-12 text-center mt-4" :style="{ display: boton }">
                        <button class="btn btn-outline-warning" type="submit" title="Enviar">
                            Enviar
                        </button>
                    </div>
                    <div class="col-12 text-center" :style="{ display: preloader }">
                        <img src="/img/img/load.gif" alt="Cargando" />
                    </div>
                </div>
            </div>
        </Form>
    </div>
</div>

<div class="modalmask" v-if="lab_modal_abierto">
    <div class="modalbox rotate">
        <a @click.prevent="cerrarLabModal()" title="Cerrar" class="close">X</a>
        <h2>{{ lab_modal_titulo }}</h2>
        <Form @submit="enviarLaboratorio()">
            <div class="form-panel">
                <div class="row container">
                    <div class="col-12 col-lg-12">
                        <label for="lab_nombre" class="form-label fw-bold">Nombre</label>
                        <Field type="text" name="lab_nombre" v-model="lab_nombre" placeholder="Nombre del laboratorio" class="form-control" />
                    </div>
                    <div class="col-12 col-lg-12 mt-3">
                        <label for="lab_descripcion" class="form-label fw-bold">Descripción</label>
                        <Field as="textarea" name="lab_descripcion" v-model="lab_descripcion" placeholder="Descripción del laboratorio" class="form-control" />
                    </div>
                    <div class="col-12 col-lg-12 mt-3">
                        <label for="file_lab_foto" class="form-label fw-bold">
                            {{ lab_modal_titulo === 'Crear Laboratorio' ? 'Subir imagen:' : 'Cambiar imagen:' }}
                        </label>
                        <input type="file" name="foto" id="file_lab_foto" class="form-control" @change="handleLabFileChange" />
                        <div v-if="lab_imagen_preview" class="mt-3 text-center">
                            <label class="form-label fw-bold">Vista previa:</label>
                            <img :src="lab_imagen_preview" alt="Vista previa del laboratorio" class="img-fluid rounded" style="max-height: 100px; display: block; margin: 0 auto;" />
                        </div>
                    </div>
                    <div class="col-12 text-center mt-4" :style="{ display: boton }">
                        <button class="btn btn-outline-warning" type="submit" title="Enviar">
                            Enviar
                        </button>
                    </div>
                    <div class="col-12 text-center" :style="{ display: preloader }">
                        <img src="/img/img/load.gif" alt="Cargando" />
                    </div>
                </div>
            </div>
        </Form>
    </div>
</div>

<div class="modalmask" v-if="col_modal_abierto">
    <div class="modalbox rotate">
        <a @click.prevent="cerrarColModal()" title="Cerrar" class="close">X</a>
        <h2>{{ col_modal_titulo }}</h2>
        <Form @submit="enviarColaborador()">
            <div class="form-panel">
                <div class="row container">
                    <div class="col-12 col-lg-12">
                        <label for="col_nombre" class="form-label fw-bold">Nombre</label>
                        <Field type="text" name="col_nombre" v-model="col_nombre" placeholder="Nombre del colaborador" class="form-control" />
                    </div>
                    <div class="col-12 col-lg-12 mt-3">
                        <label for="file_col_foto" class="form-label fw-bold">
                            {{ col_modal_titulo === 'Crear Colaborador' ? 'Subir logo:' : 'Cambiar logo:' }}
                        </label>
                        <input type="file" name="foto" id="file_col_foto" class="form-control" @change="handleColFileChange" />
                        <div v-if="col_imagen_preview" class="mt-3 text-center">
                            <label class="form-label fw-bold">Vista previa:</label>
                            <img :src="col_imagen_preview" alt="Vista previa del logo" class="img-fluid rounded" style="max-height: 100px; display: block; margin: 0 auto;" />
                        </div>
                    </div>
                    <div class="col-12 text-center mt-4" :style="{ display: boton }">
                        <button class="btn btn-outline-warning" type="submit" title="Enviar">
                            Enviar
                        </button>
                    </div>
                    <div class="col-12 text-center" :style="{ display: preloader }">
                        <img src="/img/img/load.gif" alt="Cargando" />
                    </div>
                </div>
            </div>
        </Form>
    </div>
</div>
</template>

<style scoped>
/* Estilos que ya tenías para el modal, se mantienen */
.modalmask {
    position: fixed;
    font-family: Arial, sans-serif;
    top: 0;
    right: 0;
    bottom: 0;
    left: 0;
    background: rgba(0, 0, 0, 0.8);
    z-index: 99999;
    opacity: 1;
    -webkit-transition: opacity 400ms ease-in;
    -moz-transition: opacity 400ms ease-in;
    transition: opacity 400ms ease-in;
    pointer-events: auto;
}
.modalbox {
    width: 600px;
    position: relative;
    padding: 5px 20px 13px 20px;
    background: #fff;
    border-radius: 3px;
    -webkit-transition: all 500ms ease-in;
    -moz-transition: all 500ms ease-in;
    transition: all 500ms ease-in;
    max-height: 90vh;
    overflow-y: auto;
    margin: 1% auto;
}

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
</style>