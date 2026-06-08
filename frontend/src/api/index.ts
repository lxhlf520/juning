const API_BASE = ''

export interface ServiceItem {
  id: number
  title: string
  description: string
  icon: string
  sort_order: number
}

export interface CaseItem {
  id: number
  title: string
  description: string
  image: string
  tags: string
  sort_order: number
}

export interface CompanyInfoItem {
  key: string
  value: string
}

export interface ContactPayload {
  name: string
  email: string
  phone?: string
  company?: string
  message: string
}

// ---------- Auth ----------

export interface LoginPayload {
  username: string
  password: string
}

export interface TokenData {
  access_token: string
  token_type: string
  username: string
  display_name: string
  role: string
}

export interface UserInfo {
  id: number
  username: string
  display_name: string
  role: string
  is_active: boolean
  created_at: string
}

// ---------- Project ----------

export interface ProjectItem {
  id: number
  start_date: string
  name: string
  description: string
  priority: string
  client_type: string
  url: string
  quote: number
  profit: number
  payment_method: string
  duration: string
  progress: string
  is_outsourced: string
  outsourced_to: string
  delivery_method: string
  is_settled: string
  client: string
  remark: string
  created_by: number
  created_at: string
  updated_at: string
}

export interface DashboardStats {
  total: number
  in_progress: number
  completed: number
  pending: number
  unsettled: number
  total_quote: number
}

// ---------- Helpers ----------

function getAuthHeaders(): Record<string, string> {
  const token = localStorage.getItem('admin_token')
  return token ? { 'Authorization': `Bearer ${token}`, 'Content-Type': 'application/json' } : { 'Content-Type': 'application/json' }
}

async function authFetch(url: string, options?: RequestInit) {
  const res = await fetch(url, {
    ...options,
    headers: { ...getAuthHeaders(), ...options?.headers },
  })
  if (res.status === 401) {
    localStorage.removeItem('admin_token')
    window.location.href = '/admin/login'
    throw new Error('登录已过期')
  }
  return res
}

// ---------- Portal API ----------

export async function fetchServices(): Promise<ServiceItem[]> {
  const res = await fetch(`${API_BASE}/api/services`)
  if (!res.ok) throw new Error('Failed to fetch services')
  return res.json()
}

export async function fetchCases(): Promise<CaseItem[]> {
  const res = await fetch(`${API_BASE}/api/cases`)
  if (!res.ok) throw new Error('Failed to fetch cases')
  return res.json()
}

export async function fetchCompanyInfo(): Promise<CompanyInfoItem[]> {
  const res = await fetch(`${API_BASE}/api/company`)
  if (!res.ok) throw new Error('Failed to fetch company info')
  return res.json()
}

export async function submitContact(data: ContactPayload): Promise<{ success: boolean; id: number }> {
  const res = await fetch(`${API_BASE}/api/contact`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) throw new Error('Failed to submit contact')
  return res.json()
}

// ---------- Auth API ----------

export async function loginApi(data: LoginPayload): Promise<TokenData> {
  const res = await fetch(`${API_BASE}/api/auth/login`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || '登录失败')
  }
  return res.json()
}

export async function getMe(): Promise<UserInfo> {
  const res = await authFetch(`${API_BASE}/api/auth/me`)
  if (!res.ok) throw new Error('未登录')
  return res.json()
}

// ---------- User Management API ----------

export async function fetchUsers(): Promise<UserInfo[]> {
  const res = await authFetch(`${API_BASE}/api/users`)
  if (!res.ok) throw new Error('获取用户列表失败')
  return res.json()
}

export async function createUser(data: { username: string; password: string; display_name?: string; role?: string }): Promise<UserInfo> {
  const res = await authFetch(`${API_BASE}/api/users`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || '创建用户失败')
  }
  return res.json()
}

export async function updateUser(id: number, data: Partial<UserInfo & { password?: string }>): Promise<UserInfo> {
  const res = await authFetch(`${API_BASE}/api/users/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || '更新用户失败')
  }
  return res.json()
}

export async function deleteUser(id: number): Promise<void> {
  const res = await authFetch(`${API_BASE}/api/users/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('删除用户失败')
}

// ---------- Project Management API ----------

export async function fetchProjects(params?: { progress?: string; client?: string; search?: string }): Promise<ProjectItem[]> {
  const searchParams = new URLSearchParams()
  if (params?.progress) searchParams.set('progress', params.progress)
  if (params?.client) searchParams.set('client', params.client)
  if (params?.search) searchParams.set('search', params.search)
  const qs = searchParams.toString() ? `?${searchParams.toString()}` : ''
  const res = await authFetch(`${API_BASE}/api/projects${qs}`)
  if (!res.ok) throw new Error('获取项目列表失败')
  return res.json()
}

export async function createProject(data: Partial<ProjectItem>): Promise<ProjectItem> {
  const res = await authFetch(`${API_BASE}/api/projects`, {
    method: 'POST',
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || '创建项目失败')
  }
  return res.json()
}

export async function updateProject(id: number, data: Partial<ProjectItem>): Promise<ProjectItem> {
  const res = await authFetch(`${API_BASE}/api/projects/${id}`, {
    method: 'PUT',
    body: JSON.stringify(data),
  })
  if (!res.ok) {
    const err = await res.json().catch(() => ({}))
    throw new Error(err.detail || '更新项目失败')
  }
  return res.json()
}

export async function deleteProject(id: number): Promise<void> {
  const res = await authFetch(`${API_BASE}/api/projects/${id}`, { method: 'DELETE' })
  if (!res.ok) throw new Error('删除项目失败')
}

// ---------- Dashboard API ----------

export async function fetchDashboardStats(): Promise<DashboardStats> {
  const res = await authFetch(`${API_BASE}/api/dashboard/stats`)
  if (!res.ok) throw new Error('获取统计失败')
  return res.json()
}
