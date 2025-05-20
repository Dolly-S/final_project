<template>
  <div class="quiz-progress-bar">
    <div class="bar" :style="barStyle"></div>
    <div class="timer">{{ timeLeft }}s</div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
const props = defineProps({
  timeLeft: { type: Number, default: 15 }
})
const maxTime = 15
const percent = computed(() => Math.max(0, Math.min(100, (props.timeLeft / maxTime) * 100)))
const barColor = computed(() => {
  // 绿色到红色渐变
  const t = 1 - props.timeLeft / maxTime
  // 0: #4ade80, 0.5: #facc15, 1: #f87171
  if (t < 0.5) {
    // 绿色到黄色
    const ratio = t / 0.5
    return `rgb(${76 + (250-76)*ratio}, ${222 + (204-222)*ratio}, ${128 + (21-128)*ratio})` // #4ade80 -> #facc15
  } else {
    // 黄色到红色
    const ratio = (t-0.5)/0.5
    return `rgb(${250 + (248-250)*ratio}, ${204 + (113-204)*ratio}, ${21 + (113-21)*ratio})` // #facc15 -> #f87171
  }
})
const barStyle = computed(() => ({
  width: percent.value + '%',
  background: barColor.value,
  transition: 'width 0.5s linear, background 0.5s linear'
}))
</script>

<style scoped>
.quiz-progress-bar {
  width: 100%;
  height: 18px;
  background: #e0e7ff;
  border-radius: 9px;
  margin-bottom: 1.1rem;
  position: relative;
  overflow: hidden;
}
.bar {
  height: 100%;
  border-radius: 9px;
  transition: width 0.5s linear, background 0.5s linear;
}
.timer {
  position: absolute;
  right: 14px;
  top: 0;
  font-size: 1.05rem;
  color: #64748b;
  line-height: 18px;
  font-weight: 500;
}
</style> 