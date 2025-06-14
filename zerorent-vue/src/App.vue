<template>
  <n-config-provider
    :theme="darkTheme"
    :theme-overrides="{ common: { fontWeightStrong: '600' } }"
    style="height: 100vh"
  >
    <n-message-provider>
      <n-dialog-provider>
        <n-notification-provider>
          <n-loading-bar-provider>
            <n-layout position="absolute">
              <n-space vertical size="large">
                <n-layout-header
                  style="
                    padding: 10px 10px;
                    display: flex;
                    align-items: center;
                    justify-content: space-between;
                  "
                >
                  <n-space justify="space-between">
                    <div style="display: flex; align-self: flex-start">
                      <img
                        src="/public/favicon.ico"
                        alt="Logo"
                        style="height: 40px; margin-right: 15px"
                      />
                      <n-text
                        strong
                        :depth="1"
                        style="font-size: 24px; padding: 0px"
                        content-style="padding: 240px"
                        >共建社区</n-text
                      >
                    </div>
                  </n-space>

                  <n-space justify="space-between">
                    <div style="flex-grow: 1; display: flex; justify-content: flex-end">
                      <n-menu mode="horizontal" :options="menuOptions" />
                    </div>
                  </n-space>
                </n-layout-header>
              </n-space>
              <n-layout-content content-style="padding: 24px;">
                <router-view />
              </n-layout-content>
            </n-layout>
          </n-loading-bar-provider>
        </n-notification-provider>
      </n-dialog-provider>
    </n-message-provider>
  </n-config-provider>
</template>

<script lang="ts">
export const isLogined = ref<boolean>(false)
</script>

<script lang="ts" setup>
import {
  NConfigProvider,
  NMessageProvider,
  NDialogProvider,
  NNotificationProvider,
  NLoadingBarProvider,
  NLayout,
  NLayoutHeader,
  NLayoutContent,
  NMenu,
  NText,
  darkTheme,
  lightTheme,
} from 'naive-ui'
import { h, ref, computed } from 'vue'
import { RouterLink } from 'vue-router'
import type { MenuOption } from 'naive-ui'

const menuOptions = computed<MenuOption[]>(() => [
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'home',
          },
        },
        { default: () => '首页' },
      ),
    key: 'home',
    disabled: false,
    show: true,
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'about',
          },
        },
        { default: () => '介绍' },
      ),
    key: 'about',
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'forum',
          },
        },
        { default: () => '论坛' },
      ),
    key: 'forum',
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'submit-order',
          },
        },
        { default: () => '发布订单' },
      ),
    key: 'submit-order',
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'list-order',
          },
        },
        { default: () => '浏览订单' },
      ),
    key: 'list-order',
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'list-worker',
          },
        },
        { default: () => '寻找开发者' },
      ),
    key: 'list-worker',
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: isLogined.value ? 'logout' : 'login',
          },
        },
        {
          default: () => {
            return isLogined.value ? '注销' : '登录'
          },
        },
      ),
    key: 'login',
  },
  {
    label: () =>
      h(
        RouterLink,
        {
          to: {
            name: 'register',
          },
        },
        { default: () => '注册' },
      ),
    key: 'register',
    show: !isLogined.value,
  },
])
</script>

<style>
html,
body,
#app {
  margin: 0;
  padding: 0;
  width: 100%;
  height: 100%;
  overflow: hidden; /* Prevent scrollbars if content is smaller than viewport */
}
</style>
