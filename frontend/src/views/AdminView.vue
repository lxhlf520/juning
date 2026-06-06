<template>
  <div class="min-h-screen" style="background-color: #0a0e1a; color: #e2e8f0;">
    <!-- Header -->
    <div class="border-b" style="border-color: #1e293b; background-color: #0f172a;">
      <div class="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
        <div class="flex items-center gap-3">
          <img src="/logo-v2.png" alt="聚宁数据" class="h-8 w-8 rounded object-cover" />
          <h1 class="text-lg font-bold" style="color: #e2e8f0;">咨询留言管理</h1>
        </div>
        <a href="/" class="text-sm hover:underline" style="color: #94a3b8;">← 返回首页</a>
      </div>
    </div>

    <!-- Content -->
    <div class="max-w-6xl mx-auto px-6 py-8">
      <!-- Stats -->
      <div class="grid grid-cols-1 sm:grid-cols-3 gap-4 mb-8">
        <div class="rounded-lg p-4" style="background-color: #1e293b;">
          <div class="text-sm" style="color: #94a3b8;">总留言数</div>
          <div class="text-2xl font-bold mt-1" style="color: #06b6d4;">{{ messages.length }}</div>
        </div>
        <div class="rounded-lg p-4" style="background-color: #1e293b;">
          <div class="text-sm" style="color: #94a3b8;">今日新增</div>
          <div class="text-2xl font-bold mt-1" style="color: #8b5cf6;">{{ todayCount }}</div>
        </div>
        <div class="rounded-lg p-4" style="background-color: #1e293b;">
          <div class="text-sm" style="color: #94a3b8;">本周新增</div>
          <div class="text-2xl font-bold mt-1" style="color: #06b6d4;">{{ weekCount }}</div>
        </div>
      </div>

      <!-- Loading -->
      <div v-if="loading" class="text-center py-20" style="color: #94a3b8;">
        加载中...
      </div>

      <!-- Empty -->
      <div v-else-if="messages.length === 0" class="text-center py-20" style="color: #94a3b8;">
        <div class="text-4xl mb-4">📭</div>
        <div>暂无咨询留言</div>
      </div>

      <!-- Message List -->
      <div v-else class="space-y-4">
        <div
          v-for="msg in messages"
          :key="msg.id"
          class="rounded-lg p-5 border transition-colors"
          style="background-color: #1e293b; border-color: #334155;"
        >
          <div class="flex items-start justify-between mb-3">
            <div class="flex items-center gap-3">
              <div
                class="w-10 h-10 rounded-full flex items-center justify-center text-sm font-bold"
                style="background: linear-gradient(135deg, #06b6d4, #8b5cf6); color: white;"
              >
                {{ msg.name.charAt(0) }}
              </div>
              <div>
                <div class="font-semibold" style="color: #e2e8f0;">{{ msg.name }}</div>
                <div class="text-xs" style="color: #94a3b8;">{{ msg.created_at }}</div>
              </div>
            </div>
            <button
              @click="deleteMessage(msg.id)"
              class="text-xs px-3 py-1 rounded border transition-colors hover:opacity-80"
              style="color: #f87171; border-color: #7f1d1d; background-color: rgba(248,113,113,0.1);"
            >
              删除
            </button>
          </div>

          <!-- Info tags -->
          <div class="flex flex-wrap gap-2 mb-3">
            <span v-if="msg.email" class="text-xs px-2 py-1 rounded" style="background-color: #0f172a; color: #06b6d4;">
              📧 {{ msg.email }}
            </span>
            <span v-if="msg.phone" class="text-xs px-2 py-1 rounded" style="background-color: #0f172a; color: #06b6d4;">
              📱 {{ msg.phone }}
            </span>
            <span v-if="msg.company" class="text-xs px-2 py-1 rounded" style="background-color: #0f172a; color: #8b5cf6;">
              🏢 {{ msg.company }}
            </span>
          </div>

          <!-- Message -->
          <div class="text-sm leading-relaxed" style="color: #cbd5e1;">
            {{ msg.message }}
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted } from 'vue'

interface ContactMsg {
  id: number
  name: string
  email: string
  phone: string
  company: string
  message: string
  created_at: string
}

const messages = ref<ContactMsg[]>([])
const loading = ref(true)

const todayCount = computed(() => {
  const today = new Date().toISOString().slice(0, 10)
  return messages.value.filter(m => m.created_at.startsWith(today)).length
})

const weekCount = computed(() => {
  const weekAgo = new Date(Date.now() - 7 * 86400000)
  return messages.value.filter(m => new Date(m.created_at) >= weekAgo).length
})

async function fetchMessages() {
  loading.value = true
  try {
    const res = await fetch('/api/contact-messages')
    if (res.ok) {
      messages.value = await res.json()
    }
  } catch (e) {
    console.error('获取留言失败', e)
  } finally {
    loading.value = false
  }
}

async function deleteMessage(id: number) {
  if (!confirm('确定删除这条留言吗？')) return
  try {
    const res = await fetch(`/api/contact-messages/${id}`, { method: 'DELETE' })
    if (res.ok) {
      messages.value = messages.value.filter(m => m.id !== id)
    }
  } catch (e) {
    console.error('删除失败', e)
  }
}

onMounted(fetchMessages)
</script>
