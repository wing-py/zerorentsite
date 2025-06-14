<template>
  <n-layout-content content-style="padding: 24px;">
    <template v-if="topic">
      <n-card :title="topic.title">
        <template #header-extra>
          <n-space align="center">
            <n-tag type="info" size="small">{{ topic.category }}</n-tag>
            <n-text depth="3">{{ topic.date }}</n-text>
          </n-space>
        </template>
        <p>{{ topic.content }}</p>
        <template #footer>
          <n-space justify="space-between" align="center">
            <n-text depth="3">作者: {{ topic.author }}</n-text>
            <n-space>
              <n-button quaternary circle @click="toggleLike">
                <template #icon>
                  <n-icon :color="isLiked ? 'red' : ''"><HeartOutline  /> </n-icon>
                </template>
                {{ likesCount }}
              </n-button>
              <n-button quaternary circle @click="toggleFavorite">
                <template #icon>
                  <n-icon :color="isFavorited ? 'gold' : ''"><StarOutline /></n-icon>
                </template>
                {{ favoritesCount }}
              </n-button>
            </n-space>
          </n-space>
        </template>
      </n-card>

      <n-card title="评论" style="margin-top: 20px;">
        <n-input
          v-model:value="newCommentContent"
          placeholder="发表你的评论..."
          type="textarea"
          :autosize="{ minRows: 3 }"
        />
        <n-button type="primary" @click="addComment" style="margin-top: 10px;">发表评论</n-button>

        <n-list bordered style="margin-top: 20px;">
          <comment-item
            v-for="comment in comments"
            :key="comment.id"
            :comment="comment"
            @reply="addReply"
          />
          <n-empty v-if="comments===null || comments.length === 0" description="暂无评论" style="padding: 20px;" />
        </n-list>
      </n-card>
    </template>

    <n-empty v-else description="话题未找到" />
    <n-button @click="goBack" style="margin-top: 20px;">返回论坛列表</n-button>
  </n-layout-content>
</template>

<script lang="ts" setup>
import { ref, onMounted } from 'vue';
import { useRoute, useRouter } from 'vue-router';
import { NLayoutContent, NCard, NButton, NTag, NText, NSpace, NEmpty, NIcon, NInput, NList } from 'naive-ui';
import { HeartOutline, StarOutline } from '@vicons/ionicons5';
import CommentItem from '../components/CommentItem.vue'; // 引入评论组件
import { topics } from './ForumListView.vue';
import type {topicType} from './ForumListView.vue';

type commentType={
    id:number,
    author:string,
    content:string,
    date:string,
    replies:commentType[],
}
const route = useRoute();
const router = useRouter();
const topic = ref<topicType|null>(null);
const isLiked = ref<boolean>(false);
const likesCount = ref<number>(0);
const isFavorited = ref<boolean>(false);
const favoritesCount = ref<number>(0);
const newCommentContent = ref<string>('');
const comments = ref<commentType[]|null>(null);

// 模拟数据
// const allTopics = [
//  { id: 1, title: '如何发布一个新订单？', author: '用户A', category: '新手指南', date: '2023-01-01', content: '这是一个关于如何发布新订单的详细指南。' },
//  { id: 2, title: '寻找Vue开发者合作项目', author: '用户B', category: '项目合作', date: '2023-01-05', content: '我们正在寻找有经验的Vue开发者加入我们的新项目。' },
//  { id: 3, title: '关于平台费用和结算的疑问', author: '用户C', category: '常见问题', date: '2023-01-10', content: '本文解答了关于平台费用、支付流程和结算周期的常见问题。' },
//  { id: 4, title: '分享我的第一个零租项目经验', author: '用户D', category: '经验分享', date: '2023-01-15', content: '我将分享我在零租平台上完成第一个项目的经验和心得。' },
// ];

onMounted(() => {
 const topicId = Number(route.params.id);
 topic.value = topics.value.find(t => t.id === topicId) ?? null;
 // 模拟点赞和收藏数据
 likesCount.value = topic.value?.likes ?? 0;
 favoritesCount.value = topic.value?.collects ?? 0;
 // 模拟评论数据
 comments.value = [
   { id: 1, author: '评论者A', content: '这个话题很有帮助！', date: '2023-01-16', replies: [] },
   { id: 2, author: '评论者B', content: '我也有类似的问题。', date: '2023-01-17', replies: [] },
 ];
});

const toggleLike = () => {
 isLiked.value = !isLiked.value;
 if (isLiked.value) {
   likesCount.value++;
 } else {
   likesCount.value--;
 }
};

const toggleFavorite = () => {
 isFavorited.value = !isFavorited.value;
 if (isFavorited.value) {
   favoritesCount.value++;
 } else {
   favoritesCount.value--;
 }
};

const addComment = () => {
 if (newCommentContent.value.trim() === '') return;
 const newComment = {
   id: (comments.value?.length || 0)+1,
   author: '当前用户', // 实际应用中应为当前登录用户
   content: newCommentContent.value,
   date: new Date().toISOString().slice(0, 10),
   replies: [],
 };
 if(comments.value)
 {
    comments.value.push(newComment);
 }
 newCommentContent.value = '';
};

const addReply = (parentCommentId:number, content:string ) => {
 const findCommentAndAddReply = (commentList:commentType[], parentId:number, replyContent:string) => {
   for (const comment of commentList) {
     if (comment.id === parentId && comments.value!=null) {
       comments.value.push({
         id: comment.replies.length + 1,
         author: '当前用户', // 实际应用中应为当前登录用户
         content: replyContent,
         date: new Date().toISOString().slice(0, 10),
         replies: [],
       });
       return true;
     }
     if (comment.replies.length > 0) {
       if (findCommentAndAddReply(comment.replies, parentId, replyContent)) {
         return true;
       }
     }
   }
   return false;
 };
 if(comments.value != null)
 {
    findCommentAndAddReply(comments.value, parentCommentId, content);
 }
};

const goBack = () => {
 router.push('/forum');
};
</script>

<style scoped>
/* 可以添加一些样式 */
</style>