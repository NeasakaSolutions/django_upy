// Importaciones
import { defineStore } from "pinia";


export const useAuthStore = defineStore('auth', {
    
    state: () => ({

        authId: (localStorage.getItem('blogs_flaites_id') != null) ? localStorage.getItem('blogs_flaites_id') : null,
        authNombre: (localStorage.getItem('blogs_flaites_nombre' != null)) ? localStorage.getItem('blogs_flaites_nombre') : null,
        authToken: (localStorage.getItem('blogs_flaites_token' != null)) ? localStorage.getItem('blogs_flaites_token') : null
    }),

    actions: {
        iniciarSesion(data){
            localStorage.setItem('blogs_flaites_id', data.id);
            localStorage.setItem('blogs_flaites_nombre', data.nombre);
            localStorage.setItem('blogs_flaites_token', data.token);
        },
        estasLogueado(){
            if(this.authId == null){
                window.location = "/login";
            }
            this.authId = localStorage.getItem('blogs_flaites_id');
            this.authNombre = localStorage.getItem('blogs_flaites_nombre');
            this.authToken = localStorage.getItem('blogs_flaites_token');
        },
        cerrarSesion(){
            if(window.confirm("¿Realmente desea cerrar la sesión?")){
                localStorage.clear();
                window.location = "/login";
            }
        },
    }
});
