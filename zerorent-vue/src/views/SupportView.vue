<template>
  <div class="support-container-wrapper">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">支持我们</h2>
      </template>

      <div class="card-text-content">
        <p class="translatable text-body-1 mb-4">欢迎加入我们的社区，共同支持和推动劳动者合作平台的发展。以下是您可以支持我们的方式：</p>

        <n-grid x-gap="20" y-gap="20" :cols="4" class="support-grid">
          <n-grid-item v-for="(option, index) in supportOptions" :key="index">
            <n-card class="support-card">
              <template #header>
                <h3 class="text-h6">{{ option.title }}</h3>
              </template>
              <p class="text-body-2">{{ option.description }}</p>
              <template #footer>
                <n-button :tag="option.link ? 'a' : 'button'" :href="option.link" :target="option.link ? '_blank' : '_self'" type="primary">{{ option.buttonText }}</n-button>
              </template>
            </n-card>
          </n-grid-item>
        </n-grid>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import { NCard, NGrid, NGridItem, NButton } from 'naive-ui';
const supportOptions=ref<{title:string,description:string,buttonText:string,link:string}[]> ([
        { title: '成为组织成员', description: '加入我们的团队，参与农业生产劳动实践，同时获得公平的报酬和保障。', buttonText: '申请成为成员', link: '/register-rider' },
        { title: '开发软件设施', description: '如果您对编程感兴趣，欢迎参与我们的平台开发，帮助我们改进和优化软件设施，提升用户体验。', buttonText: '参与开发', link: '/dev-contribution' },
        { title: '编写相关文档', description: '帮助我们编写用户指南、技术文档或宣传资料，让更多人了解和使用我们的平台。', buttonText: '参与文档编写', link: '/doc-contribution' },
        { title: '审查组织经济', description: '无论您是否有财务或审计背景，欢迎对我们组织具体的经济运作进行审查，确保组织财务的透明和公正。', buttonText: '开始审查', link: '/financial-review' },
        { title: '提供重要信息', description: '如果您有关于农业运营、劳动者权益或其他重要信息，欢迎与我们分享，帮助平台更好地发展。', buttonText: '提交信息', link: '/submit-info' }
      ]);
// export default {
//   name: 'SupportView',
//   components: {
//     NCard,
//     NGrid,
//     NGridItem,
//     NButton
//   },
//   data() {
//     return {
//       supportOptions: [
//         { title: '成为组织成员', description: '加入我们的团队，参与农业生产劳动实践，同时获得公平的报酬和保障。', buttonText: '申请成为成员', link: '/register-rider' },
//         { title: '开发软件设施', description: '如果您对编程感兴趣，欢迎参与我们的平台开发，帮助我们改进和优化软件设施，提升用户体验。', buttonText: '参与开发', link: '/dev-contribution' },
//         { title: '编写相关文档', description: '帮助我们编写用户指南、技术文档或宣传资料，让更多人了解和使用我们的平台。', buttonText: '参与文档编写', link: '/doc-contribution' },
//         { title: '审查组织经济', description: '无论您是否有财务或审计背景，欢迎对我们组织具体的经济运作进行审查，确保组织财务的透明和公正。', buttonText: '开始审查', link: '/financial-review' },
//         { title: '提供重要信息', description: '如果您有关于农业运营、劳动者权益或其他重要信息，欢迎与我们分享，帮助平台更好地发展。', buttonText: '提交信息', link: '/submit-info' }
//       ]
//     };
//   }
// }
</script>

<style scoped>
.support-container-wrapper {
  padding: 20px;
}

.main-content {
  max-width: 1200px;
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

.mb-4 {
  margin-bottom: 16px;
}

.support-grid {
  margin-top: 20px;
}

.support-card {
  text-align: center;
  transition: all 0.3s ease;
  height: 100%; /* Ensure cards in a grid have equal height */
}

.support-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}

.text-h6 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 10px;
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