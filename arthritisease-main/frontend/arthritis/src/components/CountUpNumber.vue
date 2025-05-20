<template>
  <span :class="{ 'highlight': highlight }">{{ displayValue }}</span>
</template>

<script setup>
import { ref, watch, onMounted } from 'vue'

const props = defineProps({
  value: { type: Number, required: true },
  duration: { type: Number, default: 800 } // ms
})

const displayValue = ref(props.value)
const highlight = ref(false)

function animateNumber(from, to, duration) {
  const start = performance.now()
  function step(now) {
    const progress = Math.min((now - start) / duration, 1)
    displayValue.value = (from + (to - from) * progress).toFixed(2)
    if (progress < 1) {
      requestAnimationFrame(step)
    } else {
      displayValue.value = to.toFixed(2)
    }
  }
  requestAnimationFrame(step)
}

watch(() => props.value, (newVal, oldVal) => {
  highlight.value = true
  animateNumber(Number(oldVal), Number(newVal), props.duration)
  setTimeout(() => { highlight.value = false }, 600)
})

onMounted(() => {
  displayValue.value = Number(props.value).toFixed(2)
})
</script>

<style scoped>
.highlight {
  background: #fffbe6;
  transition: background 0.5s;
  border-radius: 6px;
  padding: 0 4px;
}
</style> 