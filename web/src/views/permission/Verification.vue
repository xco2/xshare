<template>
  <PageContainer>
    <Card title="请输入验证码" class="container">
      <a-input-password default-value="" v-model="password" placeholder="请输入验证码" />
      <div class="submit">
        <a-button type="primary">验证</a-button>
      </div>
    </Card>
  </PageContainer>
</template>

<script lang="ts" setup>
  import PageContainer from '@/components/common/PageContainer'
  import Card from '@/components/common/Card'
  const password = ref('')
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
