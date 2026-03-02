// Importaciones
import { useAuthStore } from '@/stores/authStore';
import axios from 'axios';

export function registroComposable(body){
    let sendData = async(body) =>
    {
        axios.post(`${import.meta.env.VITE_API_URL}seguridad/registro`, body, 
                {headers: {'content-type': 'application/json'}})
                .then((response) => {
                    alert("Te has registrado exitosamente. \nRevisa tu correo para activar tu cuenta.")
                    window.location = location.href;
                })
                .catch(() => {
                    alert("Ocurrió un error inesperado.")
                    window.location = location.href;
                });
    };

    return {
        sendData,
    };
}

export function loginComposable(body) {

    let sendData = async (body) => {
        try {
            axios.post(`${import.meta.env.VITE_API_URL}seguridad/login`, body, 
                { headers: { 'content-type': "application/json" } })
                .then((response) => {
                    let store = useAuthStore();
                    store.iniciarSesion(response.data);
                    window.location = "/panel";
            })
            .catch((err) => {
                alert("Ocurrió un error inesperado "+err);
                window.location = location.href;
            });
        } catch (error) {
            alert("Ocurrió un error inesperado");
            window.location=location.href;
        }
        
    };
    return {
        sendData,
    };

}

