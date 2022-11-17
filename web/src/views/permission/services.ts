// 验证上传码

import { request } from '@/network/axios'
export async function validateUploadCode(code: string) {
  return request<{
    code: string
  }>('/checkSerial', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    data: JSON.stringify({
      serial: code,
    }),
    // headers
    //... 其他配置如请求头等
  })
}
