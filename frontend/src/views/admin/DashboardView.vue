<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { fetchDashboardStats, getMe, type DashboardStats, type UserInfo } from '@/api'

const router = useRouter()
const route = useRoute()
const stats = ref<DashboardStats | null>(null)
const user = ref<UserInfo | null>(null)
const loading = ref(true)

const navItems = [
  { name: '概览', path: '/admin', icon: 'dashboard' },
  { name: '项目管理', path: '/admin/projects', icon: 'project' },
  { name: '用户管理', path: '/admin/users', icon: 'users' },
  { name: '咨询留言', path: '/admin/messages', icon: 'messages' },
]

function logout() {
  localStorage.removeItem('admin_token')
  localStorage.removeItem('admin_user')
  router.push('/admin/login')
}

onMounted(async () => {
  try {
    const [statsData, userData] = await Promise.all([fetchDashboardStats(), getMe()])
    stats.value = statsData
    user.value = userData
  } catch {
    logout()
  } finally {
    loading.value = false
  }
})
</script>

<template>
  <div class="min-h-screen bg-[#0a0e1a] flex">
    <!-- Sidebar -->
    <aside class="w-60 bg-[#0f172a] border-r border-[#1e293b] flex flex-col fixed h-full">
      <div class="p-5 border-b border-[#1e293b]">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#06b6d4] to-[#8b5cf6] flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
              <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
            </svg>
          </div>
          <span class="text-white font-bold text-sm">聚宁数据</span>
        </div>
      </div>

      <nav class="flex-1 p-3 space-y-1">
        <router-link
          v-for="item in navItems"
          :key="item.path"
          :to="item.path"
          class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm transition-colors"
          :class="route.path === item.path ? 'bg-[#06b6d4]/10 text-[#06b6d4]' : 'text-[#94a3b8] hover:text-white hover:bg-[#1e293b]'"
        >
          {{ item.name }}
        </router-link>
      </nav>

      <div class="p-3 border-t border-[#1e293b]">
        <div class="flex items-center gap-2 px-3 py-2 text-sm text-[#94a3b8]">
          <span>{{ user?.display_name || user?.username || '' }}</span>
          <span v-if="user?.role === 'admin'" class="text-[10px] px-1.5 py-0.5 rounded bg-[#06b6d4]/20 text-[#06b6d4]">管理员</span>
        </div>
        <button @click="logout" class="w-full text-left px-3 py-2 text-sm text-[#64748b] hover:text-red-400 transition-colors">
          退出登录
        </button>
      </div>
    </aside>

    <!-- Main Content -->
    <main class="flex-1 ml-60 p-8">
      <h1 class="text-xl font-bold text-white mb-6">数据概览</h1>

      <div v-if="loading" class="text-[#94a3b8]">加载中...</div>

      <div v-else-if="stats" class="space-y-6">
        <!-- Stats Cards -->
        <div class="grid grid-cols-2 lg:grid-cols-4 gap-4">
          <div class="bg-[#1e293b] rounded-xl p-5">
            <p class="text-[#94a3b8] text-sm mb-1">项目总数</p>
            <p class="text-3xl font-bold text-white">{{ stats.total }}</p>
          </div>
          <div class="bg-[#1e293b] rounded-xl p-5">
            <p class="text-[#94a3b8] text-sm mb-1">进行中</p>
            <p class="text-3xl font-bold text-[#06b6d4]">{{ stats.in_progress }}</p>
          </div>
          <div class="bg-[#1e293b] rounded-xl p-5">
            <p class="text-[#94a3b8] text-sm mb-1">已完成</p>
            <p class="text-3xl font-bold text-green-400">{{ stats.completed }}</p>
          </div>
          <div class="bg-[#1e293b] rounded-xl p-5">
            <p class="text-[#94a3b8] text-sm mb-1">未结算</p>
            <p class="text-3xl font-bold text-amber-400">{{ stats.unsettled }}</p>
          </div>
        </div>

        <div class="grid grid-cols-1 lg:grid-cols-2 gap-4">
          <div class="bg-[#1e293b] rounded-xl p-5">
            <p class="text-[#94a3b8] text-sm mb-1">待开始</p>
            <p class="text-3xl font-bold text-[#8b5cf6]">{{ stats.pending }}</p>
          </div>
          <div class="bg-[#1e293b] rounded-xl p-5">
            <p class="text-[#94a3b8] text-sm mb-1">总报价额</p>
            <p class="text-3xl font-bold text-white">¥{{ stats.total_quote.toLocaleString() }}</p>
          </div>
        </div>

        <!-- Quick Actions -->
        <div class="flex gap-4 mt-4">
          <router-link to="/admin/projects" class="px-5 py-2.5 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity">
            管理项目
          </router-link>
          <router-link v-if="user?.role === 'admin'" to="/admin/users" class="px-5 py-2.5 bg-[#1e293b] text-[#94a3b8] rounded-lg text-sm hover:text-white transition-colors">
            用户管理
          </router-link>
        </div>
      </div>
    </main>
  </div>
</template>
