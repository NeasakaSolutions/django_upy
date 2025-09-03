export async function getDatosLaboratorios() {
    let respuesta = await fetch(`${import.meta.env.VITE_API_URL}laboratorios`, 
        {headers: {'content-type': 'application/json'}});

    const resultado = await respuesta.json();
    return resultado;
}