<template>
  <n-list-item>
    <n-thing :title="comment.author" :description="comment.date">
      <p>{{ comment.content }}</p>
      <template #footer>
        <n-space justify="end">
          <n-button text @click="showReplyInput = !showReplyInput">回复</n-button>
        </n-space>
        <n-input
          v-if="showReplyInput"
          v-model:value="replyContent"
          placeholder="回复评论..."
          type="textarea"
          :autosize="{ minRows: 2 }"
          style="margin-top: 10px;"
        />
        <n-button
          v-if="showReplyInput"
          type="primary"
          size="small"
          style="margin-top: 5px;"
          @click="submitReply"
        >
          提交回复
        </n-button>
      </template>
    </n-thing>
    <div v-if="comment.replies && comment.replies.length > 0" style="margin-left: 20px; border-left: 2px solid #eee; padding-left: 10px;">
      <comment-item
        v-for="reply in comment.replies"
        :key="reply.id"
        :comment="reply"
        @reply="$emit('reply', $event)"
      />
    </div>
  </n-list-item>
</template>

<script lang="ts" setup>
import { ref } from 'vue';
import { NListItem, NThing, NButton, NSpace, NInput } from 'naive-ui';

const props = defineProps({
  comment: {
    type: Object,
    required: true,
  },
});

const emit = defineEmits(['reply']);

const showReplyInput = ref<boolean>(false);
const replyContent = ref<string>('');

const submitReply = () => {
  if (replyContent.value.trim() === '') return;
  emit('reply', { parentCommentId: props.comment.id, content: replyContent.value });
  replyContent.value = '';
  showReplyInput.value = false;
};
</script>

<style scoped>
/* 可以添加一些样式 */
</style>