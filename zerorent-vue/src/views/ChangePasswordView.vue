<template>
  <div class="change-password-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">更改密码</h2>
      </template>

      <n-form @submit.prevent="changePassword">
        <n-form-item label="旧密码">
          <n-input
            v-model:value="oldPassword"
            type="password"
            placeholder="请输入旧密码"
            required
          />
        </n-form-item>

        <n-form-item label="新密码">
          <n-input
            v-model:value="newPassword"
            type="password"
            placeholder="请输入新密码"
            required
          />
        </n-form-item>

        <n-form-item label="确认新密码">
          <n-input
            v-model:value="confirmPassword"
            type="password"
            placeholder="请确认新密码"
            required
          />
        </n-form-item>

        <div class="form-actions mt-4">
          <n-button type="primary" @click="changePassword">更改密码</n-button>
          <n-button @click="goToProfile" class="ml-2">返回个人信息</n-button>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton } from 'naive-ui';

const oldPassword=ref<string>('')
const newPassword=ref<string>('')
const confirmPassword=ref<string>('')

const changePassword = () => {
      console.log('Changing password...');
};

const router = useRouter();
const goToProfile = () =>{
      router.push('/profile');
    };

</script>

<style scoped>
.change-password-container {
  padding: 20px;
}

.main-content {
  max-width: 600px;
  margin: 0 auto;
}

.text-h5 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.ml-2 {
  margin-left: 8px;
}
</style>