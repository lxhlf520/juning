<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { fetchProjects, createProject, updateProject, deleteProject, type ProjectItem } from '@/api'

const projects = ref<ProjectItem[]>([])
const loading = ref(true)
const error = ref('')
const searchQuery = ref('')
const filterProgress = ref('')

const showCreateModal = ref(false)
const showEditModal = ref(false)
const editingProject = ref<ProjectItem | null>(null)

const emptyProject = {
  start_date: '', name: '', description: '', priority: '中', client_type: '',
  url: '', quote: 0, profit: 0, payment_method: '', duration: '',
  progress: '待开始', is_outsourced: '否', outsourced_to: '', delivery_method: '',
  is_settled: '未结算', client: '', remark: '',
}

const form = ref({ ...emptyProject })

async function loadProjects() {
  loading.value = true
  try {
    projects.value = await fetchProjects({
      progress: filterProgress.value || undefined,
      search: searchQuery.value || undefined,
    })
  } catch (e: any) {
    error.value = e.message
  } finally {
    loading.value = false
  }
}

function openCreate() {
  form.value = { ...emptyProject }
  showCreateModal.value = true
}

function openEdit(p: ProjectItem) {
  editingProject.value = p
  form.value = {
    start_date: p.start_date, name: p.name, description: p.description,
    priority: p.priority, client_type: p.client_type, url: p.url,
    quote: p.quote, profit: p.profit, payment_method: p.payment_method,
    duration: p.duration, progress: p.progress, is_outsourced: p.is_outsourced,
    outsourced_to: p.outsourced_to, delivery_method: p.delivery_method,
    is_settled: p.is_settled, client: p.client, remark: p.remark,
  }
  showEditModal.value = true
}

async function handleCreate() {
  error.value = ''
  try {
    await createProject(form.value)
    showCreateModal.value = false
    await loadProjects()
  } catch (e: any) {
    error.value = e.message
  }
}

async function handleEdit() {
  if (!editingProject.value) return
  error.value = ''
  try {
    await updateProject(editingProject.value.id, form.value)
    showEditModal.value = false
    await loadProjects()
  } catch (e: any) {
    error.value = e.message
  }
}

async function handleDelete(p: ProjectItem) {
  if (!confirm(`确定删除项目 "${p.name}" 吗？`)) return
  try {
    await deleteProject(p.id)
    await loadProjects()
  } catch (e: any) {
    error.value = e.message
  }
}

function priorityColor(p: string) {
  return p === '高' ? 'text-red-400 bg-red-400/10' : p === '低' ? 'text-[#64748b] bg-[#64748b]/10' : 'text-amber-400 bg-amber-400/10'
}

function progressColor(p: string) {
  if (p === '已完成') return 'text-green-400 bg-green-400/10'
  if (p === '正在进行') return 'text-[#06b6d4] bg-[#06b6d4]/10'
  return 'text-[#8b5cf6] bg-[#8b5cf6]/10'
}

onMounted(loadProjects)
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
        <router-link to="/admin/projects" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm bg-[#06b6d4]/10 text-[#06b6d4]">项目管理</router-link>
        <router-link to="/admin/users" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#94a3b8] hover:text-white hover:bg-[#1e293b]">用户管理</router-link>
        <router-link to="/admin/messages" class="flex items-center gap-3 px-3 py-2.5 rounded-lg text-sm text-[#94a3b8] hover:text-white hover:bg-[#1e293b]">咨询留言</router-link>
      </nav>
    </aside>

    <!-- Main -->
    <main class="flex-1 ml-60 p-8">
      <div class="flex items-center justify-between mb-6">
        <h1 class="text-xl font-bold text-white">项目管理</h1>
        <button @click="openCreate" class="px-4 py-2 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white text-sm font-semibold rounded-lg hover:opacity-90 transition-opacity">
          新增项目
        </button>
      </div>

      <!-- Filters -->
      <div class="flex gap-3 mb-4">
        <input v-model="searchQuery" @input="loadProjects" placeholder="搜索项目名称..." class="px-3 py-2 bg-[#1e293b] border border-[#334155] rounded-lg text-white text-sm w-64 focus:outline-none focus:border-[#06b6d4]" />
        <select v-model="filterProgress" @change="loadProjects" class="px-3 py-2 bg-[#1e293b] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
          <option value="">全部进度</option>
          <option value="待开始">待开始</option>
          <option value="正在进行">正在进行</option>
          <option value="已完成">已完成</option>
        </select>
      </div>

      <div v-if="error" class="mb-4 p-3 rounded-lg bg-red-500/10 border border-red-500/20 text-red-400 text-sm">{{ error }}</div>
      <div v-if="loading" class="text-[#94a3b8]">加载中...</div>

      <!-- Project Table -->
      <div v-else class="bg-[#1e293b] rounded-xl overflow-x-auto">
        <table class="w-full min-w-[1000px]">
          <thead>
            <tr class="border-b border-[#334155]">
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">开始时间</th>
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">项目名称</th>
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">优先级</th>
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">进度</th>
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">报价</th>
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">甲方</th>
              <th class="text-left px-4 py-3 text-[#94a3b8] text-xs font-medium">结算</th>
              <th class="text-right px-4 py-3 text-[#94a3b8] text-xs font-medium">操作</th>
            </tr>
          </thead>
          <tbody>
            <tr v-for="p in projects" :key="p.id" class="border-b border-[#1e293b] hover:bg-[#0f172a]/50 cursor-pointer" @click="openEdit(p)">
              <td class="px-4 py-3 text-[#94a3b8] text-xs">{{ p.start_date || '-' }}</td>
              <td class="px-4 py-3 text-white text-sm font-medium">{{ p.name }}</td>
              <td class="px-4 py-3 text-xs"><span :class="priorityColor(p.priority)" class="px-1.5 py-0.5 rounded">{{ p.priority }}</span></td>
              <td class="px-4 py-3 text-xs"><span :class="progressColor(p.progress)" class="px-1.5 py-0.5 rounded">{{ p.progress }}</span></td>
              <td class="px-4 py-3 text-[#e2e8f0] text-sm">{{ p.quote ? `¥${p.quote.toLocaleString()}` : '-' }}</td>
              <td class="px-4 py-3 text-[#94a3b8] text-sm">{{ p.client || '-' }}</td>
              <td class="px-4 py-3 text-xs"><span :class="p.is_settled === '已结算' ? 'text-green-400' : 'text-amber-400'">{{ p.is_settled }}</span></td>
              <td class="px-4 py-3 text-right" @click.stop>
                <button @click="openEdit(p)" class="text-[#06b6d4] hover:underline text-xs">编辑</button>
                <button @click="handleDelete(p)" class="text-red-400 hover:underline text-xs ml-2">删除</button>
              </td>
            </tr>
            <tr v-if="projects.length === 0">
              <td colspan="8" class="text-center py-8 text-[#64748b] text-sm">暂无项目数据</td>
            </tr>
          </tbody>
        </table>
      </div>

      <!-- Create/Edit Modal -->
      <div v-if="showCreateModal || showEditModal" class="fixed inset-0 bg-black/60 flex items-start justify-center z-50 overflow-y-auto py-10">
        <div class="bg-[#1e293b] rounded-xl p-6 w-full max-w-2xl">
          <h2 class="text-lg font-bold text-white mb-4">{{ showCreateModal ? '新增项目' : '编辑项目' }}</h2>
          <div class="grid grid-cols-2 gap-4">
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">项目名称 *</label>
              <input v-model="form.name" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">开始时间</label>
              <input v-model="form.start_date" type="date" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div class="col-span-2">
              <label class="block text-[#94a3b8] text-xs mb-1">需求描述</label>
              <textarea v-model="form.description" rows="2" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]"></textarea>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">优先级</label>
              <select v-model="form.priority" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option value="高">高</option>
                <option value="中">中</option>
                <option value="低">低</option>
              </select>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">客户端类型</label>
              <input v-model="form.client_type" placeholder="web/app/小程序" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">报价</label>
              <input v-model.number="form.quote" type="number" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">利润</label>
              <input v-model.number="form.profit" type="number" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">进度</label>
              <select v-model="form.progress" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option value="待开始">待开始</option>
                <option value="正在进行">正在进行</option>
                <option value="已完成">已完成</option>
              </select>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">甲方</label>
              <input v-model="form.client" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">是否外包</label>
              <select v-model="form.is_outsourced" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option value="否">否</option>
                <option value="是">是</option>
              </select>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">外包人</label>
              <input v-model="form.outsourced_to" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">交付方式</label>
              <input v-model="form.delivery_method" placeholder="数据交付/代码交付/平台交付/工具交付" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">是否结算</label>
              <select v-model="form.is_settled" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]">
                <option value="未结算">未结算</option>
                <option value="已结算">已结算</option>
              </select>
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">支付方式</label>
              <input v-model="form.payment_method" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">工期</label>
              <input v-model="form.duration" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div>
              <label class="block text-[#94a3b8] text-xs mb-1">网址</label>
              <input v-model="form.url" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]" />
            </div>
            <div class="col-span-2">
              <label class="block text-[#94a3b8] text-xs mb-1">备注</label>
              <textarea v-model="form.remark" rows="2" class="w-full px-3 py-2 bg-[#0f172a] border border-[#334155] rounded-lg text-white text-sm focus:outline-none focus:border-[#06b6d4]"></textarea>
            </div>
          </div>
          <div class="flex gap-3 mt-6">
            <button @click="showCreateModal = false; showEditModal = false" class="flex-1 py-2 bg-[#0f172a] text-[#94a3b8] rounded-lg text-sm hover:text-white transition-colors">取消</button>
            <button @click="showCreateModal ? handleCreate() : handleEdit()" class="flex-1 py-2 bg-gradient-to-r from-[#06b6d4] to-[#8b5cf6] text-white rounded-lg text-sm font-semibold hover:opacity-90 transition-opacity">
              {{ showCreateModal ? '创建' : '保存' }}
            </button>
          </div>
        </div>
      </div>
    </main>
  </div>
</template>
