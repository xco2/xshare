import { watch, ref, Ref } from 'vue'

export enum ReadyState {
  Connecting = 0,
  Open = 1,
  Closing = 2,
  Closed = 3,
}

export interface Options {
  reconnectLimit?: number
  reconnectInterval?: number
  manual?: Ref<boolean> | boolean
  onOpen?: (event: WebSocketEventMap['open'], instance: WebSocket) => void
  onClose?: (event: WebSocketEventMap['close'], instance: WebSocket) => void
  onMessage?: (message: WebSocketEventMap['message'], instance: WebSocket) => void
  onError?: (event: WebSocketEventMap['error'], instance: WebSocket) => void

  protocols?: string | string[]
}

export interface Result {
  latestMessage?: Ref<WebSocketEventMap['message']>
  sendMessage?: WebSocket['send']
  disconnect?: () => void
  connect?: () => void
  readyState: Ref<ReadyState>
  webSocketIns?: WebSocket
}

// function isLatestMessage(target: unknown): target is Result['latestMessage'] {
//   if (target !== undefined) return true
//   return false
// }

/**
 * author：杨杰
 * @param socketUrl socketUrl地址
 * @param options 配置
 */
export default function useWebSocket(
  socketUrl: Ref<string> | string,
  options: Options = {},
): Result {
  const {
    reconnectLimit = 3,
    reconnectInterval = 3 * 1000,
    manual = ref(false),
    onOpen,
    onClose,
    onMessage,
    onError,
    protocols,
  } = options

  const onOpenRef = ref(onOpen)
  const onCloseRef = ref(onClose)
  const onMessageRef = ref(onMessage)
  const onErrorRef = ref(onError)

  const reconnectTimesRef = ref(0)
  const reconnectTimerRef = ref<ReturnType<typeof setTimeout>>()
  const websocketRef = ref<WebSocket>()

  const unmountedRef = ref(false)

  const latestMessage = ref<WebSocketEventMap['message']>()
  const readyState = ref<ReadyState>(ReadyState.Closed)

  const reconnect = () => {
    if (
      reconnectTimesRef.value < reconnectLimit &&
      websocketRef.value?.readyState !== ReadyState.Open
    ) {
      if (reconnectTimerRef.value) {
        clearTimeout(reconnectTimerRef.value)
      }

      reconnectTimerRef.value = setTimeout(() => {
        // eslint-disable-next-line @typescript-eslint/no-use-before-define
        connectWs()
        reconnectTimesRef.value++
      }, reconnectInterval)
    }
  }

  const connectWs = () => {
    if (reconnectTimerRef.value) {
      clearTimeout(reconnectTimerRef.value)
    }

    if (websocketRef.value) {
      websocketRef.value.close()
    }

    const ws = new WebSocket(isRef(socketUrl) ? socketUrl.value : socketUrl, protocols)
    readyState.value = ReadyState.Connecting

    ws.onerror = (event) => {
      if (unmountedRef.value) {
        return
      }
      reconnect()
      onErrorRef.value?.(event, ws)
      readyState.value = ws.readyState || ReadyState.Closed
    }
    ws.onopen = (event) => {
      if (unmountedRef.value) {
        return
      }
      onOpenRef.value?.(event, ws)
      reconnectTimesRef.value = 0
      readyState.value = ws.readyState || ReadyState.Open
    }
    ws.onmessage = (message: WebSocketEventMap['message']) => {
      if (unmountedRef.value) {
        return
      }
      onMessageRef.value?.(message, ws)
      latestMessage.value = message
    }
    ws.onclose = (event) => {
      if (unmountedRef.value) {
        return
      }
      reconnect()
      onCloseRef.value?.(event, ws)
      readyState.value = ws.readyState || ReadyState.Closed
    }

    websocketRef.value = ws
  }

  const sendMessage: WebSocket['send'] = (message) => {
    if (readyState.value === ReadyState.Open) {
      websocketRef.value?.send(message)
    } else {
      throw new Error('WebSocket disconnected')
    }
  }

  const connect = () => {
    reconnectTimesRef.value = 0
    connectWs()
  }

  const disconnect = () => {
    if (reconnectTimerRef.value) {
      clearTimeout(reconnectTimerRef.value)
    }

    reconnectTimesRef.value = reconnectLimit
    websocketRef.value?.close()
  }

  watch(
    [socketUrl, manual],
    (c) => {
      const [_, manualWatch] = c
      if (!manualWatch) {
        connect()
      }
    },
    {
      immediate: true,
    },
  )

  onUnmounted(() => {
    unmountedRef.value = true
    disconnect()
  })

  return {
    latestMessage: latestMessage as Result['latestMessage'],
    sendMessage,
    connect,
    disconnect,
    readyState,
    webSocketIns: websocketRef.value,
  }
}
