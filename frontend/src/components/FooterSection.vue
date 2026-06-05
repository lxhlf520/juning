<template>
  <footer class="bg-dark-bg py-12">
    <div class="max-w-7xl mx-auto px-6">
      <div class="flex flex-col md:flex-row items-center justify-between gap-6">
        <!-- Logo & Copyright -->
        <div class="flex items-center gap-3">
          <img src="/logo-v2.png" alt="聚宁数据" class="w-7 h-7 rounded-md object-cover" />
          <span class="text-text-dark-muted text-sm">&copy; {{ year }} 聚宁数据. All rights reserved.</span>
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
