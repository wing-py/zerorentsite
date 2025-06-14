<template>
  <div class="disclosure-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">信息公示</h2>
      </template>

      <div class="card-text-content">
        <n-collapse>
          <!-- 资产信息 -->
          <n-collapse-item title="资产" name="assets">
            <div class="assets">
              <n-grid x-gap="12" :cols="2">
                <n-grid-item>
                  <h4 class="translatable text-subtitle-1">收入</h4>
                  <ul>
                    <li class="translatable text-body-2">...</li>
                  </ul>
                </n-grid-item>

                <n-grid-item>
                  <h4 class="translatable text-subtitle-1">支出</h4>
                  <ul>
                    <li class="translatable text-body-2">劳动报酬</li>
                    <li class="translatable text-body-2">公共资产积累再生产</li>
                  </ul>
                </n-grid-item>
              </n-grid>
            </div>
          </n-collapse-item>

          <!-- 人员组织结构 -->
          <n-collapse-item title="人员组织结构" name="organization">
            <div class="org-level">
              <n-tag class="ma-1">种植组</n-tag>
              <n-tag class="ma-1">养殖组</n-tag>
              <n-tag class="ma-1">媒体组</n-tag>
            </div>

            <div class="organization-chart mt-4">
              <div class="org-level">
                <n-tag class="ma-1">股东</n-tag>
                <n-tag class="ma-1">劳动者</n-tag>
              </div>
            </div>
          </n-collapse-item>

          <!-- 宪章 -->
          <n-collapse-item title="宪章" name="constitution">
            <div class="constitution">
              <p class="translatable text-body-1">本平台致力于构建一个公平、透明、高效的劳动者合作生态系统。所有参与者都将遵循以下原则：</p>
              <ul>
                <li class="translatable text-body-2">公开透明的收入分配机制</li>
                <li class="translatable text-body-2">民主决策的组织管理模式</li>
                <li class="translatable text-body-2">持续发展的公共资产积累</li>
                <li class="translatable text-body-2">劳动者权益优先保障</li>
                <li class="translatable text-body-2">技术驱动的服务优化</li>
              </ul>
            </div>
          </n-collapse-item>
        </n-collapse>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { NCard, NCollapse, NCollapseItem, NGrid, NGridItem, NTag } from 'naive-ui';

</script>

<style scoped>
.disclosure-container {
  padding: 20px;
}

.main-content {
  max-width: 1000px;
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

.section {
  margin-bottom: 20px;
}

h4 {
  margin-bottom: 10px;
  color: #333;
}

ul {
  list-style-type: disc;
  margin-left: 20px;
  margin-bottom: 10px;
}

li {
  margin-bottom: 5px;
}

.org-level {
  margin-bottom: 10px;
}

.ma-1 {
  margin: 4px;
}

.mt-4 {
  margin-top: 16px;
}

.text-subtitle-1 {
  font-size: 1rem;
  font-weight: bold;
}

.text-body-1 {
  font-size: 1rem;
  line-height: 1.6;
}

.text-body-2 {
  font-size: 0.875rem;
  line-height: 1.6;
}
</style>