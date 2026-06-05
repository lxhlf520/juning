<template>
  <section id="contact" class="py-24 bg-light-bg">
    <div class="max-w-7xl mx-auto px-6">
      <div class="text-center mb-16 reveal">
        <span class="text-accent-cyan font-semibold text-sm tracking-wider uppercase mb-3 block">Contact</span>
        <h2 class="text-3xl md:text-4xl font-bold text-text-light mb-4">联系我们</h2>
        <p class="text-text-light-muted max-w-2xl mx-auto text-lg">
          无论您有明确的需求还是初步的想法，我们都乐意与您交流
        </p>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-5 gap-10 reveal">
        <!-- Left: Info -->
        <div class="lg:col-span-2 space-y-8">
          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-lg bg-accent-cyan/10 flex items-center justify-center flex-shrink-0">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M4 4h16c1.1 0 2 .9 2 2v12c0 1.1-.9 2-2 2H4c-1.1 0-2-.9-2-2V6c0-1.1.9-2 2-2z" /><polyline points="22,6 12,13 2,6" />
              </svg>
            </div>
            <div>
              <div class="font-semibold text-text-light mb-1">电子邮箱</div>
              <div class="text-text-light-muted text-sm">{{ companyInfo.email || 'contact@shulantech.com' }}</div>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-lg bg-accent-cyan/10 flex items-center justify-center flex-shrink-0">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M22 16.92v3a2 2 0 0 1-2.18 2 19.79 19.79 0 0 1-8.63-3.07 19.5 19.5 0 0 1-6-6 19.79 19.79 0 0 1-3.07-8.67A2 2 0 0 1 4.11 2h3a2 2 0 0 1 2 1.72 12.84 12.84 0 0 0 .7 2.81 2 2 0 0 1-.45 2.11L8.09 9.91a16 16 0 0 0 6 6l1.27-1.27a2 2 0 0 1 2.11-.45 12.84 12.84 0 0 0 2.81.7A2 2 0 0 1 22 16.92z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold text-text-light mb-1">联系电话</div>
              <div class="text-text-light-muted text-sm">{{ companyInfo.phone || '400-888-9999' }}</div>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-lg bg-accent-cyan/10 flex items-center justify-center flex-shrink-0">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 10c0 7-9 13-9 13s-9-6-9-13a9 9 0 0 1 18 0z" /><circle cx="12" cy="10" r="3" />
              </svg>
            </div>
            <div>
              <div class="font-semibold text-text-light mb-1">公司地址</div>
              <div class="text-text-light-muted text-sm">{{ companyInfo.address || '北京市海淀区中关村软件园二期' }}</div>
            </div>
          </div>

          <div class="flex items-start gap-4">
            <div class="w-10 h-10 rounded-lg bg-accent-cyan/10 flex items-center justify-center flex-shrink-0">
              <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#06b6d4" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                <path d="M21 11.5a8.38 8.38 0 0 1-.9 3.8 8.5 8.5 0 0 1-7.6 4.7 8.38 8.38 0 0 1-3.8-.9L3 21l1.9-5.7a8.38 8.38 0 0 1-.9-3.8 8.5 8.5 0 0 1 4.7-7.6 8.38 8.38 0 0 1 3.8-.9h.5a8.48 8.48 0 0 1 8 8v.5z" />
              </svg>
            </div>
            <div>
              <div class="font-semibold text-text-light mb-1">微信公众号</div>
              <div class="text-text-light-muted text-sm">{{ companyInfo.wechat || 'shulantech' }}</div>
            </div>
          </div>
        </div>

        <!-- Right: Form -->
        <div class="lg:col-span-3">
          <form @submit.prevent="handleSubmit" class="bg-white rounded-xl p-8 border border-gray-100 shadow-sm">
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-5">
              <div>
                <label class="block text-sm font-medium text-text-light mb-1.5">姓名 *</label>
                <input
                  v-model="form.name"
                  type="text"
                  required
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan/30 transition-colors"
                  placeholder="您的姓名"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-text-light mb-1.5">邮箱 *</label>
                <input
                  v-model="form.email"
                  type="email"
                  required
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan/30 transition-colors"
                  placeholder="your@email.com"
                />
              </div>
            </div>
            <div class="grid grid-cols-1 sm:grid-cols-2 gap-5 mb-5">
              <div>
                <label class="block text-sm font-medium text-text-light mb-1.5">电话</label>
                <input
                  v-model="form.phone"
                  type="tel"
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan/30 transition-colors"
                  placeholder="手机号码"
                />
              </div>
              <div>
                <label class="block text-sm font-medium text-text-light mb-1.5">公司</label>
                <input
                  v-model="form.company"
                  type="text"
                  class="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan/30 transition-colors"
                  placeholder="公司名称"
                />
              </div>
            </div>
            <div class="mb-6">
              <label class="block text-sm font-medium text-text-light mb-1.5">需求描述 *</label>
              <textarea
                v-model="form.message"
                required
                rows="4"
                class="w-full px-4 py-2.5 rounded-lg border border-gray-200 text-sm focus:outline-none focus:border-accent-cyan focus:ring-1 focus:ring-accent-cyan/30 transition-colors resize-none"
                placeholder="请简要描述您的需求..."
              ></textarea>
            </div>
            <button
              type="submit"
              :disabled="submitting"
              class="btn-cta w-full py-3 rounded-lg font-semibold text-sm disabled:opacity-50 disabled:cursor-not-allowed"
            >
              {{ submitting ? '提交中...' : '提交咨询' }}
            </button>
            <p v-if="submitResult === 'success'" class="mt-3 text-sm text-green-600 text-center">
              提交成功，我们会尽快与您联系！
            </p>
            <p v-else-if="submitResult === 'error'" class="mt-3 text-sm text-red-500 text-center">
              提交失败，请稍后重试或直接发送邮件。
            </p>
          </form>
        </div>
      </div>
    </div>
  </section>
</template>

<script setup lang="ts">
import { ref, reactive, onMounted } from 'vue'
import { submitContact, fetchCompanyInfo, type CompanyInfoItem } from '@/api'

const form = reactive({
  name: '',
  email: '',
  phone: '',
  company: '',
  message: '',
})

const submitting = ref(false)
const submitResult = ref<string | null>(null)

const companyInfo = reactive<Record<string, string>>({
  email: '',
  phone: '',
  address: '',
  wechat: '',
})

onMounted(async () => {
  try {
    const info: CompanyInfoItem[] = await fetchCompanyInfo()
    for (const item of info) {
      if (item.key.startsWith('company_')) {
        const key = item.key.replace('company_', '')
        companyInfo[key] = item.value
      }
    }
  } catch {
    // Use defaults
  }
})

async function handleSubmit() {
  submitting.value = true
  submitResult.value = null
  try {
    await submitContact({ ...form })
    submitResult.value = 'success'
    form.name = ''
    form.email = ''
    form.phone = ''
    form.company = ''
    form.message = ''
  } catch {
    submitResult.value = 'error'
  } finally {
    submitting.value = false
  }
}
</script>
