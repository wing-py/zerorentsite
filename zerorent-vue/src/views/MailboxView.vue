<template>
  <div class="mailbox-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">信函列表</h2>
      </template>

      <div class="card-text-content">
        <div class="search-bar d-flex align-center mb-4">
          <n-input
            v-model:value="searchQuery"
            placeholder="搜索信函..."
            clearable
            class="mr-2"
          />
          <n-button type="primary" @click="searchLetters">搜索</n-button>
        </div>

        <n-list v-if="letters && letters.length > 0" hoverable clickable>
          <n-list-item v-for="letter in letters" :key="letter.id" @click="goToLetterDetail(letter.id)">
            <n-thing
              :title="letter.title"
              :description="formatLetterSubtitle(letter)"
            >
              <p class="text-body-2 mt-2">{{ truncateContent(letter.content) }}</p>
            </n-thing>
          </n-list-item>
        </n-list>
        <div v-else class="text-center text-body-1 grey-text">
          <p class="no-letters translatable">暂无信函</p>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>

import {ref} from 'vue';
import { useRouter } from 'vue-router';
import { NCard, NInput, NButton, NList, NListItem, NThing } from 'naive-ui';
import type {letterType} from './LetterDetailView.vue';

const searchQuery=ref<string>('');
const letters=ref<letterType[]>([
        { id: 1,
            title: '示例信函一',
            category: '问题反馈',
            created_at: '2023-10-26 10:00',
            author: { username: '作者一' },
            content: '这是第一封示例信函的内容，非常长，需要截断显示。这是第一封示例信函的内容，非常长，需要截断显示。这是第一封示例信函的内容，非常长，需要截断显示。',
            attachments:null,
            display_permission:'',
            ip_address:'127.0.0.1',
        },
        { id: 2,
            title: '示例信函二',
            category: '组织机制建议',
            created_at: '2023-10-26 11:00',
            author: { username: '作者二' },
            content: '这是第二封示例信函的内容...',
            attachments:null,
            display_permission:'',
            ip_address:'127.0.0.1',
        }
      ]);


const searchLetters = ()=> {
      console.log('Searching for:', searchQuery.value);
    };
const router=useRouter();
const goToLetterDetail = (id:number) => {
      router.push('/mailbox/' + id);
    };
const formatLetterSubtitle = (letter:letterType):string => {
      let subtitle:string = `${letter.category} ${letter.created_at}`;
      if (letter.author) {
        subtitle += ` 作者: ${letter.author.username}`;
      }
      return subtitle;
    };

const truncateContent = (content:string):string => {
      const maxLength = 100;
      return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
    };
// export default {
//   name: 'MailboxView',
//   components: {
//     NCard,
//     NInput,
//     NButton,
//     NList,
//     NListItem,
//     NThing
//   },
//   data() {
//     return {
//       searchQuery: '',
//       letters: [
//         { id: 1, title: '示例信函一', category: '问题反馈', content: '这是第一封示例信函的内容，非常长，需要截断显示。这是第一封示例信函的内容，非常长，需要截断显示。这是第一封示例信函的内容，非常长，需要截断显示。', created_at: '2023-10-26 10:00', author: { username: '作者一' } },
//         { id: 2, title: '示例信函二', category: '组织机制建议', content: '这是第二封示例信函的内容...', created_at: '2023-10-26 11:00', author: { username: '作者二' } }
//       ]
//     };
//   },
//   methods: {
//     searchLetters() {
//       console.log('Searching for:', this.searchQuery);
//       // Implement search logic here
//     },
//     goToLetterDetail(id) {
//       this.$router.push('/mailbox/' + id);
//     },
//     formatLetterSubtitle(letter) {
//       let subtitle = `${letter.category} ${letter.created_at}`;
//       if (letter.author) {
//         subtitle += ` 作者: ${letter.author.username}`;
//       }
//       return subtitle;
//     },
//     truncateContent(content) {
//       const maxLength = 100;
//       return content.length > maxLength ? content.substring(0, maxLength) + '...' : content;
//     }
//   }
// }
</script>

<style scoped>
.mailbox-container {
  padding: 20px;
}

.main-content {
  max-width: 900px;
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

.search-bar {
  display: flex;
  align-items: center;
  margin-bottom: 16px;
}

.mr-2 {
  margin-right: 8px;
}

.text-center {
  text-align: center;
}

.text-body-1 {
  font-size: 1rem;
  line-height: 1.6;
}

.text-body-2 {
  font-size: 0.875rem;
  line-height: 1.6;
}

.grey-text {
  color: #9aa0a6;
}

.no-letters {
  margin-top: 20px;
}
</style>