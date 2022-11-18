<template>
  <div class="text-cyan-500 p-2"
    >我是demo-

    <slot></slot>
    <div>{{ text }}</div>
  </div>
</template>

<script lang="ts" setup>
  defineProps<{
    text: string
  }>()
</script>

<style scoped lang="less"></style>
