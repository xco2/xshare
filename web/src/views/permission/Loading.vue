<template>
  <a-spin :spinning="loading">
    <slot></slot>
  </a-spin>
</template>

<script lang="ts" setup>
  import { useHomeStore } from '@/store/modules/home'

  const homeStore = useHomeStore()

  const loading = computed(() => homeStore.getPermissionLoading)
</script>

<style scoped lang="less"></style>
