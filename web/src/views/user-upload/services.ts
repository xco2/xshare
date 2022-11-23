import { request } from '@/network/axios'
export async function upload(data: FormData, onUploadProgress: (progressEvent: any) => void) {
  return request<{
    code: string
  }>('/upload', {
    method: 'POST',
    headers: {
      'Content-Type': 'multipart/form-data',
      XAuthorization: sessionStorage?.getItem('use-check-key')?.replace('"', '') ?? '',
    },
    data,
    onUploadProgress,
  })
}
