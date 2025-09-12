// Importaciones
import Blogs from '@/views/Blogs.vue'
import Videos from '@/views/Videos.vue'
import Error404 from '@/views/Error404.vue'

import { createRouter, createWebHistory } from 'vue-router'
import BlogsDetalles from '@/views/blogsDetalles.vue'
import BlogsGeneral from '@/views/BlogsGeneral.vue'
import BlogsBuscador from '@/views/BlogsBuscador.vue';
import Contacto from '@/views/Contacto.vue'
import Registro from '@/views/Registro.vue'
import Login from '@/views/Login.vue'
import Panel from '@/views/Panel.vue'
import { useAuthStore } from '@/stores/authStore'
import PanelEditarFoto from '@/views/PanelEditarFoto.vue'
import PanelEditarDocumento from '@/views/PanelEditarDocumento.vue'
import PanelDocentes from '@/views/PanelDocentes.vue'
import PanelPortadas from '@/views/PanelPortadas.vue'
import PanelVideos from '@/views/PanelVideos.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path:'/',
      component: () => import('@/views/Home.vue'),
      name: 'home',
    },
    {
      path: '/Blogs',
      component: Blogs,
      name: 'blogs'
    },
    {
      path: '/Videos',
      component: Videos,
      name: 'videos'
    },
    {
      path: '/blogs/general',
      component: BlogsGeneral,
      name: 'BlogsGeneral'
    },
    {
      path: '/blogs/buscador',
      component: BlogsBuscador,
    },
    {
      path: '/contacto',
      component: Contacto,
      name: 'contacto'
    },
    {
      path: '/registro',
      component: Registro,
      name: 'registro'
    },
    {
      path: '/login',
      component: Login,
      name: 'login'
    },
    {
      path: '/panel',
      component: Panel,
      name: 'panel',
      meta: {
        secure: true
      }
    },
    {
      path: '/panel/editar/foto/:id',
      component: PanelEditarFoto,
      name: 'panel_editar_foto',
      meta: {
        secure: true
      }
    },
    {
      path: '/panel/editar/documento/:id',
      component: PanelEditarDocumento,
      name: 'panel_editar_documento',
      meta: {
        secure: true
      }
    },
    {
      path: '/docentes',
      component: PanelDocentes,
      name: 'panelDocentes',
      meta: {
        secure: true
      }
    },
    {
      path: '/portadas',
      component: PanelPortadas,
      name: 'panelPortadas',
      meta: {
        secure: true
      }
    },
    {
      path: '/videos',
      component: PanelVideos,
      name: 'panelVideos',
      meta: {
        secure: true
      }
    },
    {
      path: '/blogs/detalle/:slug',
      component: BlogsDetalles,
      name: 'blogsDetalle'
    },
    // Ultima ruta, para error 404
    {
      path:'/:pathMatch(.*)*',
      component: Error404,
      name: 'error404'
    },
  ],
})

// guards
router.beforeEach((to, from) => {

  let store = useAuthStore();

  if(to.meta.secure){
    
    store.estasLogueado();

  }

});

export default router
