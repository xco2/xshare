<template>
  <a-layout>
    <a-layout-sider class="layout-sider" collapsible v-model:collapsed="collapsed">
      <!-- <a-row type="flex" justify="center" align="top" style="padding-top: 8px">
        <a-col>
          <a-input-search placeholder="input search text" style="width: 150px" />
        </a-col>
      </a-row> -->
      <div style="height: 8px"></div>
      <a-menu
        mode="inline"
        class="layout-menu"
        @click="(menuClick as any)"
        v-model:selectedKeys="selectedKeys"
      >
        <a-menu-item key="/home">
          <home-outlined />
          <span>首页</span>
        </a-menu-item>
        <a-menu-item key="/desktop">
          <desktop-outlined />
          <span>调度</span>
        </a-menu-item>
        <a-menu-item key="/upload">
          <cloud-upload-outlined />
          <span>上传</span>
        </a-menu-item>

        <a-menu-item key="/app-warehouse">
          <appstore-outlined />
          <span>资源库</span>
        </a-menu-item>

        <a-menu-item key="/code-area">
          <bulb-outlined />
          <span>码场</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>

    <a-layout style="padding: 12px" class="layout">
      <Loading>
        <a-layout-content class="layout-content">
          <router-view v-slot="{ Component }">
            <keep-alive>
              <component :is="Component" />
            </keep-alive>
          </router-view>
        </a-layout-content>
      </Loading>
    </a-layout>
  </a-layout>
</template>

<script lang="ts" setup>
  import {
    AppstoreOutlined,
    HomeOutlined,
    CloudUploadOutlined,
    BulbOutlined,
    DesktopOutlined,
  } from '@ant-design/icons-vue'
  // import { MenuClickEventHandler } from 'ant-design-vue/es/menu/src/interface'
  import { useDarkMode, useWinResize } from 'vue-hooks-plus'

  const router = useRouter()
  const route = useRoute()
  const collapsed = ref(true)
  const layoutContentHeight = ref(0)
  const selectedKeys = ref(['/home'])

  const [darkMode, setDarkMode] = useDarkMode()

  watchEffect(() => {
    console.log(darkMode.value)
  })

  provide('darkMode', [darkMode, setDarkMode])

  watchEffect(() => {
    document
      .querySelector('html')
      ?.setAttribute('data-prefers-color-scheme', `${darkMode.value ? 'dark' : ''}`)
  })

  watchEffect(() => {
    selectedKeys.value = [route.path]
  })

  onMounted(() => {
    const height = window.outerHeight - 135
    layoutContentHeight.value = height
  })

  useWinResize(() => {
    const height = window.outerHeight - 135
    layoutContentHeight.value = height
  })

  const menuClick = ({ key }: { key: string }) => {
    router.push(key)
  }
</script>
<style>
  body {
    background-color: var(--xshare-layout-sider-color);
  }

  .layout {
    background-color: var(--xshare-layout-sider-color);
  }
  .layout-content {
    background-color: var(--xshare-page-background);
    padding: 12px;
    margin: 0;
    overflow: scroll;
    min-height: 280px;
    border-radius: 0.35rem;
    height: calc(100vh - 24px);
  }

  .layout-sider {
    background-color: var(--xshare-layout-sider-color);
    color: var(--xshare-layout-sider-font-color);
  }

  .layout-menu {
    background-color: var(--xshare-layout-sider-color);
    -webkit-backdrop-filter: blur(10px);
    backdrop-filter: blur(10px);
    border: 0;
    color: var(--xshare-layout-sider-font-color);
  }

  .ant-menu-item {
    background-color: var(--xshare-layout-sider-color);
    color: var(--xshare-layout-sider-font-color);
    border-radius: 1rem 0 0 1rem !important;
  }

  .ant-menu {
    background-color: var(--xshare-layout-sider-color);
    color: var(--xshare-layout-sider-font-color);
  }

  .ant-menu-submenu {
    background-color: var(--xshare-layout-sider-color);
    color: var(--xshare-layout-sider-font-color);
    border-radius: 1rem 0 0 1rem !important;
  }

  .ant-menu-inline {
    background-color: var(--xshare-layout-sider-color) !important;
    color: var(--xshare-layout-sider-font-color);
    border-radius: 1rem 0 0 1rem !important;
  }

  .ant-menu-item-selected {
    background-color: rgba(82, 129, 255, 0.15) !important;
    border-radius: 1。5rem 0 0 1.5rem !important;
  }

  .ant-menu-title-content {
    display: flex;
    align-items: center;
  }

  .ant-layout-sider-trigger {
    background-color: var(--xshare-layout-sider-color) !important;
  }

  .ant-layout-sider-trigger {
    color: var(--xshare-layout-sider-font-color);
  }
</style>
