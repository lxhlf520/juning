import { onMounted, onUnmounted } from 'vue'

export function useScrollReveal() {
  let observer: IntersectionObserver | null = null
  let mutationObserver: MutationObserver | null = null

  function observeElements() {
    if (!observer) return
    document.querySelectorAll('.reveal:not(.visible)').forEach((el) => {
      observer?.observe(el)
    })
  }

  onMounted(() => {
    observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            entry.target.classList.add('visible')
            observer?.unobserve(entry.target)
          }
        })
      },
      { threshold: 0.1 }
    )

    observeElements()

    // 用 MutationObserver 监听新增的 .reveal 元素（异步数据渲染后）
    mutationObserver = new MutationObserver(() => {
      observeElements()
    })
    mutationObserver.observe(document.body, {
      childList: true,
      subtree: true,
    })
  })

  onUnmounted(() => {
    observer?.disconnect()
    mutationObserver?.disconnect()
  })
}
