<template>
  <div class="submit-order-container">
    <!-- <n-space vertical :size="12"> -->
    <!-- <n-data-table
        :bordered="false"
        :single-line="false"
        :columns="columns"
        :data="data"
        :pagination="pagination"
      /> -->
    <n-form ref="formRef" :model="model">
      <n-form-item path="name" label="名称*">
        <n-input v-model:value="model.name" @keydown.enter.prevent />
      </n-form-item>
      <n-form-item path="desription" label="详细描述*">
        <n-input v-model:value="model.description" @keydown.enter.prevent />
      </n-form-item>
      <n-form-item path="price" label="价格*">
        <n-input v-model:value="model.price" @keydown.enter.prevent />
      </n-form-item>
      <n-row :gutter="[0, 24]">
        <n-col :span="24">
          <div style="display: flex; justify-content: flex-end">
            <n-button
              :disabled="model.name === null"
              round
              type="primary"
              @click="handleValidateButtonClick"
            >
              提交
            </n-button>
          </div>
        </n-col>
      </n-row>
    </n-form>

    <!-- <pre>{{ JSON.stringify(model, null, 2) }} -->
    <!-- </pre> -->
    <!-- </n-space> -->
  </div>
</template>

<script lang="ts">
// 1. 定义用户对象类型
type User = {
  id: number
  name: string
}
type OrderStatus = 'undo' | 'doing' | 'done' | 'dealing?'

export type Order = {
  id: number
  name: string
  description: string
  price: number
  stat: OrderStatus // 使用预定义的状态类型
  date: string
  publisher: User // 复用用户类型
  worker: User | null // 复用用户类型
}

export type modelRef = {
  name: string | null
  description: string | null
  price: number | null
}

export const orders = ref<Order[]>([
  {
    id: 1,
    name: '订单1',
    description: '这是描述A',
    price: 100,
    stat: 'undo',
    date: '2023-01-01',
    publisher: { id: 1, name: 'a' },
    worker: null,
  },
  {
    id: 2,
    name: '订单2',
    description: '这是描述B',
    price: 200,
    stat: 'doing',
    date: '2023-01-01',
    publisher: { id: 2, name: 'b' },
    worker: { id: 2, name: 'B' },
  },
  {
    id: 3,
    name: '订单3',
    description: '这是描述C',
    price: 300,
    stat: 'done',
    date: '2023-01-01',
    publisher: { id: 3, name: 'c' },
    worker: { id: 3, name: 'C' },
  },
  {
    id: 4,
    name: '订单4',
    description: '这是描述D',
    price: 400,
    stat: 'dealing?',
    date: '2023-01-01',
    publisher: { id: 4, name: 'd' },
    worker: null,
  },
])

export function createColumns() {
  return [
    { title: 'ID', key: 'id' },
    { title: 'Name', key: 'name' },
    { title: 'Description', key: 'description' },
    { title: 'Price', key: 'price' },
    { title: 'Stat', key: 'stat' },
    { title: 'Publisher', key: 'publisher' },
    { title: 'Worker', key: 'worker' },
    { title: 'Date', key: 'date' },
  ]
}
</script>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
// import { DataTableColumns } from 'naive-ui';
import { defineComponent } from 'vue'
import { useNotification } from 'naive-ui'
// import { namespace } from 'naive-ui/es/_utils/cssr'
import type { FormInst, FormItemInst } from 'naive-ui'
import axios from 'axios'
import { isLogined } from '../App.vue'
import { currentUserId } from './LoginView.vue'

const columns = createColumns()
const data = orders
const pagination = { pageSize: 4 }

const formRef = ref<FormInst | null>(null)
const rPasswordFormItemRef = ref<FormItemInst | null>(null)

const router = useRouter()
const notification = useNotification()

const model = ref<modelRef>({ name: null, description: null, price: null })

const handleValidateButtonClick = async () => {
  if (!isLogined.value) {
    notification['warning']({
      content: '请先登陆',
      meta: '跳转到登陆...',
      duration: 500,
      keepAliveOnHover: true,
    })

    setTimeout(() => {
      router.push('/login')
    }, 300)
    return
  }
  if (model.value.name == null || model.value.description == null || model.value.price == null) {
    notification['info']({
      content: '请必须填写带*字段',
      meta: '跳转到登陆...',
      duration: 2000,
      keepAliveOnHover: true,
    })
    return
  }
  const data: any = {
    // id: 1,
    name: model.value.name,
    description: model.value.description,
    price: model.value.price,
    publisher_id: currentUserId.value,
  }

  try {
    const response = await axios.post('http://localhost:5000/apis/postOrder', data, {
      headers: { 'Content-Type': 'application/json' },
    })

    console.log('response:', response)

    notification['info']({
      content: '提交成功',
      meta: '跳转到主页面...',
      duration: 2500,
      keepAliveOnHover: true,
    })

    setTimeout(() => {
      router.push('/')
    }, 300)
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
</script>

<style scoped>
.submit-order-container {
  padding: 20px;
}

.main-content {
  max-width: 600px;
  margin: 0 auto;
}

.card-text-content {
  padding: 16px;
}

.text-center {
  text-align: center;
}

.text-h6 {
  font-size: 1.25rem;
  font-weight: bold;
}
</style>
descriptionsDark,
