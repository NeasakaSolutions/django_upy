/*
export async function getPortadas() {
    let respuesta = await fetch(`${import.meta.env.VITE_API_URL}portadas`, 
        {headers: {'content-type': 'application/json'}});

    const resultado = await respuesta.json();
    return resultado;
}
*/

export async function getPortadaById(id) {
  let respuesta = await fetch(`${import.meta.env.VITE_API_URL}portadas/${id}`, 
      {headers: {'content-type': 'application/json'}});
  const resultado = await respuesta.json();
  return resultado.data;
}