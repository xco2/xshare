<template>
  <div>
    <div ref="container"></div>
  </div>
</template>

<script lang="ts" setup>
  import { usePreview } from 'vue-hooks-plus'

  const props = defineProps<{
    text: any
  }>()

  const { container } = usePreview(props.text)
</script>

<style scoped lang="less"></style>
