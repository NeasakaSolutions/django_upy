export async function getDatosDocentes() {
    let respuesta = await fetch(`${import.meta.env.VITE_API_URL}docentes`, 
        {headers: {'content-type': 'application/json'}});

    const resultado = await respuesta.json();
    return resultado;
}