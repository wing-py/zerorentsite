<template>
  <div class="compose-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h5">撰写信函</h2>
      </template>

      <n-form @submit.prevent="submitLetter">
        <n-form-item label="标题">
          <n-input
            v-model:value="title"
            placeholder="请输入标题"
            required
          />
        </n-form-item>

        <n-form-item label="内容">
          <n-input
            v-model:value="content"
            type="textarea"
            placeholder="请输入内容"
            rows="10"
            required
          />
        </n-form-item>

        <n-form-item label="信件类别">
          <n-select
            v-model:value="category"
            :options="categories.map(c => ({ label: c, value: c }))"
            placeholder="请选择信件类别"
            required
          />
        </n-form-item>

        <n-form-item label="公开展示意见">
          <n-select
            v-model:value="displayPermission"
            :options="displayPermissions.map(p => ({ label: p, value: p }))"
            placeholder="请选择公开权限"
          />
        </n-form-item>

        <n-form-item label="附件 (可选)">
          <n-upload
            multiple
            :default-file-list="attachments"
            @change="handleFileUpload"
            accept="image/*"
          >
            <n-button>上传文件</n-button>
          </n-upload>
        </n-form-item>

        <div class="form-actions mt-4">
          <n-button type="primary" @click="submitLetter">发送信函</n-button>
          <n-button @click="goToMailbox" class="ml-2">取消</n-button>
        </div>
      </n-form>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { NCard, NForm, NFormItem, NInput, NSelect, NUpload, NButton} from 'naive-ui';
import type {UploadFileInfo} from 'naive-ui'

const title=ref<string>('');
const content=ref<string>('');
const category=ref<string|null>(null);
const displayPermission=ref<string>('希望展示');
const attachments=ref<UploadFileInfo[] | undefined>();
const categories=ref<string[]>(['技术支持诉求', '组织机制建议', '问题反馈', '个人看法', '其他']);
const displayPermissions=ref<string[]>(['希望展示', '不介意展示', '拒绝展示']);
const handleFileUpload = (data: { fileList: UploadFileInfo[] })  => {
      attachments.value = data.fileList;
    };
const submitLetter = () => {
      console.log('Submitting letter...');
      console.log('Title:', title.value);
      console.log('Content:', content.value);
      console.log('Category:', category.value);
      console.log('Display Permission:', displayPermission.value);
      console.log('Attachments:', attachments.value);
      // Implement letter submission logic here
    };

const router = useRouter();
const goToMailbox = () =>{
      router.push('/mailbox');
    };

</script>

<style scoped>
.compose-container {
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

.form-actions {
  display: flex;
  gap: 10px;
  margin-top: 16px;
}

.ml-2 {
  margin-left: 8px;
}
</style>