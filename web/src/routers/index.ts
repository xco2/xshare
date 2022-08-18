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
      name: 'demo',
      path: '/demo',
      component: () => import('@/views/demo/demo.vue'),
    },
    {
      name: 'verification',
      path: '/permission/verification',
      component: () => import('@/views/permission/Verification.vue'),
    },
  ],
})

export { routers }
