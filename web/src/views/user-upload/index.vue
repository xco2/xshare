<template>
  <Loading>
    <Permission>
      <a-row style="margin-top: 80px" justify="center">
        <a-col class="upload"> <Upload /> </a-col>
      </a-row>
    </Permission>
  </Loading>
</template>

<script lang="ts" setup>
  import Permission from '@/views/permission/index.vue'
  import { defineAsyncComponent } from 'vue'
  const Upload = defineAsyncComponent(() => import('@/views/user-upload/Upload.vue'))
</script>

<style scoped lang="less">
  .upload {
    background-color: #c0c0c0;
    padding: 24px;
    border-radius: 1rem;
    width: 20vw;
  }
</style>
