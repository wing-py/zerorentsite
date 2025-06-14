<template>
  <div class="list-worker-container">
    <n-card class="main-content">
      <div class="card-text-content text-center text-h6">
        <p class="coming-soon translatable">全世界的程序员，联合起来！！！</p>
      </div>
    </n-card>
    <n-divider />
    <div class="list-order-container">
      <n-space vertical :size="12">
        <n-data-table
          :bordered="false"
          :single-line="false"
          :columns="columns"
          :data="data"
          :pagination="pagination"
        />
      </n-space>
    </div>
  </div>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue'
import { NCard } from 'naive-ui'
import axios from 'axios'

type developerType = {
  id: string
  name: string
}
const columns: any = [
  { title: '账户', key: 'id' },
  { title: '用户名', key: 'name' },
]

const pagination = { pageSize: 10 }

const data = ref<developerType[]>([])

onMounted(async () => {
  try {
    const response = await axios.get('http://localhost:5000/apis/getDevelopers', {
      headers: { 'Content-Type': 'application/json' },
    })
    console.log(response.data.data[0].id)
    console.log(response.data.data[0].username)
    data.value = [
      ...data.value,
      {
        id: response.data.data[0].id,
        name: response.data.data[0].username,
      },
    ]
  } catch (error) {
    console.log('get error')
  }
})
</script>

<style scoped>
.list-worker-container {
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

.coming-soon {
  color: #4285f4;
}
</style>
