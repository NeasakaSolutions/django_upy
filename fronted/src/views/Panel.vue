<script setup>
import Header from '@/components/Header.vue'
import Fondo from '@/components/Fondo.vue';
import Fotter from '@/components/Fotter.vue';
import { useAuthStore } from '@/stores/authStore';
import { onMounted, ref } from 'vue';
import { Form, Field, ErrorMessage } from 'vee-validate';
import { blogsSchema } from '@/schemas/validacionesSchema';
import axios from 'axios';
import { Fancybox } from '@fancyapps/ui'
import "@fancyapps/ui/dist/fancybox.css"
import { categoriasSchema } from '@/schemas/categoriasSchema';

// Validaciones de superusuario para el menu lateral
let store =useAuthStore();

// Devolver todos los blogs del usuario logeado
let datos = ref([]);
let categorias = ref([]);

onMounted(async()=>{
  let respuesta = await fetch(`${import.meta.env.VITE_API_URL}blogs-panel/${localStorage.getItem('blogs_flaites_id')}`, {
    headers: {'content-type': 'application/json', 'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`}
  });
  datos.value = await respuesta.json();

  let respuesta2 = await fetch(`${import.meta.env.VITE_API_URL}categorias`, {
    headers: {'content-type': 'application/json'}
  });
  categorias.value = await respuesta2.json();
});

// Formulario
let nombre = ref('');
let descripcion = ref('');
let categoria_id = ref('0');
let blogs_id=ref('0');
let boton = ref('block');
let preloader = ref('none');

let enviar =()=>{
  boton.value="none";
  preloader.value="block";

  if(modal_titulo.value=="Crear"){
    let file_foto = document.querySelector("#file_foto").files[0];
    let file_documento = document.querySelector("#file_documento").files[0];
    let formData = new FormData();
    formData.append('foto', file_foto);
    formData.append('documento', file_documento);
    formData.append('categoria_id', categoria_id.value);
    formData.append('nombre', nombre.value);
    formData.append('descripcion', descripcion.value)

    axios.post(`${import.meta.env.VITE_API_URL}blogs`, formData, {headers: {'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`}})
    .then((response)=>{
      alert("Se creó el registro exitosamente");
      window.location="/panel";
    })
    .catch((err)=>{
      alert("Ocurrio un error inesperado" + err);
      window.location="/panel";
    });
    
  }
  if(modal_titulo.value=="Editar"){
    axios.put(`${import.meta.env.VITE_API_URL}blogs/${blogs_id.value}`, {nombre: nombre.value, descripcion: descripcion.value, categoria_id: categoria_id.value}, 
    {headers: {'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`}})
    .then((response)=>{
      alert("Se modificó el registro exitosamente");
      window.location="/panel";
    })
    .catch((err)=>{
      alert("Ocurrio un error inesperado" + err);
      window.location="/panel";
    });
  }
};

// Ventana modal
let modal_titulo = ref('');
let crear = ()=>{
  modal_titulo.value='Crear';
  categoria_id.value="0";
  nombre.value='';
  descripcion.value='';
};

let editar = (modelo)=>{
  modal_titulo.value='Editar';
  blogs_id.value=modelo.id;
  categoria_id.value=modelo.categoria_id;
  nombre.value=modelo.nombre;
  descripcion.value=modelo.descripcion;
};

const eliminar=(id)=>{
  if(window.confirm("¿Eliminar registro?")){
    axios.delete(`${import.meta.env.VITE_API_URL}blogs/${id}`, 
    {headers: {'Authorization': `Bearer ${localStorage.getItem('blogs_flaites_token')}`}})
    .then((response)=>{
      alert("Se eliminó el registro exitosamente");
      window.location="/panel";
    })
    .catch((err)=>{
      alert("Ocurrio un error inesperado" + err);
      window.location="/panel";
    });
  }
};

const categoria_id_modal = ref(0);
const nombre_categoria = ref('');
const modal_titulo_categoria = ref('');
const boton_categoria = ref('block');
const preloader_categoria = ref('none');

// Variables para la lista de categorías en el modal
let listaCategorias = ref([]);
const mostrarListaCategorias = ref(false); // Nueva variable para controlar la vista del modal

// Función para abrir el modal de categorías
const crearCategoria = async () => {
    modal_titulo_categoria.value = 'Crear Categoría';
    nombre_categoria.value = '';
    mostrarListaCategorias.value = false; // Oculta la lista al crear una nueva
};

// Función para abrir el modal con la lista de categorías
const abrirModalCategorias = async () => {
    modal_titulo_categoria.value = 'Gestión de Categorías';
    mostrarListaCategorias.value = true; // Muestra la lista
    // Obtener las categorías de la API
    try {
        const respuesta = await axios.get(`${import.meta.env.VITE_API_URL}categorias`);
        listaCategorias.value = respuesta.data.data;
    } catch (error) {
        alert("Ocurrió un error al cargar las categorías.");
    }
};

const editarCategoria = (modelo) => {
    modal_titulo_categoria.value = 'Editar Categoría';
    categoria_id_modal.value = modelo.id;
    nombre_categoria.value = modelo.nombre;
    mostrarListaCategorias.value = false; // Oculta la lista para mostrar el formulario de edición
};

const enviarCategoria = async () => {
    boton_categoria.value = "none";
    preloader_categoria.value = "block";

    if (modal_titulo_categoria.value === "Crear Categoría") {
        try {
            await axios.post(`${import.meta.env.VITE_API_URL}categorias`, { nombre: nombre_categoria.value });
            alert("Se creó la categoría exitosamente");
            window.location = "/panel";
        } catch (err) {
            alert("Ocurrió un error inesperado al crear la categoría: " + err);
            window.location = "/panel";
        }
    }

    if (modal_titulo_categoria.value === "Editar Categoría") {
        try {
            await axios.put(`${import.meta.env.VITE_API_URL}categorias/${categoria_id_modal.value}`, { nombre: nombre_categoria.value });
            alert("Se modificó la categoría exitosamente");
            window.location = "/panel";
        } catch (err) {
            alert("Ocurrió un error inesperado al editar la categoría: " + err);
            window.location = "/panel";
        }
    }
};

const eliminarCategoria = async (id) => {
    if (window.confirm("¿Eliminar categoría?")) {
        try {
            await axios.delete(`${import.meta.env.VITE_API_URL}categorias/${id}`);
            alert("Se eliminó la categoría exitosamente");
            window.location = "/panel";
        } catch (err) {
            alert("Ocurrió un error inesperado al eliminar la categoría: " + err);
            window.location = "/panel";
        }
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

        <div class="row">
          <div class="col-2">
              <div class="text-right my-5">
                  <a href="#modal2" @click="crear()" class="btn btn-outline-warning">
                      <i class="fas fa-plus"></i> Crear
                  </a>
              </div>
          </div>

          <div class="col-2">
            <div class="text-right my-5">
                <a href="#modal3" @click="abrirModalCategorias()" class="btn btn-outline-warning">
                    Categorías
                </a>
            </div>
        </div>

        <div class="modalmask" id="modal3">
            <div class="modalbox rotate">
                <a href="#close" title="Cerrar" class="close">X</a>
                <h2>{{ modal_titulo_categoria }}</h2>

                <div v-if="mostrarListaCategorias" class="modal-listado">
                    <p>
                        <a href="#modal3" @click="crearCategoria()" class="btn btn-outline-warning">
                            <i class="fas fa-plus"></i> Crear nueva
                        </a>
                    </p>
                    <ul class="list-group">
                        <li v-for="(categoria, index) in listaCategorias" :key="index" class="list-group-item d-flex justify-content-between align-items-center">
                            {{ categoria.nombre }}
                            <div>
                                <a href="#modal3" title="Editar" @click="editarCategoria(categoria)" class="btn btn-sm btn-outline-warning me-2">
                                    <i class="fas fa-edit"></i>
                                </a>
                                <a href="#" @click.prevent="eliminarCategoria(categoria.id)" title="Eliminar" class="btn btn-sm btn-outline-danger">
                                    <i class="fas fa-trash"></i>
                                </a>
                            </div>
                        </li>
                    </ul>
                </div>

                <div v-else>
                    <Form :validation-schema="categoriasSchema" @submit="enviarCategoria()">
                        <div class="form-panel">
                            <div class="row container">
                                <div class="col-12 col-lg-12">
                                    <ErrorMessage name="nombre" class="text text-warning" />
                                    <Field type="text" name="nombre" v-model="nombre_categoria" placeholder="Nombre de la categoría" class="form-control"></Field>
                                </div>

                                <div class="col-12 text-center" :style="'display:' + boton_categoria">
                                    <button class="btn btn-outline-warning" type="submit" title="Enviar">
                                        Enviar
                                    </button>
                                </div>
                                <div class="col-12 text-center" :style="'display:' + preloader_categoria">
                                    <img src="/img/img/load.gif" />
                                </div>
                            </div>
                        </div>
                    </Form>
                </div>
            </div>
        </div>
          
          <div class="col-2">
              <div class="text-right my-5">
                  <a href="#" class="btn btn-outline-warning"> 
                       <router-link :to = "{name: 'panelDocentes'}" class="nav-link">Principal</router-link>
                  </a>
              </div>
          </div>
          
          <div class="col-2">
              <div class="text-right my-5">
                  <a href="#" class="btn btn-outline-warning">
                       <router-link :to = "{name: 'panelPortadas'}" class="nav-link">Portadas</router-link>
                  </a>
              </div>
          </div>
          
          <div class="col-2">
              <div class="text-right my-5">
                  <a href="#" class="btn btn-outline-warning">
                       Videos
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
                  <th>Categoría</th>
                  <th>Nombre</th>
                  <th>Descripcion</th>
                  <th>Foto</th>
                  <th>Documento</th>
                  <th>Acciones</th>
                </tr>
              </thead>

              <tbody>
                <tr v-for="(dato, index) in datos.data" :key="index">
                  <td>{{  dato.id }}</td>
                  <td>{{  dato.categoria }}</td>
                  <td>{{  dato.nombre }}</td>
                  <td>{{  dato.descripcion }}</td>
                  <td class="text-center">
                    <a :href="dato.imagen" class="lightbox d-block" data-fancybox="image-gallery">
                      <img :src="dato.imagen" :alt="dato.nombre" style="width: 100px;"></img>
                    </a>
                  </td>
                  <td class="text-center">
                  <a v-if="dato.documento" :href="dato.documento" target="_blank">
                    Ver documento
                  </a>
                  <span v-else>No disponible</span>
                </td>
                <td class="text-center">
                  <!--AQUI VAN LOS BOTONES DE FONT AWESOME-->
                  <router-link :to="{name: 'panel_editar_foto', params:{id:dato.id}}" title="Editar foto" class="text-warning">
                    <i class="fa-solid fa-image"></i>
                  </router-link>
                  &nbsp;&nbsp;
                  <router-link :to="{name: 'panel_editar_documento', params:{id:dato.id}}" title="Editar documento" class="text-warning">
                    <i class="fa-solid fa-file"></i>
                  </router-link>
                  &nbsp;&nbsp;
                  <a href="#modal2" title="Editar" @click="editar(dato)" class="text-warning">
                    <i class="fas fa-edit"></i>
                  </a>
                  &nbsp;&nbsp;
                  <router-link to="#" @click.navigate="eliminar(dato.id)" title="Eliminar" class="text-danger">
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
  <!--modal-->
  <div class="modalmask" id="modal2">
    <div class="modalbox rotate">
      <a href="#close" title="Cerrar" class="close">X</a>
      <h2>{{ modal_titulo }}</h2>

      <!-- Inicio formulario -->
      <Form :validation-schema="blogsSchema" @submit="enviar()">
        <div class="form-panel">
        <div class="row container">

          <div class="col-12 col-lg-12">

            <ErrorMessage name="categoria_id" class="text text-warning" />
            <Field as="select" name="categoria_id" v-model="categoria_id" class="form-control"
              style="height: calc(2.25rem + 10px);">
              <option value="0">Selecciones...</option>
              <option v-for="(categoria, i) in categorias.data" :key="i" :value="categoria.id"> {{ categoria.nombre }}</option>
            </Field>

          </div>

          <div class="col-12 col-lg-12">

            <ErrorMessage name="nombre" class="text text-warning" />
            <Field type="text" name="nombre" v-model="nombre" placeholder="Nombre" class="form-control"></Field>

          </div>

          <div class="col-12 col-lg-12">

            <ErrorMessage name="descripcion" class="text text-warning" />
            <Field as="textarea" name="descripcion" v-model="descripcion" placeholder="Descripción" class="form-control area_mensaje"></Field>

          </div>

          <div v-if="modal_titulo == 'Crear'" class="col-12 col-lg-12">
            <label for="file_foto" class="form-label fw-bold">Subir foto:</label>
            <input type="file" name="foto" id="file_foto" class="form-control"></input>

          </div>

          <div v-if="modal_titulo == 'Crear'" class="col-12 col-lg-12">
            <label for="file_documento" class="form-label fw-bold">Subir documento:</label>
            <input type="file" name="documento" id="file_documento" class="form-control"></input>

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

        </div>
        </div>
      </Form>
      <!-- Final formulario -->
    </div>
  </div>
  <!--/modal-->


</template>

<style scoped>

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

/*-------------------------------------------------------------------------------------------------------------------- */
/* Presentación simple del formulario */

</style>
