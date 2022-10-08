import { createRouter, createWebHistory } from 'vue-router'

export const routerHistory = createWebHistory()

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
  ],
})

export { routers }
