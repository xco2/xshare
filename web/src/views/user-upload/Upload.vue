<template>
  <a-upload
    v-model:file-list="fileList"
    action="https://www.mocky.io/v2/5cc8019d300000980a055e76"
    @change="handleChange"
  >
    <a-button type="primary" shape="round" size="large" style="display: flex; align-items: center">
      <template #icon>
        <UploadOutlined />
      </template>
      上传
    </a-button>
  </a-upload>
</template>
<script setup lang="ts">
  import { UploadOutlined } from '@ant-design/icons-vue'
  import { ref } from 'vue'
  import type { UploadChangeParam, UploadProps } from 'ant-design-vue'

  const fileList = ref<UploadProps['fileList']>([
    // {
    //   uid: '1',
    //   name: 'xxx.png',
    //   status: 'done',
    //   response: 'Server Error 500', // custom error message to show
    //   url: 'http://www.baidu.com/xxx.png',
    // },
    // {
    //   uid: '2',
    //   name: 'yyy.png',
    //   status: 'done',
    //   url: 'http://www.baidu.com/yyy.png',
    // },
    // {
    //   uid: '3',
    //   name: 'zzz.png',
    //   status: 'error',
    //   response: 'Server Error 500', // custom error message to show
    //   url: 'http://www.baidu.com/zzz.png',
    // },
  ])

  const handleChange = ({ file, fileList }: UploadChangeParam) => {
    if (file.status !== 'uploading') {
      console.log(file, fileList)
    }
  }
</script>
