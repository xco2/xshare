import { ProxyOptions } from 'vite'

export const proxy: Record<string, Record<string, ProxyOptions>> = {
  development: {},
  production: {
    '/': {
      // target:"http://",
      changeOrigin: true,
    },
  },
}
