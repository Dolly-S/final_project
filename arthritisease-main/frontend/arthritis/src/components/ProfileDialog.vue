<template>
  <div class="dialog-overlay" v-show="show" @click.self="closeDialog">
    <div class="dialog-content">
      <div class="dialog-header">
        <h3>{{ props.isEdit ? 'Edit Profile' : 'Set Up Profile' }}</h3>
        <button class="close-btn" @click="closeDialog">×</button>
      </div>

      <div class="dialog-body">
        <div class="input-group" :class="{ error: !!errorMsg }">
          <label>Nickname</label>
          <input
            ref="inputRef"
            v-model.trim="nameInput"
            type="text"
            :placeholder="props.isEdit ? 'Enter new nickname' : 'Enter nickname'"
            maxlength="20"
            @keyup.enter="handleSubmit"
          />
          <div class="input-hint">
            <span class="error-text" v-if="errorMsgVisible && errorMsg" :class="'shake'" @animationend="onErrorMsgAnimationEnd">{{ errorMsg }}</span>
            <span class="char-count">{{ nameInput.length }}/20</span>
          </div>
        </div>

        <div class="nickname-rules">
          <h4>Nickname Rules:</h4>
          <ul>
            <li>Between 2-20 characters</li>
            <li>Cannot start with numbers</li>
            <li>No special characters (except underscore and dash)</li>
          </ul>
        </div>
      </div>

      <div class="dialog-footer">
        <button 
          class="cancel-btn" 
          @click="closeDialog"
          :disabled="isSubmitting"
        >
          Cancel
        </button>
        <button 
          v-if="props.isEdit"
          class="random-btn" 
          @click="handleReset"
          :disabled="isSubmitting"
        >
          Random Name
        </button>
        <button 
          class="submit-btn" 
          @click="handleSubmit"
          :disabled="!canSubmit || isSubmitting"
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

// Error messages
const ERROR_MESSAGES = {
  NICKNAME_TOO_SHORT: 'Nickname must be at least 2 characters',
  NICKNAME_TOO_LONG: 'Nickname cannot exceed 20 characters',
  NICKNAME_START_NUMBER: 'Nickname cannot start with a number',
  NICKNAME_INVALID_CHARS: 'Nickname contains invalid characters',
  VALIDATION_FAILED: 'Nickname validation failed, please try again',
  RANDOM_GENERATION_FAILED: 'Failed to generate random nickname, please try again',
  RANDOM_INVALID: 'Generated random nickname is invalid, please try again'
}

const props = defineProps({
  show: Boolean,
  isEdit: Boolean
})

const emit = defineEmits(['update:show'])
const userStore = useUserStore()

const nameInput = ref('')
const errorMsg = ref('')
const errorMsgVisible = ref(false)
const isSubmitting = ref(false)
const inputRef = ref(null)

const canSubmit = computed(() => {
  return nameInput.value.length >= 2 && 
         nameInput.value.length <= 20 && 
         !isSubmitting.value
})

const submitButtonText = computed(() => {
  if (isSubmitting.value) return 'Validating...'
  return props.isEdit ? 'Save Changes' : 'Create Profile'
})

watch(() => props.show, async (newVal) => {
  if (newVal) {
    errorMsg.value = ''
    nameInput.value = props.isEdit ? userStore.anonymousName : ''
    await nextTick()
    inputRef.value?.focus()
  }
})

function closeDialog() {
  if (isSubmitting.value) return
  emit('update:show', false)
}

async function filterInappropriateContent(content) {
  try {
    const response = await fetch('https://api.arthritisease.org/filterInappropriateComments/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    });
    if (!response.ok) throw new Error('Content moderation service error');
    const data = await response.json();
    return data; // { isFlagged: true/false, reason: 'xxx' }
  } catch (error) {
    console.error('Content moderation failed:', error);
    throw new Error('Content moderation failed, please try again later');
  }
}

async function validateNickname(nickname) {
  try {
    // AI content moderation
    const filterResult = await filterInappropriateContent(nickname);
    if (filterResult.isFlagged) {
      return { isValid: false, message: `Inappropriate nickname: ${filterResult.reason}` };
    }
    // Basic validation
    if (nickname.length < 2) {
      return { isValid: false, message: ERROR_MESSAGES.NICKNAME_TOO_SHORT }
    }
    if (nickname.length > 20) {
      return { isValid: false, message: ERROR_MESSAGES.NICKNAME_TOO_LONG }
    }
    if (/^[0-9]/.test(nickname)) {
      return { isValid: false, message: ERROR_MESSAGES.NICKNAME_START_NUMBER }
    }
    if (/[<>{}[\]\\]/.test(nickname)) {
      return { isValid: false, message: ERROR_MESSAGES.NICKNAME_INVALID_CHARS }
    }
    
    return { isValid: true }
  } catch (error) {
    console.error('Nickname validation error:', error)
    throw new Error(ERROR_MESSAGES.VALIDATION_FAILED)
  }
}

function showErrorMsg(msg) {
  errorMsg.value = msg
  errorMsgVisible.value = true
  setTimeout(() => errorMsgVisible.value = false, 3000)
}

function onErrorMsgAnimationEnd() {}

async function handleSubmit() {
  if (!canSubmit.value) return
  
  try {
    isSubmitting.value = true
    errorMsg.value = ''
    
    const validationResult = await validateNickname(nameInput.value)
    if (!validationResult.isValid) {
      showErrorMsg(validationResult.message)
      return
    }
    
    await userStore.setAnonymousName(nameInput.value)
    emit('update:show', false)
  } catch (err) {
    showErrorMsg(err.message)
  } finally {
    isSubmitting.value = false
  }
}

async function handleReset() {
  try {
    isSubmitting.value = true
    errorMsg.value = ''
    
    const randomName = `User${Math.floor(Math.random() * 10000)}`
    // Validate random nickname
    const validationResult = await validateNickname(randomName)
    if (!validationResult.isValid) {
      throw new Error(ERROR_MESSAGES.RANDOM_INVALID)
    }
    
    await userStore.setAnonymousName(randomName)
    emit('update:show', false)
  } catch (error) {
    showErrorMsg(error.message || ERROR_MESSAGES.RANDOM_GENERATION_FAILED)
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
  max-width: 500px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
}

.dialog-header {
  padding: 1.5rem;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.dialog-header h3 {
  margin: 0;
  font-size: 1.5rem;
  color: #333;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 0.5rem;
  line-height: 1;
  transition: all 0.3s ease;
}

.close-btn:hover {
  color: #333;
}

.dialog-body {
  padding: 1.5rem;
}

.input-group {
  margin-bottom: 1.5rem;
}

.input-group label {
  display: block;
  margin-bottom: 0.5rem;
  color: #333;
  font-weight: 500;
}

.input-group input {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-group input:focus {
  outline: none;
  border-color: #4a6741;
  box-shadow: 0 0 0 2px rgba(74, 103, 65, 0.1);
}

.input-group.error input {
  border-color: #dc3545;
}

.input-hint {
  margin-top: 0.5rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 0.875rem;
}

.error-text {
  color: #dc3545;
}

.char-count {
  color: #666;
}

.nickname-rules {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-bottom: 1rem;
}

.nickname-rules h4 {
  color: #333;
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
}

.nickname-rules ul {
  margin: 0;
  padding-left: 1.25rem;
}

.nickname-rules li {
  color: #666;
  font-size: 0.875rem;
  margin-bottom: 0.25rem;
}

.dialog-footer {
  padding: 1rem 1.5rem;
  border-top: 1px solid #eee;
  display: flex;
  justify-content: flex-end;
  gap: 0.75rem;
}

button {
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 6px;
  font-size: 0.875rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
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

.random-btn {
  background: #e8e8e8;
  color: #333;
}

.random-btn:hover:not(:disabled) {
  background: #ddd;
}

.submit-btn {
  background: #4a6741;
  color: white;
  min-width: 120px;
}

.submit-btn:hover:not(:disabled) {
  background: #3a5331;
}

@media (max-width: 480px) {
  .dialog-content {
    width: 95%;
    margin: 1rem;
  }
  
  .dialog-header h3 {
    font-size: 1.25rem;
  }
  
  .dialog-footer {
    flex-direction: column-reverse;
  }
  
  button {
    width: 100%;
  }
}

.error-text.shake {
  color: #dc3545;
  background: #fff0f0;
  border: 1px solid #ffb3b3;
  border-radius: 6px;
  padding: 4px 12px;
  margin-right: 8px;
  box-shadow: 0 2px 8px rgba(220,53,69,0.08);
  animation: shake 0.4s, fadeIn 0.3s;
  transition: opacity 0.5s;
}
@keyframes shake {
  0% { transform: translateX(0); }
  20% { transform: translateX(-8px); }
  40% { transform: translateX(8px); }
  60% { transform: translateX(-6px); }
  80% { transform: translateX(6px); }
  100% { transform: translateX(0); }
}
@keyframes fadeIn {
  from { opacity: 0; }
  to   { opacity: 1; }
}
</style> 