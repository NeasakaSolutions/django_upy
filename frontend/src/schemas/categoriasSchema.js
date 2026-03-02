import * as yup from 'yup';

export const categoriasSchema = yup.object({
  nombre: yup.string()
    .required('El nombre de la categoría es obligatorio.')
    .min(3, 'El nombre debe tener al menos 3 caracteres.')
    .max(50, 'El nombre no puede exceder los 50 caracteres.'),
});