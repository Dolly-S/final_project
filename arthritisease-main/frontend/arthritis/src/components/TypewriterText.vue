<template>
  <span>{{ displayText }}</span>
</template>

<script setup>
import { ref, watch } from 'vue'

const props = defineProps({
  text: { type: String, required: true },
  speed: { type: Number, default: 30 }
})

const emit = defineEmits(['typing'])
const displayText = ref('')

watch(() => props.text, (newVal) => {
  displayText.value = ''
  if (!newVal) return
  let i = 0
  function type() {
    if (i <= newVal.length) {
      displayText.value = newVal.slice(0, i)
      emit('typing')
      i++
      setTimeout(type, props.speed)
    }
  }
  type()
}, { immediate: true })
</script> 