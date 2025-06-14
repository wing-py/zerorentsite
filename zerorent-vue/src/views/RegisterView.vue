<template>
  <div class="register-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">用户注册</h2>
      </template>

      <div class="card-text-content">
        <n-form @submit.prevent="register">
          <n-form-item label="用户名*">
            <n-input v-model:value="username" placeholder="请输入用户名" required />
          </n-form-item>

          <n-form-item label="密码*">
            <n-input v-model:value="password" type="password" placeholder="请输入密码" required />
          </n-form-item>

          <n-form-item label="确认密码*">
            <n-input
              v-model:value="confirmPassword"
              type="password"
              placeholder="请确认密码"
              required
            />
          </n-form-item>

          <n-form-item label="邮箱 (可选)">
            <n-input v-model:value="email" type="text" placeholder="请输入邮箱" />
          </n-form-item>

          <n-form-item label="手机号码 (可选)">
            <n-input v-model:value="phone" type="text" placeholder="请输入手机号码" />
          </n-form-item>

          <div class="form-actions mt-4">
            <n-button type="primary" @click="register">注册</n-button>
            <router-link to="/login" class="text-decoration-none">
              <n-button class="ml-2">已有账号？去登录</n-button>
            </router-link>
          </div>
        </n-form>

        <div class="social-login mt-4 text-center text-caption grey-text">
          <p class="translatable">微信登录、QQ登录、手机验证码登录、邮箱绑定待开发</p>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton, useNotification } from 'naive-ui'
import type { NotificationType } from 'naive-ui'
import axios from 'axios'

const username = ref<string>('')
const password = ref<string>('')
const confirmPassword = ref<string>('')
const email = ref<string>('')
const phone = ref<string>('')
const router = useRouter()
const notification = useNotification()

const register = async () => {
  if (username.value == '' || password.value == '' || confirmPassword.value == '') {
    alert('请填写必须字段（带*字段）')
    return
  }
  if (password.value != confirmPassword.value) {
    alert('请确保两次密码输入一致')
    return
  }

  const data: any = {
    name: username.value,
    password: password.value,
    email: email.value,
    phone: phone.value,
  }

  console.log('Registering user:', username.value, email.value, phone.value)
  try {
    const response = await axios.post('http://localhost:5000/apis/register', data, {
      headers: { 'Content-Type': 'application/json' },
    })

    console.log('response:', response)

    notification['info']({
      content: '注册成功',
      meta: '跳转到登陆页面...',
      duration: 2500,
      keepAliveOnHover: true,
    })
    setTimeout(() => {
      router.push('/login')
    }, 3000)
  } catch (error: any) {
    if (error.response) {
      console.error('err response:', error.response.data)
      if (error.response.data.erro == '用户名已存在') {
        notification['error']({
          content: '注册成功',
          meta: '跳转到登陆页面...',
          duration: 2500,
          keepAliveOnHover: true,
        })
      }
      console.error('err msg:', error.message)
    } else {
      console.error('err msg:', error.message)
    }
  }
}

// export default {
//   name: 'RegisterView',
//   components: {
//     NCard,
//     NForm,
//     NFormItem,
//     NInput,
//     NButton
//   },
//   data() {
//     return {
//       username: '',
//       password: '',
//       confirmPassword: '',
//       email: '',
//       phone: ''
//     };
//   },
//   methods: {
//     register() {
//       console.log('Registering user:', this.username, this.email, this.phone);
//       // Implement registration logic here
//     }
//   }
// }
</script>

<style scoped>
.register-container {
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

.social-login {
  margin-top: 16px;
  text-align: center;
  color: #666;
  font-size: 0.75rem; /* text-caption */
}

.grey-text {
  color: #9aa0a6;
}
</style>
