export async function getDatosColaboradores() {
    let respuesta = await fetch(`${import.meta.env.VITE_API_URL}colaboradores`, 
        {headers: {'content-type': 'application/json'}});

    const resultado = await respuesta.json();
    return resultado;
}