// Importaciones
import { readonly, ref } from "vue";
import { useRoute } from "vue-router";

export function blogsComposable(){

    // Variables
    let datos = ref([]);
    let categorias = ref([]);
    let error = ref(null);

    let getDatos = async() => {

        let route = useRoute();
        let url;

        if(route.query.categoria_id){
            url = `${import.meta.env.VITE_API_URL}blogs-buscador?categoria_id=${route.query.categoria_id}&search=${route.query.search}`;
        } else {
            url = `${import.meta.env.VITE_API_URL}blogs`;
        }

        try {
            // RUTA DEL BACKEND
            const res = await fetch(url, { headers: { 'content-type': 'application-json' }}); 
                datos.value = await res.json();

        } catch (err) {
            error.value = err;
        }

    };

    getDatos();
    /*
    let getDatos = async() => {

        try {
            // RUTA DEL BACKEND
            const res = await fetch(`${import.meta.env.VITE_API_URL}blogs`, 
                {headers: {'content-type': 'application-json'}})
                datos.value = await res.json();

        } catch (err) {
            error.value = err;
        }

    };

    getDatos();
     */

    let getCategorias = async() => {

        try {
            // RUTA DEL BACKEND
            const res = await fetch(`${import.meta.env.VITE_API_URL}categorias`, 
                {headers: {'content-type': 'application-json'}})
                categorias.value = await res.json();

        } catch (err) {
            error.value = err;
        }

    };

    getCategorias();

    return{

        datos:readonly(datos),
        error:readonly(error),
        categorias:readonly(categorias)

    }

}

