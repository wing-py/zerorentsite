<template>
  <div class="home-container">
    <div class="text-center my-8">
      <h2 class="translatable text-h4">欢迎来到零抽成外包平台</h2>
      <p class="translatable text-subtitle-1">这里是零抽成开发外包平台的公开网站</p>
    </div>

    <n-grid x-gap="12" y-gap="12" :cols="4">
      <n-grid-item v-for="feature in features" :key="feature.name">
        <n-card :title="feature.name" @click="goToLink(feature.link)">
          <p>{{ feature.description }}</p>
        </n-card>
      </n-grid-item>
    </n-grid>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NGrid, NGridItem, NCard } from 'naive-ui';

type FeatureItem = {
  name: string
  description: string
  link: string
};

const features = ref<FeatureItem[]>([
        { name: '平台介绍', description: '介绍零抽成外包平台的目标、运行机制和运营战略', link: '/about' },
        { name: '意见论坛', description: '收集和公开讨论对平台的各种建议意见', link: '/forum' },
        { name: '发展规划', description: '目前关于组织以及相关程序设施建设的待办事项', link: '/development-plan' },
        { name: '提供支持', description: '您可以为组织以及其建设提供支持', link: '/support' },
        { name: '相关文档', description: '相关的文档资料', link: '/documentation' },
        { name: 'AI服务', description: '我们使用AI进行信息服务,并尝试使用AI管理组织!', link: '/ai-services' },
        { name: '账号管理', description: '填写账号个人信息，方便整理归档和进一步沟通', link: '/profile' },
        { name: '撰写信件', description: '收集人们的意见、看法和诉求', link: '/compose' },
        { name: '信件阅览', description: '浏览其他人的信件，了解大家的想法和建议', link: '/mailbox' },
        { name: '信息公示', description: '对资产、人员和组织制度的信息透明公示', link: '/disclosure' }
      ]);

const router = useRouter();
const goToLink = (link: string) => {
  router.push(link);
};

</script>

<style>
.home-container {
  padding: 20px;
}

.text-center {
  text-align: center;
}

.my-8 {
  margin-top: 32px;
  margin-bottom: 32px;
}

.text-h4 {
  font-size: 2rem;
  font-weight: bold;
}

.text-subtitle-1 {
  font-size: 1rem;
  color: #666;
}

.n-card {
  cursor: pointer;
  transition: all 0.3s ease;
}

.n-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}
</style>