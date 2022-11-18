<template>
  <div>
    <div ref="container"></div>
    <div style="font-size: 16px">6767</div>
  </div>
</template>

<script lang="ts" setup>
  import { usePreview } from 'vue-hooks-plus'

  const props = defineProps<{
    text: any
  }>()
  const textRef = computed(() => props.text)

  const { container } = usePreview(textRef)
</script>

<style scoped lang="less"></style>
