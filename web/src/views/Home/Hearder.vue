<template>
  <img
    @click="handleClick"
    src="https://vuejs.org/images/logo.png"
    alt="vue logo"
    style="cursor: pointer"
  />
  <div class="header">{{ title ?? '-' }}</div>
  <div>点击图标切换主题色</div>
  <!-- <div class="header" v-boolean="boolean">test</div> -->
</template>

<script lang="ts" setup>
  import { useToggle } from 'vue-hooks-plus'

  defineProps<{
    title?: string
  }>()

  // @ts-ignore
  const [darkMode, setDarkMode] = inject<any>('darkMode')

  const [value, { toggle, set }] = useToggle()

  onMounted(() => {
    // @ts-ignore
    set(darkMode.value)
  })
  watchEffect(() => {
    // @ts-ignore
    setDarkMode(value.value)
  })

  const handleClick = () => {
    toggle()
  }
</script>

<style scoped lang="less">
  img {
    width: 300px;
    height: 300px;
  }

  .header {
    font-size: 64px;
    font-weight: 600;
    text-align: center;
  }
</style>
