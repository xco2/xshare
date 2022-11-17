<template>
  <PageContainer>
    <Card title="请输入验证码">
      <a-textarea v-model:value="password" placeholder="请输入验证码" :rows="4" />
      <div class="submit" @click="onSubmit()">
        <a-button type="primary" size="large" style="width: 20vw">验证</a-button>
      </div>
    </Card>
  </PageContainer>
</template>

<script lang="ts" setup>
  import PageContainer from '@/components/common/PageContainer'
  import Card from '@/components/common/Card'
  import { useRequest, useSessionStorageState } from 'vue-hooks-plus'
  import { validateUploadCode } from './services'
  import { useHomeStore } from '@/store/modules/home'

  const homeStore = useHomeStore()

  const [_, setKey] = useSessionStorageState('use-check-key', { defaultValue: '' })

  const password = ref('')

  const emit = defineEmits(['setVerification'])

  const setVerification = (value: boolean) => {
    emit('setVerification', value)
  }

  defineExpose({
    setVerification,
  })

  const { run, loading } = useRequest(validateUploadCode, {
    manual: true,
    onSuccess: () => {
      setVerification(true)
      setKey(password.value)
    },
  })

  const onSubmit = () => {
    run(password.value)
  }

  watchEffect(() => {
    homeStore.setPermissionLoading(loading.value)
  })
</script>

<style scoped lang="less">
  .container {
    width: 40vw;
    padding: 12px;

    .submit {
      width: 100%;
      display: flex;
      justify-content: center;
      margin-top: 16px;
    }
  }
</style>
