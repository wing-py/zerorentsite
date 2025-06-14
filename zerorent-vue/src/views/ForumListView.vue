<template>
  <n-layout has-sider style="height: calc(100vh - 60px);">
    <n-layout-sider
      bordered
      collapse-mode="width"
      :collapsed-width="64"
      :width="240"
      :native-scrollbar="false"
      :show-trigger="true"
      :collapsed="collapsed"
      @update:collapsed="handleCollapsed"
      class="forum-sider"
    >
      <n-menu
        :collapsed-width="64"
        :collapsed-icon-size="22"
        :options="siderMenuOptions"
        style="color:aqua;"
      />
    </n-layout-sider>
    <n-layout>
      <n-layout-header bordered style="padding: 10px 20px;">
        <n-input
          v-model:value="searchValue"
          placeholder="搜索论坛..."
          clearable
          size="large"
          style="max-width: 600px;"
        >
          <template #prefix>
            <n-icon :component="Search" />
          </template>
        </n-input>
      </n-layout-header>
      <n-layout-content content-style="padding: 24px;">
        <n-card>
          <template #header>
            <h2 class="text-h5">话题</h2>
          </template>
          <n-list bordered>
            <n-list-item v-for="topic in showTopics" :key="topic.id" @click="goToTopic(topic.id)">
              <n-thing :title="topic.title" :description="topic.author">
                <template #footer>
                  <n-space justify="space-between">
                    <n-tag type="info" size="small">{{ topic.category }}</n-tag>
                    <n-text depth="3">{{ topic.date }}</n-text>
                  </n-space>
                </template>
              </n-thing>
            </n-list-item>
          </n-list>
          <div v-if="!showTopics || showTopics.length === 0" class="translatable text-body-1">没有找到话题</div>
        </n-card>
      </n-layout-content>
    </n-layout>
  </n-layout>
</template>

<script lang="ts" setup>
import { ref, h } from 'vue';
import { RouterLink, useRouter } from 'vue-router';
import {
  NLayout,
  NLayoutSider,
  NLayoutHeader,
  NLayoutContent,
  NMenu,
  NInput,
  NIcon,
  NCard,
  NList,
  NListItem,
  NThing,
  NTag,
  NText,
  NSpace
} from 'naive-ui';
import { Search } from '@vicons/ionicons5'; // Corrected import path

const collapsed = ref<boolean>(false); // Initialize collapsed state to false (expanded)

const handleCollapsed = (value:boolean) => {
  collapsed.value = value;
};


// const menuNodeProps = ({ option:any }) => {
//   return {

//     onClick() {
//         console.log("options:" + option);
//         console.log("getShowTopics:");
//         getShowTopics();
//     //   if (option.key === 'all-topics' || option.children) {
//     //     // Do nothing for parent items or "All Topics"
//     //   } else {
//     //     // For actual link items, ensure text color is clear
//     //     // This is a workaround if default theme doesn't provide enough contrast
//     //     // You might want to adjust theme overrides in App.vue for a global solution
//     //   }
//     },
//     style: {
//       color: 'var(--n-text-color)' // Use a variable that should resolve to a clear color
//     }
//   }
// }

const router = useRouter();
const searchValue = ref<string>('');
const categories=ref<string>('');
const tag=ref<string>('');

const showTopics = ref<topicType[]>(topics.value);

function getShowTopics(){
    const searchParams = new URLSearchParams(window.location.search);
    console.log(searchParams.get('category')); // 输出参数值
    // showTopics = topics;


    if(searchParams.get('category'))
    {
        showTopics.value=topics.value.filter((t)=>t.category==searchParams.get('category'));
    }
    if(searchParams.get('tag'))
    {
        showTopics.value=topics.value.filter((t)=>t.tag==searchParams.get('tag'));
    }

    console.log(showTopics);
    console.log(topics);

}

const siderMenuOptions = [
  {
    label: () => h(RouterLink, { to: { name: 'forum' } }, { default: () => '所有话题' }),
    key: 'all-topics',
  },
  {
    label: '分类',
    key: 'categories',
    children: [
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { category: '新手指南' } } }, { default: () => '新手指南' }),
        key: 'newbie-guide',
      },
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { category: '项目合作' } } }, { default: () => '项目合作' }),
        key: 'project-collaboration',
      },
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { category: '常见问题' } } }, { default: () => '常见问题' }),
        key: 'faq',
      },
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { category: '经验分享' } } }, { default: () => '经验分享' }),
        key: 'experience-sharing',
      },
    ],
  },
  {
    label: '标签',
    key: 'tags',
    children: [
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { tag: 'Vue' } } }, { default: () => 'Vue' }),
        key: 'vue',
      },
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { tag: 'React' } } }, { default: () => 'React' }),
        key: 'react',
      },
      {
        label: () => h(RouterLink, { to: { name: 'forum', query: { tag: 'Python' } } }, { default: () => 'Python' }),
        key: 'python',
      },
    ],
  },
];

const goToTopic = (id:number) => {
  router.push(`/forum/topic/${id}`);
};
</script>

<script lang="ts">
export type topicType={
    id:number,
    title:string,
    author:string,
    content:string,
    category:string,
    tag:string,
    date:string,
    likes:number,
    collects:number,
};

export const topics = ref<topicType[]>([
  { id: 1, title: '如何发布一个新订单？', author: '用户A', content: '这是一个关于如何发布新订单的详细指南。', category: '新手指南',tag:'Vue', date: '2023-01-01',likes:12,collects:21},
  { id: 2, title: '寻找Vue开发者合作项目', author: '用户B', content: '我们正在寻找有经验的Vue开发者加入我们的新项目。', category: '项目合作', tag:'Vue',date: '2023-01-05',likes:13,collects:31 },
  { id: 3, title: '关于平台费用和结算的疑问', author: '用户C', content: '本文解答了关于平台费用、支付流程和结算周期的常见问题。', category: '常见问题', tag:'Vue',date: '2023-01-10' ,likes:14,collects:41},
  { id: 4, title: '分享我的第一个零租项目经验', author: '用户D', content: '我将分享我在零租平台上完成第一个项目的经验和心得。' , category: '经验分享', tag:'Vue',date: '2023-01-15' ,likes:15,collects:51},
]);
</script>

<style scoped>


/* Adjust menu item text color for better visibility */
.n-menu .n-menu-item-content .n-menu-item-content__header {
  color: #333 !important; /* Darker color for better contrast */
}

.n-menu .n-menu-item-content .n-menu-item-content__arrow {
  color: #333 !important; /* Darker color for arrow */
}


.n-card {
  margin-bottom: 20px;
}

.n-list-item {
  cursor: pointer;
  transition: background-color 0.2s;
}

/* .n-list-item:hover {
  background-color: #0f0f0f;
} */

.text-h5 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.text-body-1 {
  font-size: 1rem;
  line-height: 1.6;
  text-align: center;
  padding: 20px;
}
</style>