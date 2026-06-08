<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchContactMessages, deleteContactMessage, type ContactMessageItem } from '@/api'

const messages = ref<ContactMessageItem[]>([])
const loading = ref(true)
const error = ref('')

async function loadMessages() {
  loading.value = true
  try {
    messages.value = await fetchContactMessages()
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function handleDelete(id: number) {
  if (!confirm('确定删除此留言吗？')) return
  try {
    await deleteContactMessage(id)
    await loadMessages()
  } catch (e: any) {
    error.value = e.message
  }
}

onMounted(loadMessages)
</script>

<template>
  <div class="min-h-screen bg-[#0a0e1a] flex">
    <!-- Sidebar -->
    <aside class="w-60 bg-[#0f172a] border-r border-[#1e293b] flex flex-col fixed h-full">
      <div class="p-5 border-b border-[#1e293b]">
        <div class="flex items-center gap-3">
          <div class="w-8 h-8 rounded-lg bg-gradient-to-br from-[#06b6d4] to-[#8b5cf6] flex items-center justify-center">
            <svg xmlns="http://www.w3.org/2000/svg" class="w-4 h-4 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2"><path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/></svg>
          </div>
          <span class="text-white font-bold text-sm">聚宁数据</span>
        </div>
      </div>
      <nav class="flex-1 p-3 space-y-1">
        <router-link to="/admin" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#94a3b8] hover:text-white hover:bg-[#1e293b]">概览</router-link>
        <router-link to="/admin/projects" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#94a3b8] hover:text-white hover:bg-[#1e293b]">项目管理</router-link>
        <router-link to="/admin/users" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#94a3b8] hover:text-white hover:bg-[#1e293b]">用户管理</router-link>
        <router-link to="/admin/messages" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm bg-[#06b6d4]/10 text-[#06b6d4]">咨询留言</router-link>
      </nav>
    </aside>

    <!-- Main -->
    <main class="flex-1 ml-60 p-8">
      <h1 class="text-xl font-bold text-white mb-6">咨询留言</h1>

      <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{{ error }}</div>
      <div v-if="loading" class="text-[#94a3b8]">加载中...</div>

      <div v-else class="space-y-4">
        <div v-for="msg in messages" :key="msg.id" class="bg-[#1e293b] rounded-xl p-5">
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-3">
              <div class="w-8 h-8 rounded-full bg-gradient-to-br from-[#06b6d4] to-[#8b5cf6] flex items-center justify-center text-white text-sm font-bold">
                {{ (msg.name || '?')[0] }}
              </div>
              <div>
                <p class="text-white text-sm font-medium">{{ msg.name || '匿名' }}</p>
                <p class="text-[#64748b] text-xs">{{ msg.created_at }}</p>
              </div>
            </div>
            <button @click="handleDelete(msg.id)" class="text-red-400 hover:underline text-xs">删除</button>
          </div>
          <div class="grid grid-cols-2 lg:grid-cols-4 gap-2 mb-3 text-xs">
            <span v-if="msg.email" class="text-[#94a3b8]">邮箱: {{ msg.email }}</span>
            <span v-if="msg.phone" class="text-[#94a3b8]">电话: {{ msg.phone }}</span>
            <span v-if="msg.company" class="text-[#94a3b8]">公司: {{ msg.company }}</span>
          </div>
          <p class="text-[#e2e8f0] text-sm leading-relaxed">{{ msg.message }}</p>
        </div>

        <div v-if="messages.length === 0" class="text-center py-8 text-[#64748b] text-sm">暂无留言</div>
      </div>
    </main>
  </div>
</template>
