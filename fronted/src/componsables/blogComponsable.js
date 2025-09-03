// Importaciones
import { readonly, ref } from "vue";

export function blogComposable(slug){

    // Variables
    let dato = ref({});
    let error = ref(null);

    let getDatos = async(slug) => {

        try {
            // RUTA DEL BACKEND
            const res = await fetch(`${import.meta.env.VITE_API_URL}blogs/slug/${slug}`, 
                {headers: {'content-type': 'application-json'}})
                dato.value = await res.json();

                if(res.status == 404){
                    window.location = "/error"
                }

        } catch (err) {
            error.value = err;
        }

    };

    getDatos(slug);

    return{

        dato:readonly(dato),
        error:readonly(error)

    }

}

