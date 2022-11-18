<template>
  <div>
    <div ref="container"></div>
  </div>
</template>

<script lang="ts" setup>
  import { usePreview } from 'vue-hooks-plus'

  const props = defineProps<{
    preview: any
  }>()
  const previewRef = computed(() => props.preview)

  const { container } = usePreview(previewRef)

  watchEffect(() => {
    console.log(props.preview)
  })
</script>

<style scoped lang="less"></style>
