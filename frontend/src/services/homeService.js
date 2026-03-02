export async function getDatosHome() {
    let respuesta = await fetch(`${import.meta.env.VITE_API_URL}blogs-home`, 
        {headers: {'content-type': 'application/json'}});

    const resultado = await respuesta.json();
    return resultado;
}