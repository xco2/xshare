<template>
  <p>readyState:{{ readyState }}</p>
  <div>{{ JSON.stringify(messageHistory) }}</div>
</template>

<script lang="ts" setup>
  // demo

  import useWebSocket from '@/hooks/useWebSocket'
  const messageHistory = ref<any[]>([])
  // 连接websocket
  const { readyState, sendMessage, latestMessage, disconnect, connect } = useWebSocket(
    'wss://demo.piesocket.com/v3/channel_1?api_key=VCXCEuvhGcBDP7XhiJJUDvR1e1D3eiVjgZ9VRiaV&notify_self',
    {
      onOpen: (e: any) => {
        console.log(e)
      },
      onClose: (e) => {
        console.log(e)
      },
      onMessage: (msg) => {
        console.log(msg)
      },
      // reconnectInterval 重试时间间隔
      // reconnectLimit 重试次数
      // protocols 额外的协议头
    },
  )

  watchEffect(() => {
    console.log(latestMessage?.value)
    // if (latestMessage?.value) {
    //   messageHistory.value.push(latestMessage?.value)
    //   disconnect?.()
    // }
  })
  // const messageHistoryCompute = computed(() => messageHistory.value.concat(latestMessage?.value))
</script>

<style scoped lang="less"></style>
