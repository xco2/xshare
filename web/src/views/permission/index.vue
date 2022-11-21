<template>
  <PageContainer>
    <a-row style="position: relative">
      <a-col
        class="check"
        @click="checkClick"
        :style="{
          transform: `translate(${check ? translateX : 0}px)`,
          cursor: dotStatus === 2 ? 'null' : 'pointer',
        }"
      >
        {{ checkTitle }}
        <span
          class="dot"
          :style="{ backgroundColor: colorStatus[dotStatus as keyof typeof colorStatus] }"
        >
          <span
            class="dot-inner"
            :style="{ backgroundColor: colorStatus[dotStatus as keyof typeof colorStatus] }"
          ></span>
        </span>
      </a-col>
    </a-row>
    <a-row justify="center" style="margin-top: 80px" v-if="verificationVisiable && dotStatus !== 2">
      <a-col>
        <Verification @setVerification="setVerification" />
      </a-col>
    </a-row>
    <div v-if="dotStatus === 2">
      <slot></slot>
    </div>
  </PageContainer>
</template>

<script lang="ts" setup>
  import PageContainer from '@/components/common/PageContainer'
  import Verification from './Verification.vue'
  import {
    useBoolean,
    useRequest,
    useSessionStorageState,
    useTimeout,
    useWinResize,
  } from 'vue-hooks-plus'
  import { validateUploadCode } from './services'
  import { useHomeStore } from '@/store/modules/home'

  const status = {
    0: '未授权，需验证',
    1: '输入验证码',
    2: '在线',
  }

  const colorStatus = {
    0: '#DC3023',
    1: '#FFA400',
    2: '#32CD32',
  }

  const homeStore = useHomeStore()

  const [check, { set: setCheck }] = useBoolean(false)
  const [verificationVisiable, { set: setVerificationVisiable }] = useBoolean(false)
  const [verification, { set: setVerification }] = useBoolean(false)

  const [sessionKey, _] = useSessionStorageState('use-check-key', { defaultValue: '' })

  const translateX = ref(0)

  const dotStatus = ref<number>(0)

  const { run } = useRequest(validateUploadCode, {
    manual: true,
    onSuccess: (data) => {
      if (data) {
        dotStatus.value = 2
        homeStore.setPermissionAccess(true)
      } else dotStatus.value = 0
    },
    onFinally: () => {
      homeStore.setPermissionLoading(false)
    },
  })

  watchEffect(() => {
    if (check.value === false) dotStatus.value = 0
    else dotStatus.value = 1
  })

  const isAccess = computed(() => homeStore.getPermissionAccess)

  watchEffect(() => {
    console.log(isAccess.value)

    if (sessionKey.value && !isAccess.value) {
      homeStore.setPermissionLoading(true)
      run(sessionKey.value)
    }

    if (isAccess.value) {
      dotStatus.value = 2
      homeStore.setPermissionLoading(false)
    }
  })

  watchEffect(() => {
    if (verification.value) {
      translateX.value = 0
      dotStatus.value = 2
    }
  })

  const checkTitle = computed(() => status[dotStatus.value as keyof typeof status])

  onMounted(() => {
    translateX.value = !check.value
      ? document.getElementsByClassName('layout-content')[0].clientWidth / 2 - 164 / 2
      : 0
  })

  useWinResize(() => {
    translateX.value =
      dotStatus.value === 1
        ? document.getElementsByClassName('layout-content')[0].clientWidth / 2 - 164 / 2
        : 0
  })

  const checkClick = () => {
    if (dotStatus.value === 0) {
      setCheck(true)
      useTimeout(() => {
        setVerificationVisiable(true)
      }, 1500)
    }
  }
</script>

<style scoped lang="less">
  .check {
    background-color: rgba(82, 129, 255, 0.15);
    width: auto;
    line-height: 32px;
    font-size: 12px;
    padding: 12px;
    border-radius: 0.5rem;
    color: var(--xshare-font-color);
    transition: all 1s;
  }

  .dot {
    display: inline-block;
    position: relative;
    width: 12px;
    height: 12px;
    border-radius: 50%;
    top: 1.5px;
    margin-left: 5px;
  }

  .dot-inner {
    position: absolute;
    top: 0;
    left: 0;
    box-sizing: border-box;
    display: block;
    width: 100%;
    height: 100%;
    border-radius: 50%;
    -webkit-animation: vabDot 1.2s ease-in-out infinite;
    animation: vabDot 1.2s ease-in-out infinite;
  }

  @-webkit-keyframes vabDot {
    0% {
      opacity: 0.6;
      transform: scale(0.8);
    }

    to {
      opacity: 0;
      transform: scale(2.4);
    }
  }
</style>
