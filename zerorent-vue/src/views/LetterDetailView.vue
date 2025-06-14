<template>
  <div class="letter-detail-container">
    <n-card class="letter-detail">
      <template #header>
        <h2 class="text-h5">{{ letter.title }}</h2>
      </template>

      <div class="card-content">
        <div class="letter-info text-caption grey-text">
          <span class="category mr-2">{{ letter.category }}</span>
          <span class="date mr-2">{{ letter.created_at }}</span>
          <span v-if="letter.author" class="author">作者: {{ letter.author.username }}</span>
        </div>

        <n-divider class="my-4"></n-divider>

        <div class="letter-content text-body-1">
          <p>{{ letter.content }}</p>
        </div>

        <div v-if="letter.attachments && letter.attachments.length > 0" class="attachments mt-4">
          <h3 class="text-h6">附件</h3>
          <n-grid x-gap="12" y-gap="12" :cols="4" class="attachments-grid">
            <n-grid-item v-for="attachment in letter.attachments" :key="attachment.filename" class="attachment-item">
              <n-image
                :src="'/static/images/uploads/' + attachment.filename"
                :alt="attachment.filename"
                width="100"
                height="100"
                object-fit="cover"
              />
              <p class="text-caption text-center">{{ attachment.filename }}</p>
            </n-grid-item>
          </n-grid>
        </div>

        <n-divider class="my-4"></n-divider>

        <div class="letter-footer text-caption grey-text">
          <span class="display-permission mr-2">公开展示意见: {{ letter.display_permission }}</span>
          <span class="ip-info">发送IP: {{ letter.ip_address }}</span>
        </div>

        <div class="letter-actions mt-4">
          <n-button @click="goToMailbox">返回信箱</n-button>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts">
export type letterType = {
    id:number,
    title:string,
    category:string,
    created_at:string,
    author:{username:string},
    content: string,
    attachments:{filename:string}[]|null,
    display_permission:string,
    ip_address:string,

};
</script>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRouter } from "vue-router";
import { NCard, NDivider, NGrid, NGridItem, NImage, NButton } from 'naive-ui';

const props = defineProps({
  letterId: {
    type: Number,
    required: true,
    default:0
  },
});

const letter=ref<letterType>({
        id: props.letterId,
        title: '示例信函标题',
        category: '问题反馈',
        created_at: '2023-10-27 10:00',
        author: { username: '示例作者' },
        content: '这是示例信函的内容。',
        attachments: [
          { filename: 'image1.jpg' },
          { filename: 'document.pdf' }
        ],
        display_permission: '希望展示',
        ip_address: '192.168.1.1'
      });

onMounted(()=> {
    // console.log('Fetching details for letter:', props.laterId);
  });
const router = useRouter();
const goToMailbox= () => {
      router.push('/mailbox');
}

// export default {
//   name: 'LetterDetailView',
//   components: {
//     NCard,
//     NDivider,
//     NGrid,
//     NGridItem,
//     NImage,
//     NButton
//   },
//   props: ['letterId'],
//   data() {
//     return {
//       letter: {
//         id: this.letterId,
//         title: '示例信函标题',
//         category: '问题反馈',
//         created_at: '2023-10-27 10:00',
//         author: { username: '示例作者' },
//         content: '这是示例信函的内容。',
//         attachments: [
//           { filename: 'image1.jpg' },
//           { filename: 'document.pdf' }
//         ],
//         display_permission: '希望展示',
//         ip_address: '192.168.1.1'
//       }
//     };
//   },
//   mounted() {
//     console.log('Fetching details for letter:', this.letterId);
//   },
//   methods: {
//     goToMailbox() {
//       this.$router.push('/mailbox');
//     }
//   }
// }
</script>

<style scoped>
.letter-detail-container {
  padding: 20px;
}

.letter-detail {
  max-width: 800px;
  margin: 0 auto;
}

.card-content {
  padding: 16px;
}

.text-h5 {
  font-size: 1.5rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.letter-info {
  color: #9aa0a6;
  font-size: 0.75rem; /* text-caption */
}

.category {
  background-color: #e8eaed;
  color: #5f6368;
  padding: 4px 8px;
  border-radius: 16px;
  font-size: 0.75rem;
}

.mr-2 {
  margin-right: 8px;
}

.my-4 {
  margin-top: 16px;
  margin-bottom: 16px;
}

.letter-content p {
  color: #5f6368;
  margin-bottom: 15px;
  word-break: break-all;
  font-size: 1rem; /* text-body-1 */
  line-height: 1.6;
}

.attachments {
  margin-top: 16px;
}

.text-h6 {
  font-size: 1.25rem;
  font-weight: bold;
  margin-bottom: 10px;
}

.attachments-grid {
  display: flex;
  flex-wrap: wrap;
  gap: 15px;
}

.attachment-item {
  text-align: center;
}

.attachment-item .n-image {
  border-radius: 4px;
}

.text-center {
  text-align: center;
}

.letter-footer {
  color: #9aa0a6;
  font-size: 0.75rem; /* text-caption */
  margin-top: 16px;
}

.letter-actions {
  margin-top: 16px;
}
</style>