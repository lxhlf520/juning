<script setup lang="ts">
import { ref } from 'vue'
import { useRouter } from 'vue-router'
import { loginApi } from '@/api'

const router = useRouter()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

async function handleLogin() {
  error.value = ''
  loading.value = true
  try {
    const data = await loginApi({ username: username.value, password: password.value })
    localStorage.setItem('admin_token', data.access_token)
    localStorage.setItem('admin_user', JSON.stringify(data))
    router.push('/admin')
  } catch (e: any) {
    error.value = e.message || '登录失败'
  } finally {
    loading.value = false
  }
}
</script>

<template>
  <div class="min-h-screen flex items-center justify-center bg-[#0a0e1a] px-4">
    <div class="w-full max-w-md">
      <!-- Logo -->
      <div class="text-center mb-10">
        <div class="inline-flex items-center justify-center w-16 h-16 rounded-xl bg-gradient-to-br from-[#06b6d4] to-[#8b5cf6] mb-4">
          <svg xmlns="http://www.w3.org/2000/svg" class="w-8 h-8 text-white" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
            <path d="M12 2L2 7l10 5 10-5-10-5zM2 17l10 5 10-5M2 12l10 5 10-5"/>
          </svg>
        </div>
        <h1 class="text-2xl font-bold text-white">聚宁数据</h1>
        <p class="text-[#94a3b8] text-sm mt-1">管理后台</p>
      </div>

      <!-- Login Form -->
      <div class="bg-[#1e293b] rounded-xl p-8 shadow-2xl">
        <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">
          {{ error }}
        </div>

        <div class="space-y-5">
          <div>
            <label class="block text-[#94a3b8] text-sm mb-2">用户名</label>
            <input
              v-model="username"
              type="text"
              placeholder="请输入用户名"
              class="w-full px-4 py-3 bg-[#0f172a] border border-[#334155] rounded-lg text-white placeholder-[#475569] focus:outline-none focus:border-[#06b6d4] transition-colors"
              @keyup.enter="handleLogin"
            />
          </div>
          <div>
            <label class="block text-[#94a3b8] text-sm mb-2">密码</label>
            <input
              v-model="password"
              type="password"
              placeholder="请输入密码"
              class="w-full px-4 py-3 bg-[#0f172a] border border-[#334155] rounded-lg text-white placeholder-[#475569] focus:outline-none focus:border-[#06b6d4] transition-colors"
              @keyup.enter="handleLogin"
            />
          </div>
          <button
            @click="handleLogin"
            :disabled="loading || !username || !password"
            class="w-full py-3 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white font-semibold rounded-lg hover:opacity-90 transition-opacity disabled:opacity-50 disabled:cursor-not-allowed"
          >
            {{ loading ? '登录中...' : '登 录' }}
          </button>
        </div>
      </div>

      <p class="text-center text-[#475569] text-xs mt-8">
        <a href="/" class="hover:text-[#06b6d4] transition-colors">返回官网</a>
      </p>
    </div>
  </div>
</template>
