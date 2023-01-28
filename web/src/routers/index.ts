import { createRouter, createWebHistory } from 'vue-router'

export const routerHistory = createWebHistory('/xshare/')

const routers = createRouter({
  history: routerHistory,
  routes: [
    {
      path: '/',
      redirect: '/home',
    },
    {
      name: 'home',
      path: '/home',
      component: () => import('@/views/Home/index.vue'),
    },
    {
      name: 'upload',
      path: '/upload',
      component: () => import('@/views/user-upload/index.vue'),
    },
    {
      name: 'app-warehouse',
      path: '/app-warehouse',
      component: () => import('@/views/app-warehouse/index.vue'),
    },
    {
      name: 'code-area',
      path: '/code-area',
      component: () => import('@/views/code-area/index.vue'),
    },
    {
      name: 'desktop',
      path: '/desktop',
      component: () => import('@/views/desktop/index.vue'),
    },
  ],
})

export { routers }
