<template>
  <a-layout>
    <a-layout-sider class="layout-sider" collapsible v-model:collapsed="collapsed">
      <!-- <a-row type="flex" justify="center" align="top" style="padding-top: 8px">
        <a-col>
          <a-input-search placeholder="input search text" style="width: 150px" />
        </a-col>
      </a-row> -->
      <div style="height: 8px"></div>
      <a-menu mode="inline" class="layout-menu">
        <a-menu-item key="1">
          <home-outlined />
          <span>首页</span>
        </a-menu-item>
        <a-menu-item key="2">
          <cloud-upload-outlined />
          <span>上传</span>
        </a-menu-item>

        <a-menu-item key="9">
          <appstore-outlined />
          <span>资源库</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout style="padding: 12px; background-color: rgb(26, 26, 26)">
      <a-layout-content class="layout-content" :style="{ height: `${layoutContentHeight}px` }">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </a-layout-content>
      <!-- <a-layout-footer style="background-color: rgb(26, 26, 26)" /> -->
    </a-layout>
  </a-layout>
</template>

<script lang="ts" setup>
  import { AppstoreOutlined, HomeOutlined, CloudUploadOutlined } from '@ant-design/icons-vue'

  const layoutContentHeight = ref(0)
  onMounted(() => {
    const height = window.outerHeight - 135
    layoutContentHeight.value = height
  })

  const collapsed = ref(true)
</script>
<style>
  body {
    background-color: rgba(26, 26, 26);
  }
  .layout-content {
    background: #fff;
    padding: 12px;
    margin: 0;
    overflow: scroll;
    min-height: 280px;
    border-radius: 0.35rem;
  }

  .layout-sider {
    background-color: rgb(26, 26, 26);
    color: #fff;
  }

  .layout-menu {
    background-color: rgb(26, 26, 26);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border: 0;
    color: #fff;
  }

  .ant-menu-item {
    background-color: rgb(26, 26, 26);
    color: #fff;
    border-radius: 1rem 0 0 1rem !important;
  }

  .ant-menu {
    background-color: rgb(26, 26, 26);
    color: #fff;
  }

  .ant-menu-submenu {
    background-color: rgb(26, 26, 26);
    color: #fff;
    border-radius: 1rem 0 0 1rem !important;
  }

  .ant-menu-inline {
    background-color: rgb(26, 26, 26) !important;
    color: #fff;
    border-radius: 1rem 0 0 1rem !important;
  }

  .ant-menu-item-selected {
    background-color: rgba(255, 255, 255, 0.15) !important;
    border-radius: 1。5rem 0 0 1.5rem !important;
  }

  .ant-menu-title-content {
    display: flex;
    align-items: center;
  }

  .ant-layout-sider-trigger {
    background-color: rgb(26, 26, 26) !important;
  }
</style>
