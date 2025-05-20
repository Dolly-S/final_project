<template>
  <Teleport to="body">
    <div v-if="show" class="dialog-overlay" @click.self="closeDialog">
      <div class="dialog-content">
        <div class="dialog-header">
          <h3>Create New Topic</h3>
          <button class="close-btn" @click="closeDialog">×</button>
        </div>

        <div class="dialog-body">
          <div class="input-group" :class="{ error: errors.title }">
            <label>Title</label>
            <input
              ref="titleInput"
              v-model.trim="title"
              type="text"
              placeholder="Enter topic title"
              maxlength="100"
              @input="validateTitle"
            />
            <div class="input-hint">
              <span class="error-text" v-if="errors.title">{{ errors.title }}</span>
              <span class="char-count">{{ title.length }}/100</span>
            </div>
          </div>

          <div class="input-group" :class="{ error: errors.category }">
            <label>Category</label>
            <select v-model="category" @change="validateCategory">
              <option value="">Select a category</option>
              <option v-for="cat in categories" :key="cat.id" :value="cat.id">
                {{ cat.icon }} {{ cat.name }}
              </option>
            </select>
            <div class="input-hint">
              <span class="error-text" v-if="errors.category">{{ errors.category }}</span>
            </div>
          </div>

          <div class="input-group" :class="{ error: errors.content }">
            <label>Content</label>
            <textarea
              v-model.trim="content"
              placeholder="Share your thoughts..."
              rows="6"
              maxlength="2000"
              @input="validateContent"
            ></textarea>
            <div class="input-hint">
              <span class="error-text" v-if="errors.content">{{ errors.content }}</span>
              <span class="char-count">{{ content.length }}/2000</span>
            </div>
          </div>

          <div class="guidelines">
            <h4>Community Guidelines:</h4>
            <ul>
              <li>Be respectful and supportive</li>
              <li>Share personal experiences</li>
              <li>No medical advice or diagnosis</li>
              <li>No promotional content or spam</li>
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
            class="submit-btn" 
            @click="handleSubmit"
            :disabled="!isValid || isSubmitting"
          >
            {{ submitButtonText }}
          </button>
        </div>
      </div>
    </div>
  </Teleport>
</template>

<script setup>
import { ref, computed, watchEffect } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { createTopic } from '@/config/api'

const props = defineProps({
  show: {
    type: Boolean,
    default: false
  }
})

const emit = defineEmits(['update:show', 'topic-created'])

// Watch for changes in props.show
watchEffect(() => {
  if (props.show) {
    // Initialize when dialog is shown
    titleInput.value?.focus()
  }
})

const userStore = useUserStore()
const titleInput = ref(null)

const categories = [
  { id: 'general', name: 'General Discussion', icon: '💭' },
  { id: 'exercise', name: 'Exercise Tips', icon: '🏃' },
  { id: 'diet', name: 'Diet & Nutrition', icon: '🥗' },
  { id: 'medication', name: 'Medication', icon: '💊' },
  { id: 'lifestyle', name: 'Lifestyle', icon: '🌟' },
  { id: 'success', name: 'Success Stories', icon: '🎉' }
]

const title = ref('')
const category = ref('')
const content = ref('')
const isSubmitting = ref(false)
const errors = ref({
  title: '',
  category: '',
  content: ''
})

const isValid = computed(() => {
  return title.value.length >= 5 &&
         title.value.length <= 100 &&
         category.value &&
         content.value.length >= 20 &&
         content.value.length <= 2000 &&
         !Object.values(errors.value).some(error => error)
})

const submitButtonText = computed(() => {
  if (isSubmitting.value) return 'Creating...'
  return 'Create Topic'
})

// Error messages
const ERROR_MESSAGES = {
  TITLE_TOO_SHORT: 'Title must be at least 5 characters long',
  TITLE_TOO_LONG: 'Title must not exceed 100 characters',
  CATEGORY_REQUIRED: 'Please select a category',
  CONTENT_TOO_SHORT: 'Content must be at least 20 characters long',
  CONTENT_TOO_LONG: 'Content must not exceed 2000 characters',
  USER_INCOMPLETE: 'Incomplete user information. Please refresh the page and try again',
  MISSING_FIELDS: 'Missing required fields',
  CREATE_FAILED: 'Failed to create topic. Please try again later'
}

function validateTitle() {
  if (title.value.length < 5) {
    errors.value.title = ERROR_MESSAGES.TITLE_TOO_SHORT
  } else if (title.value.length > 100) {
    errors.value.title = ERROR_MESSAGES.TITLE_TOO_LONG
  } else {
    errors.value.title = ''
  }
}

function validateCategory() {
  if (!category.value) {
    errors.value.category = ERROR_MESSAGES.CATEGORY_REQUIRED
  } else {
    errors.value.category = ''
  }
}

function validateContent() {
  if (content.value.length < 20) {
    errors.value.content = ERROR_MESSAGES.CONTENT_TOO_SHORT
  } else if (content.value.length > 2000) {
    errors.value.content = ERROR_MESSAGES.CONTENT_TOO_LONG
  } else {
    errors.value.content = ''
  }
}

function resetForm() {
  title.value = ''
  category.value = ''
  content.value = ''
  errors.value = {
    title: '',
    category: '',
    content: ''
  }
}

function closeDialog() {
  if (isSubmitting.value) return
  resetForm()
  emit('update:show', false)
}

// AI内容审核API
async function filterInappropriateContent(content) {
  try {
    const response = await fetch('https://api.arthritisease.org/filterInappropriateComments/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ content })
    })
    if (!response.ok) throw new Error('内容审核服务异常')
    const data = await response.json()
    return { isFlagged: data.isFlagged, reason: data.reason }
  } catch (error) {
    console.error('内容审核失败:', error)
    throw new Error('内容审核失败，请稍后重试')
  }
}

async function handleSubmit() {
  if (!isValid.value || isSubmitting.value) return
  try {
    isSubmitting.value = true
    // 校验用户信息
    if (!userStore.anonymousName || !userStore.sessionId) {
      throw new Error('Incomplete user information. Please refresh the page and try again')
    }
    // AI审核标题
    const titleCheck = await filterInappropriateContent(title.value.trim())
    if (titleCheck.isFlagged) {
      alert('Title contains inappropriate content: ' + (titleCheck.reason || ''))
      return
    }
    // AI审核内容
    const contentCheck = await filterInappropriateContent(content.value.trim())
    if (contentCheck.isFlagged) {
      alert('Content contains inappropriate content: ' + (contentCheck.reason || ''))
      return
    }
    // AI审核匿名昵称
    const nameCheck = await filterInappropriateContent(userStore.anonymousName)
    if (nameCheck.isFlagged) {
      alert('Anonymous name contains inappropriate content: ' + (nameCheck.reason || ''))
      return
    }
    // 构造新话题对象
    const newTopic = {
      title: title.value.trim(),
      content: content.value.trim(),
      category: category.value,
      anonymousName: userStore.anonymousName,
      sessionId: userStore.sessionId
    }
    // 字段校验
    const requiredFields = ['title', 'content', 'category', 'anonymousName', 'sessionId']
    const missingFields = requiredFields.filter(field => !newTopic[field])
    if (missingFields.length > 0) {
      throw new Error(`Failed to create topic: Missing required fields ${missingFields.join(', ')}`)
    }
    // 调用后端API
    const res = await createTopic(newTopic)
    // 通知父组件并关闭弹窗
    emit('topic-created', res)
    resetForm()
    emit('update:show', false)
  } catch (error) {
    alert(error.message || 'Failed to create topic. Please try again later')
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
  max-width: 600px;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.15);
  max-height: 90vh;
  display: flex;
  flex-direction: column;
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
  overflow-y: auto;
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

.input-group input,
.input-group select,
.input-group textarea {
  width: 100%;
  padding: 0.75rem 1rem;
  border: 1px solid #ddd;
  border-radius: 8px;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.input-group textarea {
  resize: vertical;
  min-height: 120px;
}

.input-group input:focus,
.input-group select:focus,
.input-group textarea:focus {
  outline: none;
  border-color: #4a6741;
  box-shadow: 0 0 0 2px rgba(74, 103, 65, 0.1);
}

.input-group.error input,
.input-group.error select,
.input-group.error textarea {
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

.guidelines {
  background: #f8f9fa;
  padding: 1rem;
  border-radius: 8px;
  margin-top: 1rem;
}

.guidelines h4 {
  color: #333;
  margin: 0 0 0.5rem 0;
  font-size: 0.875rem;
}

.guidelines ul {
  margin: 0;
  padding-left: 1.25rem;
}

.guidelines li {
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
    max-height: 85vh;
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
</style> 