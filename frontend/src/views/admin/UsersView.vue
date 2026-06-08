<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchUsers, createUser, updateUser, deleteUser, type UserInfo } from '@/api'

const users = ref<UserInfo[]>([])
const loading = ref(true)
const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingUser = ref<UserInfo | null>(null)
const error = ref('')

const newUser = ref({ username: '', password: '', display_name: '', role: 'staff' })
const editForm = ref({ display_name: '', role: '', is_active: true, password: '' })

async function loadUsers() {
  try {
    users.value = await fetchUsers()
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

async function handleCreate() {
  error.value = ''
  try {
    await createUser(newUser.value)
    showCreateModal.value = false
    newUser.value = { username: '', password: '', display_name: '', role: 'staff' }
    await loadUsers()
  } catch (e: any) {
    error.value = e.message
  }
}

function openEdit(user: UserInfo) {
  editingUser.value = user
  editForm.value = { display_name: user.display_name, role: user.role, is_active: user.is_active, password: '' }
  showEditModal.value = true
}

async function handleEdit() {
  if (!editingUser.value) return
  error.value = ''
  try {
    const data: any = { display_name: editForm.value.display_name, role: editForm.value.role, is_active: editForm.value.is_active }
    if (editForm.value.password) data.password = editForm.value.password
    await updateUser(editingUser.value.id, data)
    showEditModal.value = false
    await loadUsers()
  } catch (e: any) {
    error.value = e.message
  }
}

async function handleDelete(user: UserInfo) {
  if (!confirm(`确定删除用户 "${user.username}" 吗？`)) return
  try {
    await deleteUser(user.id)
    await loadUsers()
  } catch (e: any) {
    error.value = e.message
  }
}

onMounted(loadUsers)
</script>

<template>
  <div class="min-h-screen bg-[#0a0e1a] flex">
    <!-- Sidebar (same as Dashboard) -->
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
        <router-link to="/admin/users" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm bg-[#06b6d4]/10 text-[#06b6d4]">用户管理</router-link>
        <router-link to="/admin/messages" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#94a3b8] hover:text-white hover:bg-[#1e293b]">咨询留言</router-link>
      </nav>
    </aside>

    <!-- Main -->
    <main class="flex-1 ml-60 p-8">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-bold text-white">用户管理</h1>
        <button @click="showCreateModal = true" class="px-4 py-2 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white text-sm font-semibold rounded-lg hover:opacity-90 transition-opacity">
          新增用户
        </button>
      </div>

      <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{{ error }}</div>

      <div v-if="loading" class="text-[#94a3b8]">加载中...</div>

      <div v-else class="bg-[#1e293b] rounded-xl overflow-hidden">
        <table class="w-full">
          <thead>
            <tr class="border-b border-[#334155]">
              <th class="text-left px-5 py-3 text-[#94a3b8] text-sm font-medium">用户名</th>
              <th class="text-left px-5 py-3 text-[#94a3b8] text-sm font-medium">显示名</th>
              <th class="text-left px-5 py-3 text-[#94a3b8] text-sm font-medium">角色</th>
              <th class="text-left px-5 py-3 text-[#94a3b8] text-sm font-medium">状态</th>
              <th class="text-left px-5 py-3 text-[#94a3b8] text-sm font-medium">创建时间</th>
              <th class="text-right px-5 py-3 text-[#94a3b8] text-sm font-medium">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="u in users" :key="u.id" class="border-b border-[#1e293b] hover:bg-[#0f172a]/50">
              <td class="px-5 py-3 text-white text-sm">{{ u.username }}</td>
              <td class="px-5 py-3 text-[#e2e8f0] text-sm">{{ u.display_name || '-' }}</td>
              <td class="px-5 py-3 text-sm">
                <span :class="u.role === 'admin' ? 'text-[#06b6d4] bg-[#06b6d4]/10' : 'text-[#8b5cf6] bg-[#8b5cf6]/10'" class="px-2 py-0.5 rounded text-xs">
                  {{ u.role === 'admin' ? '管理员' : '普通用户' }}
                </span>
              </td>
              <td class="px-5 py-3 text-sm">
                <span :class="u.is_active ? 'text-green-400' : 'text-red-400'">{{ u.is_active ? '正常' : '禁用' }}</span>
              </td>
              <td class="px-5 py-3 text-[#94a3b8] text-sm">{{ u.created_at }}</td>
              <td class="px-5 py-3 text-right space-x-2">
                <button @click="openEdit(u)" class="text-[#06b6d4] hover:underline text-sm">编辑</button>
                <button @click="handleDelete(u)" class="text-red-400 hover:underline text-sm">删除</button>
              </td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create Modal -->
      <div v-if="showCreateModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
        <div class="bg-[#1e293b] rounded-xl p-6 w-full max-w-md">
          <h2 class="text-lg font-bold text-white mb-4">新增用户</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">用户名</label>
              <input v-model="newUser.username" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">密码</label>
              <input v-model="newUser.password" type="password" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">显示名</label>
              <input v-model="newUser.display_name" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">角色</label>
              <select v-model="newUser.role" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option value="staff">普通用户</option>
                <option value="admin">管理员</option>
              </select>
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showCreateModal = false" class="flex-1 py-2 bg-[#0f172a] text-[#94a3b8] rounded-lg text-sm hover:text-white transition-colors">取消</button>
            <button @click="handleCreate" class="flex-1 py-2 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity">创建</button>
          </div>
        </div>
      </div>

      <!-- Edit Modal -->
      <div v-if="showEditModal" class="fixed inset-0 bg-black/60 flex items-center justify-center z-50">
        <div class="bg-[#1e293b] rounded-xl p-6 w-full max-w-md">
          <h2 class="text-lg font-bold text-white mb-4">编辑用户 - {{ editingUser?.username }}</h2>
          <div class="space-y-4">
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">显示名</label>
              <input v-model="editForm.display_name" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">角色</label>
              <select v-model="editForm.role" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option value="staff">普通用户</option>
                <option value="admin">管理员</option>
              </select>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">状态</label>
              <select v-model="editForm.is_active" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option :value="true">正常</option>
                <option :value="false">禁用</option>
              </select>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-sm mb-1">新密码（留空则不修改）</label>
              <input v-model="editForm.password" type="password" placeholder="留空则不修改" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showEditModal = false" class="flex-1 py-2 bg-[#0f172a] text-[#94a3b8] rounded-lg text-sm hover:text-white transition-colors">取消</button>
            <button @click="handleEdit" class="flex-1 py-2 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity">保存</button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
