<template>
  <section class="relative min-h-screen flex items-center justify-center overflow-hidden bg-dark-bg">
    <!-- Particle Canvas -->
    <canvas ref="canvasRef" class="particle-canvas"></canvas>

    <!-- Gradient Overlay -->
    <div class="absolute inset-0 bg-gradient-to-b from-dark-bg/50 via-transparent to-dark-bg pointer-events-none"></div>

    <!-- Content -->
    <div class="relative z-10 max-w-4xl mx-auto px-6 text-center">
      <h1 class="text-4xl md:text-6xl font-bold text-white leading-tight tracking-tight mb-6">
        以<span class="gradient-text">数据</span>驱动决策<br />用<span class="gradient-text">技术</span>赋能增长
      </h1>
      <p class="text-lg md:text-xl text-text-dark-muted max-w-2xl mx-auto mb-10 leading-relaxed">
        专注于数据分析、智能采集与全栈开发，为企业提供从数据到增长的一站式技术解决方案。
      </p>
      <div class="flex flex-col sm:flex-row gap-4 justify-center">
        <a
          href="#services"
          class="btn-cta px-8 py-3.5 rounded-lg text-base font-semibold inline-flex items-center justify-center gap-2"
        >
          了解我们的服务
          <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5" stroke-linecap="round" stroke-linejoin="round">
            <line x1="5" y1="12" x2="19" y2="12" /><polyline points="12 5 19 12 12 19" />
          </svg>
        </a>
        <a
          href="#contact"
          class="px-8 py-3.5 rounded-lg text-base font-semibold border border-white/15 text-white hover:bg-white/5 transition-colors inline-flex items-center justify-center"
        >
          预约咨询
        </a>
      </div>
    </div>

    <!-- Bottom Fade -->
    <div class="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-light-bg to-transparent pointer-events-none"></div>
  </section>
</template>

<script setup lang="ts">
import { ref, onMounted, onUnmounted } from 'vue'

const canvasRef = ref<HTMLCanvasElement | null>(null)
let animationId: number | null = null
let particles: Array<{
  x: number
  y: number
  vx: number
  vy: number
  radius: number
  opacity: number
}> = []

function initParticles(canvas: HTMLCanvasElement) {
  const count = Math.min(80, Math.floor((canvas.width * canvas.height) / 15000))
  particles = []
  for (let i = 0; i < count; i++) {
    particles.push({
      x: Math.random() * canvas.width,
      y: Math.random() * canvas.height,
      vx: (Math.random() - 0.5) * 0.3,
      vy: (Math.random() - 0.5) * 0.3,
      radius: Math.random() * 1.5 + 0.5,
      opacity: Math.random() * 0.4 + 0.1,
    })
  }
}

function draw(canvas: HTMLCanvasElement) {
  const ctx = canvas.getContext('2d')
  if (!ctx) return

  ctx.clearRect(0, 0, canvas.width, canvas.height)

  // Draw connections
  for (let i = 0; i < particles.length; i++) {
    for (let j = i + 1; j < particles.length; j++) {
      const dx = particles[i].x - particles[j].x
      const dy = particles[i].y - particles[j].y
      const dist = Math.sqrt(dx * dx + dy * dy)
      if (dist < 150) {
        const alpha = (1 - dist / 150) * 0.08
        ctx.strokeStyle = `rgba(6, 182, 212, ${alpha})`
        ctx.lineWidth = 0.5
        ctx.beginPath()
        ctx.moveTo(particles[i].x, particles[i].y)
        ctx.lineTo(particles[j].x, particles[j].y)
        ctx.stroke()
      }
    }
  }

  // Draw & update particles
  for (const p of particles) {
    p.x += p.vx
    p.y += p.vy

    if (p.x < 0 || p.x > canvas.width) p.vx *= -1
    if (p.y < 0 || p.y > canvas.height) p.vy *= -1

    ctx.beginPath()
    ctx.arc(p.x, p.y, p.radius, 0, Math.PI * 2)
    ctx.fillStyle = `rgba(6, 182, 212, ${p.opacity})`
    ctx.fill()
  }

  animationId = requestAnimationFrame(() => draw(canvas))
}

function handleResize() {
  const canvas = canvasRef.value
  if (!canvas) return
  canvas.width = canvas.offsetWidth
  canvas.height = canvas.offsetHeight
  initParticles(canvas)
}

onMounted(() => {
  const canvas = canvasRef.value
  if (!canvas) return
  handleResize()
  draw(canvas)
  window.addEventListener('resize', handleResize)
})

onUnmounted(() => {
  if (animationId) cancelAnimationFrame(animationId)
  window.removeEventListener('resize', handleResize)
})
</script>
