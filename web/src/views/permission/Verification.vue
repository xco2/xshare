<template>
  <PageContainer>
    <Card title="请输入验证码" class="container">
      <a-input-password default-value="" v-model="password" placeholder="请输入验证码" />
      <div class="submit" @click="onSubmit">
        <a-button type="primary">验证</a-button>
      </div>
    </Card>
  </PageContainer>
</template>

<script lang="ts" setup>
  import PageContainer from '@/components/common/PageContainer'
  import Card from '@/components/common/Card'
  import { useRequest } from 'vue-hooks-plus'
  import { validateUploadCode } from './services'
  const password = ref('')

  const router = useRouter()

  const { run } = useRequest(validateUploadCode, {
    manual: true,
    onSuccess: (data) => {
      if (data.code === '0') {
        router.addRoute({
          path: `/${data.path}`,
          name: '上传页',
          component: () => import('@/views/user-upload/Upload.vue'),
        })
      }
    },
  })
  const onSubmit = () => {
    run(password.value)
  }

  // 验证成功动态注册路由
</script>

<style scoped lang="less">
  .container {
    width: 300px;
    position: absolute;
    left: 50%;
    top: 40%;
    transform: translate(-50%, -50%);
    padding: 12px;

    .submit {
      width: 100%;
      display: flex;
      justify-content: center;
      margin-top: 16px;
    }
  }
</style>
