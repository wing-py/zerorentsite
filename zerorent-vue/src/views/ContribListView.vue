<template>
  <div class="contrib-list-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">贡献榜</h2>
      </template>

      <div class="card-text-content">
        <n-data-table
          :columns="columns"
          :data="contribData"
          :bordered="false"
        />
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import {ref} from  'vue'
import { NCard, NDataTable } from 'naive-ui';


const columns =ref<{title:string,key:string}[]>([
        { title: '排名', key: 'rank' },
        { title: '客户名', key: 'customerName' },
        { title: '下单日期', key: 'orderDate' },
        { title: '贡献值', key: 'contribution' },
]
);

const contribData =ref<{rank:number,customerName:string,orderDate:string,contribution:number}[]>(
    [
        { rank: 1, customerName: '客户 A', orderDate: '2023-01-01', contribution: 1000 },
        { rank: 2, customerName: '客户 B', orderDate: '2023-01-15', contribution: 800 },
    ]
);

</script>

<style scoped>
.contrib-list-container {
  padding: 20px;
}

.main-content {
  max-width: 800px;
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
</style>