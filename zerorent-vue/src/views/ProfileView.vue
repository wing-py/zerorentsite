<template>
  <div class="profile-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">账号信息</h2>
      </template>

      <div class="card-text-content">
        <n-form @submit.prevent="saveProfile">
          <n-form-item label="账号名">
            <n-input
              v-model:value="user.username"
              placeholder="请输入账号名"
            />
          </n-form-item>

          <n-form-item label="姓名">
            <n-input
              v-model:value="user.real_name"
              placeholder="请输入姓名"
            />
          </n-form-item>

          <n-form-item label="身份证号">
            <n-input
              v-model:value="user.id_card"
              placeholder="请输入身份证号"
            />
          </n-form-item>

          <n-form-item label="手机号码">
            <n-input
              v-model:value="user.phone"
              type="text"
              placeholder="请输入手机号码"
            />
          </n-form-item>

          <n-form-item label="QQ">
            <n-input
              v-model:value="user.qq"
              placeholder="请输入QQ"
            />
          </n-form-item>

          <n-form-item label="微信">
            <n-input
              v-model:value="user.wechat"
              placeholder="请输入微信"
            />
          </n-form-item>

          <n-form-item label="邮箱">
            <n-input
              v-model:value="user.email"
              type="text"
              placeholder="请输入邮箱"
            />
          </n-form-item>

          <div class="form-actions mt-4">
            <n-button type="primary" @click="saveProfile">保存信息</n-button>
            <n-button @click="goToMailbox" class="ml-2">返回信箱</n-button>
            <n-button @click="goToChangePassword" class="ml-2">更改密码</n-button>
          </div>
        </n-form>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import {useRouter} from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton } from 'naive-ui';

type userType = {
        username: string,
        real_name: string,
        id_card: string,
        phone: string,
        qq: string,
        wechat: string,
        email: string,
};

const user = ref<userType> ({
        username: '示例用户',
        real_name: '示例姓名',
        id_card: '123456789012345678',
        phone: '13800000000',
        qq: '123456789',
        wechat: '示例微信',
        email: 'user@example.com'
});

const router = useRouter();

const saveProfile = () => {
      console.log('Saving profile:', user.value);
      // Implement save profile logic here
    };

const goToMailbox = () => {
      router.push('/mailbox');
    };

const goToChangePassword = () => {
      router.push('/change-password');
    };

// export default {
//   name: 'ProfileView',
//   components: {
//     NCard,
//     NForm,
//     NFormItem,
//     NInput,
//     NButton
//   },
//   data() {
//     return {
//       user: {
//         username: '示例用户',
//         real_name: '示例姓名',
//         id_card: '123456789012345678',
//         phone: '13800000000',
//         qq: '123456789',
//         wechat: '示例微信',
//         email: 'user@example.com'
//       }
//     };
//   },
//   methods: {
//     saveProfile() {
//       console.log('Saving profile:', this.user);
//       // Implement save profile logic here
//     },
//     goToMailbox() {
//       this.$router.push('/mailbox');
//     },
//     goToChangePassword() {
//       this.$router.push('/change-password');
//     }
//   }
// }
</script>

<style scoped>
.profile-container {
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

.card-text-content {
  padding: 16px;
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