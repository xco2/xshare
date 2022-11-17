<template>
  <a-upload
    :file-list="fileList"
    :before-upload="beforeUpload"
    @remove="handleRemove"
    :max-count="1"
  >
    <a-button type="primary" shape="round" size="large" style="display: flex; align-items: center">
      <template #icon>
        <UploadOutlined />
      </template>
      选择文件
    </a-button>
  </a-upload>
</template>
<script setup lang="ts">
  import { UploadOutlined } from '@ant-design/icons-vue'
  import { ref } from 'vue'
  import { message, UploadProps } from 'ant-design-vue'
  import 'ant-design-vue/es/message/style/index'

  const fileList = ref<UploadProps['fileList']>([])
  // const uploading = ref<boolean>(false)

  const beforeUpload: UploadProps['beforeUpload'] = (file) => {
    if (fileList.value && fileList.value?.length < 1) {
      fileList.value = [...(fileList.value ?? []), file]
    } else {
      console.log(777)

      message.error('只能上传一个文件')
    }

    return false
  }

  const handleRemove: UploadProps['onRemove'] = (file) => {
    const index = fileList.value?.indexOf(file)
    const newFileList = fileList.value?.slice()
    if (index !== undefined && newFileList !== undefined) {
      newFileList.splice(index, 1)
      fileList.value = newFileList
    }
  }

  // const handleUpload = () => {
  //   const formData = new FormData()
  //   // @ts-ignore
  //   fileList.value?.forEach((file: UploadProps['fileList'][number]) => {
  //     formData.append('upload_file', file as any)
  //   })
  //   uploading.value = true

  //   // You can use any AJAX library you like
  //   // request('https://www.mocky.io/v2/5cc8019d300000980a055e76', {
  //   //   method: 'post',
  //   //   data: formData,
  //   // })
  //   //   .then(() => {
  //   //     fileList.value = []
  //   //     uploading.value = false
  //   //     message.success('upload successfully.')
  //   //   })
  //   //   .catch(() => {
  //   //     uploading.value = false
  //   //     message.error('upload failed.')
  //   //   })
  // }
</script>
