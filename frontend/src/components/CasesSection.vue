<template>
  <section id="cases" class="py-24 bg-dark-surface">
    <div class="max-w-7xl mx-auto px-6">
      <!-- Section Header -->
      <div class="text-center mb-16 reveal">
        <span class="text-accent-cyan font-semibold text-sm tracking-wider uppercase mb-3 block">Cases</span>
        <h2 class="text-3xl md:text-4xl font-bold text-white mb-4">案例展示</h2>
        <p class="text-text-dark-muted max-w-2xl mx-auto text-lg">
          深耕数据与开发领域，以下是我们为各行业客户交付的部分代表性项目
        </p>
      </div>

      <!-- Cases Grid -->
      <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div
          v-for="item in cases"
          :key="item.id"
          class="case-card bg-dark-card rounded-xl overflow-hidden border border-white/5 reveal"
        >
          <!-- Case Image -->
          <div class="h-48 overflow-hidden">
            <img
              v-if="item.image"
              :src="item.image"
              :alt="item.title"
              class="w-full h-full object-cover"
            />
            <div v-else class="w-full h-full bg-gradient-to-br from-accent-cyan/20 to-accent-violet/20 flex items-center justify-center">
              <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(6,182,212,0.5)" stroke-width="1.5" stroke-linecap="round" stroke-linejoin="round">
                <rect x="3" y="3" width="18" height="18" rx="2" /><circle cx="8.5" cy="8.5" r="1.5" /><path d="m21 15-5-5L5 21" />
              </svg>
            </div>
          </div>
          <div class="p-6">
            <h3 class="text-lg font-bold text-white mb-2">{{ item.title }}</h3>
            <p class="text-text-dark-muted text-sm leading-relaxed mb-4">{{ item.description }}</p>
            <div class="flex flex-wrap gap-2">
              <span
                v-for="tag in item.tags.split(',')"
                :key="tag"
                class="text-xs px-2.5 py-1 rounded-md bg-accent-cyan/10 text-accent-cyan font-medium"
              >
                {{ tag.trim() }}
              </span>
            </div>
          </div>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchCases, type CaseItem } from '@/api'

const cases = ref<CaseItem[]>([])

onMounted(async () => {
  try {
    cases.value = await fetchCases()
  } catch {
    cases.value = [
      { id: 1, title: '某电商平台用户行为分析系统', description: '为头部电商平台搭建全链路用户行为分析体系，日均处理 2 亿+事件数据，将用户转化率提升 34%。', image: '', tags: '数据分析,数据采集', sort_order: 1 },
      { id: 2, title: '智能客服 Agent 系统', description: '基于大语言模型构建多轮对话 Agent，集成知识库检索与工单系统，客户问题自动解决率达 78%。', image: '', tags: 'Agent搭建,AI应用', sort_order: 2 },
      { id: 3, title: '连锁零售数据中台', description: '为 2000+ 门店的连锁零售品牌搭建统一数据中台，实现经营日报自动化与智能补货建议。', image: '', tags: '数据分析,系统开发', sort_order: 3 },
      { id: 4, title: '智慧社区小程序矩阵', description: '覆盖 50+ 社区的微信小程序矩阵，涵盖物业缴费、报修、社区商城，月活用户超 30 万。', image: '', tags: '小程序开发,App开发', sort_order: 4 },
    ]
  }
})
</script>
