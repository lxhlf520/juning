<template>
  <footer class="bg-dark-bg py-12">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6">
        <!-- Logo & Copyright -->
        <div class="flex items-center gap-3">
          <div class="w-7 h-7 rounded-lg bg-gradient-to-br from-accent-cyan to-accent-violet flex items-center justify-center">
            <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
              <path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z" />
            </svg>
          </div>
          <span class="text-text-dark-muted text-sm">&copy; {{ year }} 数澜科技. All rights reserved.</span>
        </div>

        <!-- Quick Links -->
        <div class="flex items-center gap-6">
          <a href="#services" class="text-text-dark-muted hover:text-white text-sm transition-colors">业务服务</a>
          <a href="#cases" class="text-text-dark-muted hover:text-white text-sm transition-colors">案例展示</a>
          <a href="#contact" class="text-text-dark-muted hover:text-white text-sm transition-colors">联系我们</a>
        </div>
      </div>
    </div>
  </footer>
</template>

<script setup lang="ts">
const year = new Date().getFullYear()
</script>
