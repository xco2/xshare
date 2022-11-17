import { request } from '@/network/axios'
export async function getFiles() {
  return request<string>('/files', {
    method: 'POST',
    headers: {
      Accept: 'text/html',
      'Content-Type': 'text/html; charset=utf-8',
    },
  })
}
