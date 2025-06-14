<template>
  <div class="link-container">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-center text-h4">布晴山农场</h2>
      </template>
      <template #header-extra>
        <p class="text-center">欢迎关注我们的媒体账号</p>
      </template>

      <div class="card-text-content">
        <n-list hoverable clickable>
          <n-list-item>
            <n-thing title="哔哩哔哩">
              <template #avatar>
                <!-- <n-icon><BilibiliIcon /></n-icon> -->
              </template>
            </n-thing>
          </n-list-item>
          <n-list-item v-for="account in bilibiliAccounts" :key="account.name">
            <n-thing
              :title="account.name"
              :description="account.description"
              @click="openLink(account.link)"
            >
              <template #avatar>
                <n-avatar :src="account.icon" :alt="account.name" />
              </template>
              <template #header-extra>
                <!-- <n-icon><LinkIcon /></n-icon> -->
              </template>
            </n-thing>
          </n-list-item>
        </n-list>

        <n-list hoverable clickable class="mt-4">
          <n-list-item>
            <n-thing title="抖音">
              <template #avatar>
                <!-- <n-icon><TikTokIcon /></n-icon> -->
              </template>
            </n-thing>
          </n-list-item>
          <n-list-item v-for="account in douyinAccounts" :key="account.name">
            <n-thing
              :title="account.name"
              :description="account.description"
              @click="openLink(account.link)"
            >
              <template #avatar>
                <n-avatar :src="account.icon" :alt="account.name" />
              </template>
              <template #header-extra>
                <!-- <n-icon><LinkIcon /></n-icon> -->
              </template>
            </n-thing>
          </n-list-item>
        </n-list>
      </div>

      <template #footer>
        <p class="text-center text-caption grey-text">&copy; 2023 布晴山农场 版权所有</p>
      </template>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { ref } from 'vue'
import { NCard, NList, NListItem, NThing, NAvatar } from 'naive-ui';
// import { Bilibili as BilibiliIcon, TikTok as TikTokIcon, Link as LinkIcon } from '@vicons/fa'; // Uncomment and install @vicons/fa if you want to use icons

type accountType={
    name:string,
    description:string,
    icon:string,
    link:string,
}

const bilibiliAccounts=ref<accountType[]>([
        { name: '布晴山数字集体农场', description: '布晴山数字集体农场的官方账号', icon: 'https://i0.hdslb.com/bfs/face/4ec794b28fa7c6262ad6746416b217a0d3103dc0.jpg', link: 'https://space.bilibili.com/1622776854?spm_id_from=333.337.search-card.all.click' },
        { name: '海星同志', description: '00后，布晴山数字集体农场的一位普通成员', icon: 'https://i1.hdslb.com/bfs/face/616812e35beba0a3d6dd1104949854412b0472d3.jpg', link: 'https://space.bilibili.com/84064954?spm_id_from=333.337.search-card.all.click' },
        { name: '布晴山种养日常号', description: '重生之我在布晴山集体农场做养殖—王莽', icon: 'https://i0.hdslb.com/bfs/face/73d28b25c199908d1343b2d6396bab917a4bd552.jpg', link: 'https://space.bilibili.com/3546842799278586?spm_id_from=333.337.search-card.all.click' }
      ]);
const douyinAccounts=ref<accountType[]>([
        { name: '布晴山数字集体农场', description: '布晴山数字集体农场的官方抖音账号', icon: 'https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/emblem.png', link: 'https://www.douyin.com/user/MS4wLjABAAAAz5vKt8yO_IMu5MZHUrz1rnSIe3uZbq50zKn1D4pMH3irje2KoMKhVO7dPwfvY6e-' },
        { name: '布晴山·养殖日常', description: '布晴山养殖日常的抖音账号', icon: 'https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/emblem.png', link: 'https://www.douyin.com/user/MS4wLjABAAAAQGuB7j0HIFWMWGXQisF791nFVbVMJxaUk6MYT3DXVvo?from_tab_name=main' },
        { name: '布晴山·海星同志', description: '海星同志的抖音账号', icon: 'https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/emblem.png', link: 'https://www.douyin.com/user/MS4wLjABAAAAnywmLLyHJq1m8R8lQGPGmPEpa-75vEvNVRFrB--lFkAmSBTh1TkRz01v7WEWdi16?from_tab_name=main' }
      ]);

const openLink = (link:string) => {
      window.open(link, '_blank');
}

// export default {
//   name: 'LinkView',
//   components: {
//     NCard,
//     NList,
//     NListItem,
//     NThing,
//     NAvatar,
//     // BilibiliIcon, // Uncomment if using icons
//     // TikTokIcon,   // Uncomment if using icons
//     // LinkIcon      // Uncomment if using icons
//   },
//   data() {
//     return {
//       bilibiliAccounts: [
//         { name: '布晴山数字集体农场', description: '布晴山数字集体农场的官方账号', icon: 'https://i0.hdslb.com/bfs/face/4ec794b28fa7c6262ad6746416b217a0d3103dc0.jpg', link: 'https://space.bilibili.com/1622776854?spm_id_from=333.337.search-card.all.click' },
//         { name: '海星同志', description: '00后，布晴山数字集体农场的一位普通成员', icon: 'https://i1.hdslb.com/bfs/face/616812e35beba0a3d6dd1104949854412b0472d3.jpg', link: 'https://space.bilibili.com/84064954?spm_id_from=333.337.search-card.all.click' },
//         { name: '布晴山种养日常号', description: '重生之我在布晴山集体农场做养殖—王莽', icon: 'https://i0.hdslb.com/bfs/face/73d28b25c199908d1343b2d6396bab917a4bd552.jpg', link: 'https://space.bilibili.com/3546842799278586?spm_id_from=333.337.search-card.all.click' }
//       ],
//       douyinAccounts: [
//         { name: '布晴山数字集体农场', description: '布晴山数字集体农场的官方抖音账号', icon: 'https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/emblem.png', link: 'https://www.douyin.com/user/MS4wLjABAAAAz5vKt8yO_IMu5MZHUrz1rnSIe3uZbq50zKn1D4pMH3irje2KoMKhVO7dPwfvY6e-' },
//         { name: '布晴山·养殖日常', description: '布晴山养殖日常的抖音账号', icon: 'https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/emblem.png', link: 'https://www.douyin.com/user/MS4wLjABAAAAQGuB7j0HIFWMWGXQisF791nFVbVMJxaUk6MYT3DXVvo?from_tab_name=main' },
//         { name: '布晴山·海星同志', description: '海星同志的抖音账号', icon: 'https://p3-pc-weboff.byteimg.com/tos-cn-i-9r5gewecjs/emblem.png', link: 'https://www.douyin.com/user/MS4wLjABAAAAnywmLLyHJq1m8R8lQGPGmPEpa-75vEvNVRFrB--lFkAmSBTh1TkRz01v7WEWdi16?from_tab_name=main' }
//       ]
//     };
//   },
//   methods: {
//     openLink(link) {
//       window.open(link, '_blank');
//     }
//   }
// }
</script>

<style scoped>
.link-container {
  padding: 20px;
}

.main-content {
  max-width: 800px;
  margin: 0 auto;
}

.text-center {
  text-align: center;
}

.text-h4 {
  font-size: 2rem;
  font-weight: bold;
}

.card-text-content {
  padding: 16px;
}

.mt-4 {
  margin-top: 16px;
}

.text-caption {
  font-size: 0.75rem;
}

.grey-text {
  color: #9aa0a6;
}
</style>