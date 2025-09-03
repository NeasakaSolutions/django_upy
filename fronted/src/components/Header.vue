<!--Cargar referencias javascript-->
<script setup>
import router from '@/router';
import { blogsComposable } from '@/componsables/blogsComponsable';
import { watchEffect, ref } from 'vue';
import { Form, Field } from 'vee-validate'
//
import { useAuthStore } from '@/stores/authStore';


const {datos: datos, categorias: categorias, error: error} = blogsComposable();

watchEffect(() =>{
    if(error.value){
        //console.log("error con la api" + error.value);
        window.location = "/error";
    }
});

// Variables reactivas
let categoria_id = ref('0');
let search = ref('');

let enviar = () => {
    //console.log(`categoria_id = ${categoria_id.value} | search = ${search.value}`);
    if(categoria_id.value != "0"){
        window.location=`/blogs/buscador?categoria_id=${categoria_id.value}&search=${search.value}`
    }
};

//
let store = useAuthStore();

</script>

<!--Codigo fuente-->
<template>
    <header>
            <nav class="navbar navbar-expand-lg navbar-dark bg-dark fixed-top">
                <div class="container-fluid">

                    <!-- Configuracion para el logotipo del menu-->
                    <router-link to = '/' title = "Home" class="navbar-brand">
                        <img src="/img/core-img/favicon.ico"
                            alt="Logotipo de la Universidad Politecnica de Yucatan" width="50px">
                    </router-link>

                    <!-- Configuracion responsiva -->
                    <button class="navbar-toggler" type="button" data-bs-toggle="collapse" data-bs-target="#menu"
                        aria-controls="menu" aria-expanded="false" aria-label="Mostrar / Ocultar Menu">
                        <span class="navbar-toggler-icon"></span>
                    </button>

                    <!-- Menu de navegacion -->
                    <div class="collapse navbar-collapse justify-content-end" id="menu">
                        <ul class="navbar-nav me-auto mb-2 mb-lg-0">
                            <li class="nav-item"><router-link :to = "{name: 'blogs'}" class="nav-link">Blogs</router-link></li>
                            <li class="nav-item"><router-link :to = "{name: 'videos'}" class="nav-link">Videos</router-link></li>
                            <li class="nav-item"><router-link :to = "{name: 'contacto'}" class="nav-link">Contacto</router-link></li>
                            <li v-if = "store.authId==null" class="nav-item"><router-link :to = "{name: 'login'}" class="nav-link">Iniciar sesión</router-link></li>
                            <li v-if = "store.authId==null" class="nav-item"><router-link :to = "{name: 'registro'}" class="nav-link">Registrarse</router-link></li>
                            <li v-if = "store.authId!=null" class="nav-item"><router-link :to = "{name: 'panel'}" class="nav-link">{{ 'Hola ' + store.authNombre }}</router-link></li>
                            <li v-if = "store.authId!=null" class="nav-item">
                                <router-link @click = "store.cerrarSesion()" to = "#" class="nav-link">Cerrar sesión</router-link>
                            </li>
                        </ul>

                        <!-- Formulario combinado en horizontal -->
                        <Form @submit="enviar" class="d-flex align-items-center gap-2 flex-wrap flex-lg-nowrap" role="search">

                            <!-- Campo de búsqueda -->
                            <Field as = "input" v-model = "search" type = "text" name = "search" id = "search" class = "form-control" 
                                placeholder="Buscar..." aria-label="Buscar" style="min-width: 200px;"/>

                            <!-- Selector de categorías -->
                            <Field as = "select" v-model = "categoria_id" class = "form-select" name = "categoria_id" 
                                placeholder = "Seleccionar categoria..." style="min-width: 200px;">
                            <option value = "0">Todas las categorías</option>
                            <option v-for ="(categoria, index) in categorias.data" :key = "index" :value = "categoria.id">
                                {{ categoria.nombre }}
                            </option>
                            </Field>

                            <!-- Botón único -->
                            <button class="btn btn-outline-light px-3" type="submit" style="white-space: nowrap;">
                                <i class = "fas fa-search"></i>     Buscar
                            </button>
                        </Form>


                    </div>
                </div>
            </nav>
    </header>
</template>
