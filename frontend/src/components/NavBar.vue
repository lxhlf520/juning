<template>
  <nav
    :class="[
      'fixed top-0 left-0 right-0 z-50 transition-all duration-300',
      scrolled ? 'nav-scrolled py-3' : 'py-5',
    ]"
  >
    <div class="max-w-7xl mx-auto px-6 flex items-center justify-between">
      <!-- Logo -->
      <router-link to="/" class="flex items-center gap-2.5 group">
        <img src="/logo-v2.png" alt="聚宁数据" class="w-8 h-8 rounded-lg object-cover" />
        <span class="text-white font-bold text-lg tracking-tight">聚宁数据</span>
      </router-link>

      <!-- Desktop Menu -->
      <div class="hidden md:flex items-center gap-8">
        <a
          v-for="item in menuItems"
          :key="item.href"
          :href="item.href"
          class="text-text-dark-muted hover:text-white transition-colors text-sm font-medium"
        >
          {{ item.label }}
        </a>
        <a
          href="#contact"
          class="btn-cta px-5 py-2 rounded-lg text-sm font-medium"
        >
          联系我们
        </a>
      </div>

      <!-- Mobile Toggle -->
      <button
        class="md:hidden text-white p-2"
        @click="mobileOpen = !mobileOpen"
        aria-label="Toggle menu"
      >
        <svg v-if="!mobileOpen" width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="3" y1="6" x2="21" y2="6" /><line x1="3" y1="12" x2="21" y2="12" /><line x1="3" y1="18" x2="21" y2="18" />
        </svg>
        <svg v-else width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2">
          <line x1="18" y1="6" x2="6" y2="18" /><line x1="6" y1="6" x2="18" y2="18" />
        </svg>
      </button>
    </div>

    <!-- Mobile Menu -->
    <transition name="fade">
      <div
        v-if="mobileOpen"
        class="md:hidden bg-dark-surface/95 backdrop-blur-md border-t border-white/5 px-6 py-4 space-y-3"
      >
        <a
          v-for="item in menuItems"
          :key="item.href"
          :href="item.href"
          class="block text-text-dark-muted hover:text-white transition-colors text-sm py-2"
          @click="mobileOpen = false"
        >
          {{ item.label }}
        </a>
      </div>
    </transition>
  </nav>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const scrolled = ref(false)
const mobileOpen = ref(false)

const menuItems = [
  { label: '业务服务', href: '#services' },
  { label: '案例展示', href: '#cases' },
  { label: '关于我们', href: '#about' },
  { label: '联系方式', href: '#contact' },
]

function onScroll() {
  scrolled.value = window.scrollY > 40
}

onMounted(() => window.addEventListener('scroll', onScroll))
onUnmounted(() => window.removeEventListener('scroll', onScroll))
</script>

<style scoped>
.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.2s ease;
}
.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}
</style>
