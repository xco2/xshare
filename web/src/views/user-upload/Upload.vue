<template>
  <a-upload
    :file-list="fileList"
    :before-upload="beforeUpload"
    @remove="handleRemove"
    :max-count="1"
  >
    <a-button size="large" style="display: flex; align-items: center">
      <template #icon>
        <UploadOutlined />
      </template>
      选择文件
    </a-button>
  </a-upload>

  <a-progress
    v-show="progressvisiablily"
    :stroke-color="{
      from: '#108ee9',
      to: '#87d068',
    }"
    :percent="progress"
    status="active"
  />

  <a-divider />
  <div class="w-full flex justify-center">
    <a-button
      type="primary"
      shape="round"
      size="large"
      style="display: flex; align-items: center; width: 8rem; justify-content: center"
      @click="handleUpload"
    >
      上传
    </a-button>
  </div>
</template>
<script setup lang="ts">
  import { UploadOutlined } from '@ant-design/icons-vue'
  import { ref } from 'vue'
  import { message, UploadProps } from 'ant-design-vue'
  import 'ant-design-vue/es/message/style/index'
  import { useBoolean, useRequest } from 'vue-hooks-plus'
  import { upload } from './services'

  const fileList = ref<UploadProps['fileList']>([])
  const uploading = ref<boolean>(false)

  const progress = ref(0)
  const [progressvisiablily, { set: setProgressvisiablily }] = useBoolean(false)

  const { run } = useRequest(upload, {
    manual: true,
    onBefore: () => {
      setProgressvisiablily(true)
    },
    onSuccess: (data) => {
      if (data) {
        message.success('文件上传成功')
        fileList.value = []
      } else message.error('文件上传失败')
    },
    onError: () => {
      message.error('文件上传失败')
    },
    onFinally: () => {
      setProgressvisiablily(false)
      progress.value = 0
    },
  })

  const beforeUpload: UploadProps['beforeUpload'] = (file) => {
    if (fileList.value && fileList.value?.length < 1) {
      fileList.value = [...(fileList.value ?? []), file]
    } else {
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

  const onUploadProgress = (progressEvent: any) => {
    progress.value = ((progressEvent.loaded / progressEvent.total) * 100) | 0
  }

  const handleUpload = async () => {
    const formData = new FormData()
    // @ts-ignore
    fileList.value?.forEach((file: UploadProps['fileList'][number]) => {
      formData.append('upload_file', file as any)
    })
    uploading.value = true
    run(formData, onUploadProgress)
  }
</script>
