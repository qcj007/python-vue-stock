<template>
  <a-layout has-sider>
    <a-layout-sider
      :style="{ overflow: 'auto', height: '100vh', position: 'fixed', left: 0, top: 0, bottom: 0 }"
    >
      <div class="logo">
        <img src="@/assets/images/logo.png" />
        <h1>牛股选股控台</h1>
      </div>
      <a-menu v-model:selectedKeys="selectedKeys" theme="dark" mode="inline">
        <a-menu-item v-for="item in navList" :key="item.label">
          <TransactionOutlined />
          <span class="nav-text">{{ item.name }}</span>
        </a-menu-item>
      </a-menu>
    </a-layout-sider>
    <a-layout :style="{ marginLeft: '200px' }">
      <a-layout-content :style="{ padding: '20px', overflow: 'initial', height: '100vh' }">
        <div class="content-body" v-resize="onResize">
          <component v-bind:is="pageComponent" v-if="pageComponent"></component>
        </div>
      </a-layout-content>
    </a-layout>
  </a-layout>
</template>
<script setup>
import {
  TransactionOutlined,
  UserOutlined,
  VideoCameraOutlined,
  UploadOutlined,
  BarChartOutlined,
  CloudOutlined,
  AppstoreOutlined,
  TeamOutlined,
  ShopOutlined
} from "@ant-design/icons-vue"
import { useStore } from "vuex"
import { ref, defineAsyncComponent, computed, watch } from "vue"
const selectedKeys = ref([sessionStorage["selectedKeys"] || "stockMyCare"])
const store = useStore()
watch(
  () => selectedKeys.value,
  (value) => {
    sessionStorage["selectedKeys"] = value[0]
  }
)
const onResize = (event) => {
  const { width, height } = event
  store.commit("setData", { contWidth: width, contHeight: height })
}

const navList = [
  {
    label: "stocksOpportunity",
    name: "股票框架"
  },
  {
    label: "stockMyCare",
    name: "我的自选"
  },
  {
    label: "stockAISelet",
    name: "AI条件选股"
  },

  {
    label: "stockConcept",
    name: "概念股票"
  },
  {
    label: "stockCycle",
    name: "周期股票"
  },
  {
    label: "stockEvents",
    name: "股票事件"
  },

  {
    label: "stockZcw",
    name: "所有股票"
  }
]

//vite需要用glob来异步import，不然启动会报错
const modules = import.meta.glob("./page/*.vue")

const pageComponent = computed(() => {
  const pageName = selectedKeys.value[0]
  if (pageName) {
    if (modules[`./page/${pageName}.vue`]) {
      return defineAsyncComponent(modules[`./page/${pageName}.vue`])
    }
  }
  return null
})
</script>
<style scoped="scoped">
.content-body {
  padding: 10px 10px 0 10px;
  background: #fff;

  height: 100%;
  border-radius: 8px;
}
#components-layout-demo-fixed-sider .logo {
  height: 32px;
  background: rgba(255, 255, 255, 0.2);
  margin: 16px;
}
.site-layout .site-layout-background {
  background: #fff;
}

[data-theme="dark"] .site-layout .site-layout-background {
  background: #141414;
}
</style>
