<template>
  <section id="services" class="py-24 bg-light-bg">
    <div class="max-w-7xl mx-auto px-6">
      <!-- Section Header -->
      <div class="text-center mb-16 reveal">
        <span class="text-accent-cyan font-semibold text-sm tracking-wider uppercase mb-3 block">Services</span>
        <h2 class="text-3xl md:text-4xl font-bold text-text-light mb-4">业务服务</h2>
        <p class="text-text-light-muted max-w-2xl mx-auto text-lg">
          从数据到产品，从策略到落地，我们提供全链路的技术服务能力
        </p>
      </div>

      <!-- Cards Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        <div
          v-for="item in services"
          :key="item.id"
          class="service-card bg-white rounded-xl p-7 border border-gray-100 reveal"
        >
          <!-- Icon -->
          <div class="w-12 h-12 rounded-xl bg-gradient-to-br from-accent-cyan/10 to-accent-violet/10 flex items-center justify-center mb-5">
            <component :is="getIcon(item.icon)" />
          </div>
          <h3 class="text-xl font-bold text-text-light mb-3">{{ item.title }}</h3>
          <p class="text-text-light-muted leading-relaxed text-sm">{{ item.description }}</p>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, type Component } from 'vue'
import { fetchServices, type ServiceItem } from '@/api'
import IconChart from './icons/IconChart.vue'
import IconDatabase from './icons/IconDatabase.vue'
import IconBot from './icons/IconBot.vue'
import IconMobile from './icons/IconMobile.vue'
import IconMiniprogram from './icons/IconMiniprogram.vue'
import IconWeb from './icons/IconWeb.vue'

const services = ref<ServiceItem[]>([])

const iconMap: Record<string, Component> = {
  chart: IconChart,
  database: IconDatabase,
  bot: IconBot,
  mobile: IconMobile,
  miniprogram: IconMiniprogram,
  web: IconWeb,
}

function getIcon(name: string): Component {
  return iconMap[name] || IconChart
}

onMounted(async () => {
  try {
    services.value = await fetchServices()
  } catch {
    // Fallback to static data
    services.value = [
      { id: 1, title: '数据分析', description: '基于深度学习与统计建模，从海量数据中提取关键洞察，为业务决策提供精准依据。', icon: 'chart', sort_order: 1 },
      { id: 2, title: '数据采集', description: '全链路数据采集方案，覆盖网页抓取、API对接、SDK埋点、日志采集等多种方式。', icon: 'database', sort_order: 2 },
      { id: 3, title: 'Agent 搭建', description: '基于大语言模型构建智能 Agent，实现自动化的数据处理、内容生成与任务编排。', icon: 'bot', sort_order: 3 },
      { id: 4, title: 'App 开发', description: '从需求分析到上架运维的全流程移动应用开发，覆盖 iOS/Android 原生与跨平台方案。', icon: 'mobile', sort_order: 4 },
      { id: 5, title: '小程序开发', description: '微信/支付宝/抖音多端小程序定制开发，轻量触达用户场景。', icon: 'miniprogram', sort_order: 5 },
      { id: 6, title: '网站开发', description: '企业官网、业务系统、SaaS 平台等全栈 Web 开发，现代化技术栈保障性能与安全。', icon: 'web', sort_order: 6 },
    ]
  }
})
</script>
