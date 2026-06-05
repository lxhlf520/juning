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
