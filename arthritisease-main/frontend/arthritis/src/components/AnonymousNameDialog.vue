<template>
  <div class="dialog-overlay" v-show="show" @click.self="closeDialog">
    <div class="dialog-content">
      <div class="dialog-title">
        <h3>{{ props.isEdit ? 'Edit Nickname' : 'Set Nickname' }}</h3>
        <span v-if="props.isEdit" class="current-name">
          Current: {{ userStore.anonymousName }}
        </span>
      </div>

      <div class="input-group" :class="{ error: !!errorMsg }">
        <input
          ref="inputRef"
          v-model.trim="nameInput"
          type="text"
          :placeholder="props.isEdit ? 'Enter new nickname' : 'Enter nickname'"
          maxlength="20"
          @keyup.enter="handleSubmit"
        />
        <div class="input-hint">
          <span class="error-text" v-if="errorMsg">{{ errorMsg }}</span>
          <span class="char-count">{{ nameInput.length }}/20</span>
        </div>
      </div>

      <div class="dialog-buttons">
        <button 
          class="cancel-btn" 
          @click="closeDialog"
          :disabled="isSubmitting"
        >
          Cancel
        </button>
        <button 
          v-if="props.isEdit"
          class="reset-btn" 
          @click="handleReset"
          :disabled="isSubmitting"
        >
          Random Name
        </button>
        <button 
          class="submit-btn" 
          @click="handleSubmit"
          :disabled="!canSubmit"
        >
          {{ submitButtonText }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick } from 'vue'
import { useUserStore } from '@/stores/userStore'

const props = defineProps({
  show: Boolean,
  isEdit: Boolean
})

const emit = defineEmits(['update:show', 'name-set'])
const userStore = useUserStore()

const nameInput = ref('')
const errorMsg = ref('')
const isSubmitting = ref(false)
const inputRef = ref(null)

const canSubmit = computed(() => {
  return nameInput.value.length >= 2 && 
         nameInput.value.length <= 20 && 
         !isSubmitting.value
})

const submitButtonText = computed(() => {
  if (isSubmitting.value) return 'Saving...'
  return props.isEdit ? 'Save' : 'Confirm'
})

watch(() => props.show, async (newVal) => {
  if (newVal) {
    errorMsg.value = ''
    nameInput.value = ''
    await nextTick()
    inputRef.value?.focus()
  }
})

function closeDialog() {
  if (isSubmitting.value) return
  emit('update:show', false)
}

async function handleSubmit() {
  if (!canSubmit.value) return
  
  try {
    isSubmitting.value = true
    errorMsg.value = ''
    
    await userStore.setAnonymousName(nameInput.value)
    emit('name-set', nameInput.value)
    emit('update:show', false)
  } catch (err) {
    errorMsg.value = err.message
  } finally {
    isSubmitting.value = false
  }
}

async function handleReset() {
  try {
    isSubmitting.value = true
    errorMsg.value = ''
    
    userStore.resetAnonymousName()
    emit('name-set', userStore.anonymousName)
    emit('update:show', false)
  } catch {
    errorMsg.value = 'Reset failed, please try again'
  } finally {
    isSubmitting.value = false
  }
}
</script>

<style scoped>
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(0, 0, 0, 0.5);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 1000;
}

.dialog-content {
  background: white;
  width: 90%;
  max-width: 360px;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.15);
}

.dialog-title {
  margin-bottom: 20px;
}

.dialog-title h3 {
  margin: 0;
  font-size: 18px;
  color: #333;
}

.current-name {
  display: block;
  margin-top: 8px;
  font-size: 14px;
  color: #666;
}

.input-group {
  margin-bottom: 24px;
}

.input-group input {
  width: 100%;
  padding: 10px 12px;
  border: 1px solid #ddd;
  border-radius: 6px;
  font-size: 15px;
  transition: all 0.2s;
}

.input-group input:focus {
  outline: none;
  border-color: #4a6741;
  box-shadow: 0 0 0 2px rgba(74, 103, 65, 0.1);
}

.input-group.error input {
  border-color: #ff4d4f;
}

.input-hint {
  margin-top: 6px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 12px;
}

.error-text {
  color: #ff4d4f;
}

.char-count {
  color: #999;
}

.dialog-buttons {
  display: flex;
  gap: 8px;
}

button {
  flex: 1;
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.cancel-btn {
  background: #f5f5f5;
  color: #666;
}

.cancel-btn:hover:not(:disabled) {
  background: #e8e8e8;
}

.reset-btn {
  background: #e8e8e8;
  color: #333;
}

.reset-btn:hover:not(:disabled) {
  background: #ddd;
}

.submit-btn {
  background: #4a6741;
  color: white;
}

.submit-btn:hover:not(:disabled) {
  background: #3a5331;
}

@media (max-width: 480px) {
  .dialog-content {
    width: 95%;
    padding: 16px;
  }
  
  button {
    padding: 10px;
  }
}
</style> 