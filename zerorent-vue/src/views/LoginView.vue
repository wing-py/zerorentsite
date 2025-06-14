<template>
  <div class="login-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">用户登录</h2>
      </template>

      <div class="card-text-content">
        <!-- 账号密码登录 -->
        <n-form @submit.prevent="login">
          <n-form-item label="用户名">
            <n-input v-model:value="username" placeholder="请输入用户名" required />
          </n-form-item>

          <n-form-item label="密码">
            <n-input v-model:value="password" type="password" placeholder="请输入密码" required />
          </n-form-item>

          <div class="form-actions mt-4">
            <n-button type="primary" @click="login">登录</n-button>
            <n-button @click="goToRegister" class="ml-2">还没有账号？去注册</n-button>
          </div>
        </n-form>

        <!-- 第三方登录按钮 -->
        <div class="social-login mt-4 text-center text-caption grey-text">
          <p class="translatable">微信登录、QQ登录、手机验证码登录、邮箱绑定待开发</p>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts">
export const currentUserName = ref<string>('')
export const currentUserId = ref<string>('')
</script>
<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NButton, useNotification } from 'naive-ui'
import { isLogined } from '../App.vue'
import axios from 'axios'

const username = ref<string>('')
const password = ref<string>('')
const notification = useNotification()

const login = async () => {
  if (username.value == '' || password.value == '') {
    alert('请填写必须字段（带*字段）')
    return
  }

  const data: any = {
    username: username.value,
    password: password.value,
  }

  try {
    const response = await axios.post('http://localhost:5000/apis/login', data, {
      headers: { 'Content-Type': 'application/json' },
    })

    console.log('response:', response)

    currentUserName.value = username.value
    currentUserId.value = response.data.data.id

    console.log('currentUserId:', currentUserId.value)
    console.log('currentUserName:', currentUserName.value)

    notification['info']({
      content: '登陆成功',
      meta: '跳转到主页面...',
      duration: 2500,
      keepAliveOnHover: true,
    })

    setTimeout(() => {
      router.push('/')
    }, 300)
    isLogined.value = true
  } catch (error: any) {
    if (error.response) {
      console.error('err response:', error.response.data)
      if (error.response.data.error == '用户不存在') {
        // alert('用户不存在')
        notification['error']({
          content: '登陆失败',
          meta: '用户不存在',
          duration: 2500,
          keepAliveOnHover: true,
        })
      } else if (error.response.data.error == '密码错误') {
        // alert('用户不存在')
        notification['error']({
          content: '登陆失败',
          meta: '密码错误',
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
const router = useRouter()
const goToRegister = () => {
  router.push('/register')
}
// export default {
//   name: 'LoginView',
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
//       password: ''
//     };
//   },
//   methods: {
//     login() {
//       console.log('Logging in with:', this.username, this.password);
//       // Implement login logic here
//     },
//     goToRegister() {
//       this.$router.push('/register');
//     }
//   }
// }
</script>

<style scoped>
.login-container {
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
