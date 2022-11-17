<template>
  <Permission>
    <a-row style="margin-top: 80px" justify="center">
      <a-col>
        <Card class="upload"> <Upload /> </Card
      ></a-col>
    </a-row>
  </Permission>
</template>

<script lang="ts" setup>
  import Card from '@/components/common/Card'
  import Permission from '@/views/permission/index.vue'
  import { defineAsyncComponent } from 'vue'
  const Upload = defineAsyncComponent(() => import('@/views/user-upload/Upload.vue'))
</script>

<style scoped lang="less">
  .upload {
    padding: 24px;
    border-radius: 1rem;
    width: 40vw;
  }
</style>
