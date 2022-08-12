<template>
  <div id="app">
    <div style="overflow: scroll">
      <router-view v-slot="{ Component }">
        <keep-alive>
          <component :is="Component" />
        </keep-alive>
      </router-view>
    </div>
  </div>
</template>

<style>
  #app {
    width: 100%;
    height: 100%;
  }
</style>
