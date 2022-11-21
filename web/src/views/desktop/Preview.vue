<template>
  <div style="width: 100%">
    <div ref="container" style="width: 100%"></div>
  </div>
</template>

<script lang="ts" setup>
  import { usePreview } from 'vue-hooks-plus'

  const props = defineProps<{
    preview: any
  }>()
  const previewRef = computed(() => props.preview)

  const { container } = usePreview(previewRef)
</script>

<style scoped lang="less">
  iframe {
    width: 100%;
    height: 100%;
  }
</style>
