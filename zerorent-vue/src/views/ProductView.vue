<template>
  <div class="product-container-wrapper">
    <n-card class="main-content">
      <template #header>
        <h2 class="text-h4">布晴山农场产品简介</h2>
      </template>

      <div class="card-text-content">
        <n-grid x-gap="20" y-gap="20" :cols="4" class="product-grid">
          <n-grid-item v-for="(product, index) in products" :key="index">
            <n-card class="product-card">
              <template #header>
                <h3 class="product-title text-h6">{{ product.title }}</h3>
              </template>
              <template #header-extra>
                <p class="product-price text-subtitle-1" v-html="product.price"></p>
              </template>
              <p class="product-description text-body-2" v-html="product.description"></p>
            </n-card>
          </n-grid-item>
        </n-grid>

        <div class="contact-section mt-8">
          <h3 class="contact-title text-h6">购买方式</h3>
          <p class="contact-info text-body-1">添加布晴山客服微信回复产品名购买</p>
          <p class="contact-info text-body-1">联系电话：17325812129（微信同号）</p>
          <p class="contact-info text-body-1">座机：075-26161893</p>
          <n-button tag="a" href="https://weixin.qq.com" target="_blank" type="primary" class="cta-button mt-4">立即联系客服</n-button>
        </div>
      </div>

      <template #footer>
        <p class="text-center text-caption grey-text">&copy; 布晴山农场 - 集体生产，品质保证！感谢同志们对集体事业的关注和支持！</p>
      </template>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import {ref} from 'vue'
import { NCard, NGrid, NGridItem, NButton } from 'naive-ui';

type productType={
  title:string,
  price:string,
  description:string,
}
const products=ref<productType[]>( [
        { title: '1. 白脚芦花鸡', price: '168元/只', description: '使用中草药有机蔬菜喂养的跑山鸡，比市面土鸡略贵，但更加营养美味！肉嫩爽滑，炖煮煲炒皆宜。' },
        { title: '2. 鸡蛋', price: '48元/盒（20枚）', description: '白脚芦花鸡鸡蛋，新鲜土鸡蛋。' },
        { title: '3. 桂味荔枝', price: '48元5斤 | 88元10斤', description: '广东惠州40年老树龄桂味荔枝，六月中旬成熟后手工采摘发货，果期较短，只有十多天，建议在此预售下单，避免错过果期！' },
        { title: '4. 酱香豆干', price: '23元/4袋常规款（150g/袋）<br>18元/2袋家庭款（300g/袋）', description: '正宗平江酱香干首批尝鲜价，鸡汤熬制，两小时小火慢炖，纯手工制作。Q弹鲜辣，片片入味，唇齿留香。' },
        { title: '5. 共创躺平项目', price: '88元/日 | 350元/周 | 1000元/月', description: '乡村集体生活劳动体验，提供吃住，露营、烧烤游玩、组织读书会自律学习。' },
        { title: '6. 钓鱼卡', price: '128元/次', description: '5月中旬开放，让您在山水间放松身心，享受垂钓乐趣。' },
        { title: '7. 农场漫游卡', price: '20元/次', description: '5月中旬开放，露营、烧烤、摄影写生，观赏各种动物，尽情拥抱大自然。' }
      ]);
// export default {
//   name: 'ProductView',
//   components: {
//     NCard,
//     NGrid,
//     NGridItem,
//     NButton
//   },
//   data() {
//     return {
//       products: [
//         { title: '1. 白脚芦花鸡', price: '168元/只', description: '使用中草药有机蔬菜喂养的跑山鸡，比市面土鸡略贵，但更加营养美味！肉嫩爽滑，炖煮煲炒皆宜。' },
//         { title: '2. 鸡蛋', price: '48元/盒（20枚）', description: '白脚芦花鸡鸡蛋，新鲜土鸡蛋。' },
//         { title: '3. 桂味荔枝', price: '48元5斤 | 88元10斤', description: '广东惠州40年老树龄桂味荔枝，六月中旬成熟后手工采摘发货，果期较短，只有十多天，建议在此预售下单，避免错过果期！' },
//         { title: '4. 酱香豆干', price: '23元/4袋常规款（150g/袋）<br>18元/2袋家庭款（300g/袋）', description: '正宗平江酱香干首批尝鲜价，鸡汤熬制，两小时小火慢炖，纯手工制作。Q弹鲜辣，片片入味，唇齿留香。' },
//         { title: '5. 共创躺平项目', price: '88元/日 | 350元/周 | 1000元/月', description: '乡村集体生活劳动体验，提供吃住，露营、烧烤游玩、组织读书会自律学习。' },
//         { title: '6. 钓鱼卡', price: '128元/次', description: '5月中旬开放，让您在山水间放松身心，享受垂钓乐趣。' },
//         { title: '7. 农场漫游卡', price: '20元/次', description: '5月中旬开放，露营、烧烤、摄影写生，观赏各种动物，尽情拥抱大自然。' }
//       ]
//     };
//   }
// }
</script>

<style scoped>
.product-container-wrapper {
  padding: 20px;
}

.main-content {
  max-width: 1200px;
  margin: 0 auto;
}

.text-h4 {
  font-size: 2rem;
  font-weight: bold;
  margin-bottom: 20px;
}

.card-text-content {
  padding: 16px;
}

.product-grid {
  margin-bottom: 40px;
}

.product-card {
  transition: transform 0.3s ease;
  height: 100%; /* Ensure cards in a grid have equal height */
}

.product-card:hover {
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
  transform: translateY(-5px);
}

.product-title {
  font-size: 1.25rem;
  color: #4CAF50;
  margin-bottom: 10px;
}

.product-price {
  font-size: 1.125rem;
  font-weight: bold;
  color: #FF5722;
  margin-bottom: 10px;
}

.product-description {
  font-size: 0.875rem;
  color: #666;
  line-height: 1.6;
}

.contact-section {
  background-color: #f9f9f9;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
  margin-top: 32px;
}

.contact-title {
  font-size: 1.25rem;
  color: #4CAF50;
  margin-bottom: 15px;
}

.contact-info {
  font-size: 1rem;
  margin-bottom: 10px;
}

.cta-button {
  margin-top: 16px;
}

.text-center {
  text-align: center;
}

.text-caption {
  font-size: 0.75rem;
}

.grey-text {
  color: #9aa0a6;
}
</style>