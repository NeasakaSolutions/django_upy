// Importaciones
import * as yup from 'yup';


export const contactoSchema = yup.object({

    nombre: yup.string().required("Este campo es obligatorio."),
    correo: yup.string().required("Este campo es obligatorio.").email("El correo ingresado no es válido."),
    telefono: yup.string().required("Este campo es obligatorio."),
    mensaje: yup.string().required("Este campo es obligatorio."),

});

export const registroSchema = yup.object({

    nombre: yup.string().required("Este campo es obligatorio."),
    correo: yup.string().required("Este campo es obligatorio.").email("El correo ingresado no es válido."),
    password: yup.string().required("Este campo es obligatorio."),

});


export const loginSchema = yup.object({

    correo: yup.string().required("Este campo es obligatorio.").email("El correo ingresado no es válido."),
    password: yup.string().required("Este campo es obligatorio."),

});


export const blogsSchema = yup.object({

    categoria_id: yup.string().test({
        name: 'categoria_id',
        skipAbsent: true,
        test(value, ctx){
            if(value == "0"){
                return ctx.createError({message: "Debe seleccionar una categoria."})
            }
            return true;
        }
    }),
    nombre: yup.string().required("Este campo es obligatorio."),
    descripcion: yup.string().required("Este campo es obligatorio."),

});

