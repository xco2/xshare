import { request } from '@/network/axios'
export async function upload(data: FormData) {
  return request<{
    code: string
  }>('/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
    },
    data,
  })
}
