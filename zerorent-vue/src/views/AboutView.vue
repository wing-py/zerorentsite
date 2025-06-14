<template>
  <div class="about-container">
    <n-card class="main-content">
      <h1 class="translatable text-h4">零抽成开发外包平台</h1>

      <div class="card-text-content">
        <div class="section">
          <h2 class="translatable text-h5">该平台的目的</h2>

          <h3 class="translatable text-h6">1. 第一目的：零抽成</h3>
          <p class="translatable text-body-1">
            使开发者不必忍受外包业务非零抽成，使用各种方法机制来保障这一点，并在这一点基础上探索和发展。
          </p>

          <h3 class="translatable text-h6">2. 第二目的：建立开发者间的联合</h3>
          <p class="translatable text-body-1">
            开发者联合起来，以通过这种联合实现一些潜在的可能性，如一起实现一些较大的项目。
          </p>
        </div>

        <div class="section">
          <h2 class="translatable text-h5">如何启动？</h2>

          <h3 class="translatable text-h6">一、拉开发者</h3>

          <h4 class="translatable text-subtitle-1">私人关系</h4>
          <ul>
            <li>wing-全栈</li>
            <li>jl</li>
            <li>ljh</li>
            <li>hsx-PCB设计</li>
            <li>xt</li>
          </ul>

          <h4 class="translatable text-subtitle-1">去相关群聊里偷人</h4>
          <ol>
            <li>假装加入某淘宝店铺</li>
            <li>到他群聊里私聊人偷人</li>
          </ol>

          <h4 class="translatable text-subtitle-1">去相关公司偷人</h4>
          <p class="translatable text-body-1">延后</p>
        </div>

        <div class="section">
          <h3 class="translatable text-h6">二、拉订单</h3>

          <h4 class="translatable text-subtitle-1">在网络渠道发布订单信息</h4>

          <h5 class="translatable text-subtitle-2">电商平台</h5>
          <ol>
            <li>淘宝店铺</li>
            <li>咸鱼店铺</li>
          </ol>

          <h5 class="translatable text-subtitle-2">媒体平台</h5>
          <ol>
            <li>b站-官号</li>
            <li>b站-友情宣传-ybx</li>
          </ol>

          <h5 class="translatable text-subtitle-2">自营网站</h5>
          <p class="translatable text-body-1">做到无漏洞的零抽成</p>

          <h5 class="translatable text-subtitle-2">推销人员</h5>
          <p class="translatable text-body-1">ybx</p>
        </div>

        <div class="section">
          <h3 class="translatable text-h6">三、平台自身资料</h3>
          <ul>
            <li>平台自身介绍</li>
            <li>分工分配机制</li>
            <li>相关群聊渠道</li>
            <li>原则保障制度</li>
            <li>平台管理网站</li>
          </ul>
        </div>

        <div class="section">
          <h2 class="translatable text-h5">作业流程</h2>

          <h3 class="translatable text-h6">订单发布</h3>
          <ol>
            <li>
              私人来源的订单
              <ul>
                <li>将订单发布到公共信息区</li>
                <li>如有需要，附加其它具体信息</li>
                <li>如聊天信息需截图以确保零抽成</li>
              </ul>
            </li>
            <li>
              平台公共渠道的订单：
              <ul>
                <li>淘宝店铺-公布淘宝订单和收付款</li>
                <li>微信群聊</li>
                <li>平台网站</li>
              </ul>
            </li>
          </ol>
        </div>

        <div class="section">
          <h3 class="translatable text-h6">接取订单</h3>
          <ol>
            <li>
              个人订单
              <p class="translatable text-body-1">
                优先个人接取个人就能完成的订单，金钱交易完全在个人那里完成。
              </p>
            </li>
            <li>
              合作订单
              <p class="translatable text-body-1">
                合作订单如何分工分配由合作团体自行决定，平台提供以下参考方案：
              </p>
            </li>
          </ol>
        </div>

        <div class="section">
          <h2 class="translatable text-h5">发展阶段</h2>
          <ul>
            <li>开发人员档案</li>
            <li>共用开发框架</li>
            <li>开放学习资料</li>
          </ul>
        </div>

        <div class="section">
          <h2 class="translatable text-h5">风险预防</h2>
          <ol>
            <li>由于夺取非零抽成外包平台的抽成费，他们可能持敌视态度，要预防其可能带来的风险</li>
          </ol>
        </div>
      </div>
    </n-card>
  </div>
</template>

<script lang="ts" setup>
import { NCard } from 'naive-ui'
</script>

<style scoped>
.about-container {
  padding: 20px;
}

.main-content {
  margin-bottom: 20px;
}

.card-text-content {
  padding: 16px; /* Default padding for card content */
}

.section {
  margin-bottom: 20px;
}

h1,
h2,
h3,
h4,
h5 {
  margin-bottom: 10px;
  /* color: #333; */
}

ul,
ol {
  margin-left: 20px;
  margin-bottom: 10px;
}

li {
  margin-bottom: 5px;
}

.text-h4 {
  font-size: 2rem;
  font-weight: bold;
}

.text-h5 {
  font-size: 1.5rem;
  font-weight: bold;
}

.text-h6 {
  font-size: 1.25rem;
  font-weight: bold;
}

.text-subtitle-1 {
  font-size: 1rem;
  font-weight: bold;
}

.text-subtitle-2 {
  font-size: 0.875rem;
  font-weight: bold;
}

.text-body-1 {
  font-size: 1rem;
  line-height: 1.6;
}
</style>
