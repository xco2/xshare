// 验证上传码

import { request } from '@/network/axios'
export async function validateUploadCode(code: string) {
  const data = new FormData()
  data.append('serial', code)
  return request<{
    code: string
  }>('http://43.138.187.142:13000/checkSerial', {
    method: 'POST',
    data,
    // headers
    //... 其他配置如请求头等
  })
}
