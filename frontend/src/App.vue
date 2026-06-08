<template>
  <router-view />
</template>

<script setup lang="ts">
import { useRoute } from 'vue-router'
import { useScrollReveal } from '@/composables/useScrollReveal'

const route = useRoute()

// 只在首页启用滚动动画
if (route.path === '/') {
  useScrollReveal()
}
</script>
