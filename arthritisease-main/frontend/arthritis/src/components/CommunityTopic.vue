<template>
  <div class="name-card">
    <div class="user-info" v-if="userStore.anonymousName">
      <span class="label">当前昵称:</span>
      <span class="name">{{ userStore.anonymousName }}</span>
      <div class="name-actions">
        <button class="edit-btn" @click="startEdit">修改</button>
        <button class="reset-btn" @click="handleReset">随机昵称</button>
      </div>
    </div>
    
    <div v-if="isEditing" class="name-editor">
      <div class="nickname-rules">
        <h4>昵称规则:</h4>
        <ul>
          <li>长度在2-20个字符之间</li>
          <li>不能包含不当或攻击性内容</li>
          <li>不能冒充他人</li>
          <li>不能包含垃圾信息</li>
        </ul>
      </div>
      
      <div class="input-group" :class="{ error: !!errorMsg }">
        <input
          ref="inputRef"
          v-model.trim="nameInput"
          type="text"
          placeholder="输入新昵称 (2-20个字符)"
          maxlength="20"
          @keyup.enter="handleSubmit"
        />
        <div class="input-hint">
          <span class="error-text" v-if="errorMsg">{{ errorMsg }}</span>
          <span class="char-count">{{ nameInput.length }}/20</span>
        </div>
      </div>
      
      <div class="validation-info">
        <span class="info-icon">🤖</span>
        <span>您的昵称将由AI进行内容审核</span>
      </div>
      
      <div class="editor-actions">
        <button class="cancel-btn" @click="cancelEdit">取消</button>
        <button 
          class="submit-btn" 
          @click="handleSubmit"
          :disabled="!canSubmit || isSubmitting"
        >
          {{ isSubmitting ? '审核中...' : '确认' }}
        </button>
      </div>
    </div>

    <div v-else-if="!userStore.anonymousName" class="name-setup">
      <p>设置昵称以加入讨论</p>
      <button class="setup-btn" @click="startEdit">设置昵称</button>
    </div>
  </div>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { API_ENDPOINTS } from '@/config/api'

const emit = defineEmits(['update'])
const userStore = useUserStore()
const inputRef = ref(null)
const isEditing = ref(false)
const isSubmitting = ref(false)
const nameInput = ref('')
const errorMsg = ref('')

const canSubmit = computed(() => {
  return nameInput.value.length >= 2 && 
         nameInput.value.length <= 20 && 
         !isSubmitting.value
})

function startEdit() {
  isEditing.value = true
  nameInput.value = userStore.anonymousName || ''
  errorMsg.value = ''
  setTimeout(() => {
    inputRef.value?.focus()
  }, 0)
}

function cancelEdit() {
  isEditing.value = false
  nameInput.value = ''
  errorMsg.value = ''
}

// AI内容审核
async function filterInappropriateContent(content) {
  try {
    const response = await fetch('https://api.arthritisease.org/filterInappropriateComments/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: content
      })
    })

    if (!response.ok) {
      throw new Error('内容审核服务异常')
    }

    const data = await response.json()
    return {
      isFlagged: data.isFlagged,
      reason: data.reason
    }
  } catch (error) {
    console.error('内容审核失败:', error)
    throw new Error('内容审核失败，请稍后重试')
  }
}

async function validateNickname(nickname) {
  try {
    // 先进行AI内容审核
    const filterResult = await filterInappropriateContent(nickname)
    if (filterResult.isFlagged) {
      return {
        isValid: false,
        message: `昵称不合适: ${filterResult.reason}`
      }
    }

    // 再进行常规验证
    const response = await fetch('https://api.arthritisease.org/validateNickname', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({ nickname })
    })

    if (!response.ok) {
      throw new Error('验证服务异常')
    }

    const data = await response.json()
    return {
      isValid: data.isValid,
      message: data.message
    }
  } catch (error) {
    console.error('昵称验证错误:', error)
    throw new Error('昵称验证失败，请稍后重试')
  }
}

async function handleSubmit() {
  if (!canSubmit.value || isSubmitting.value) return
  
  try {
    isSubmitting.value = true
    errorMsg.value = ''

    // 验证昵称
    const validationResult = await validateNickname(nameInput.value)
    if (!validationResult.isValid) {
      errorMsg.value = validationResult.message
      return
    }

    // 更新昵称
    const response = await fetch(API_ENDPOINTS.UPDATE_NICKNAME, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        nickname: nameInput.value,
        sessionId: userStore.sessionId
      })
    })

    if (!response.ok) {
      throw new Error('更新昵称失败')
    }

    const data = await response.json()
    userStore.setAnonymousName(data.nickname)
    isEditing.value = false
    nameInput.value = ''
    emit('update')
  } catch (error) {
    errorMsg.value = error.message
  } finally {
    isSubmitting.value = false
  }
}

async function handleReset() {
  try {
    const response = await fetch(API_ENDPOINTS.RANDOM_NICKNAME, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json'
      }
    })

    if (!response.ok) {
      throw new Error('获取随机昵称失败')
    }

    const data = await response.json()
    userStore.setAnonymousName(data.nickname)
    emit('update')
  } catch (error) {
    console.error('重置昵称失败:', error)
  }
}
</script>

<style scoped>
.name-card {
  padding: 24px;
  background: white;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  max-width: 600px;
  margin: 0 auto;
}

.user-info {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 8px 0;
}

.label {
  color: #666;
  font-size: 15px;
}

.name {
  color: #4a6741;
  font-weight: 500;
  font-size: 16px;
}

.name-actions {
  margin-left: auto;
  display: flex;
  gap: 12px;
}

.name-editor {
  margin-top: 20px;
  border-top: 1px solid #eee;
  padding-top: 20px;
}

.nickname-rules {
  background: #f8f9fa;
  padding: 16px;
  border-radius: 8px;
  margin-bottom: 20px;
}

.nickname-rules h4 {
  color: #4a6741;
  margin: 0 0 8px 0;
  font-size: 15px;
}

.nickname-rules ul {
  margin: 0;
  padding-left: 20px;
}

.nickname-rules li {
  color: #666;
  font-size: 13px;
  margin-bottom: 4px;
}

.validation-info {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 12px;
  background: #fff8e6;
  border-radius: 6px;
  margin: 16px 0;
  font-size: 13px;
  color: #666;
}

.info-icon {
  font-size: 16px;
}

.input-group {
  margin-bottom: 16px;
}

.input-group input {
  width: 100%;
  padding: 12px 16px;
  border: 1px solid #ddd;
  border-radius: 8px;
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
  margin-top: 8px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  font-size: 13px;
}

.error-text {
  color: #ff4d4f;
}

.char-count {
  color: #999;
}

.editor-actions {
  display: flex;
  justify-content: flex-end;
  gap: 12px;
}

.name-setup {
  text-align: center;
  padding: 32px 0;
}

.name-setup p {
  color: #666;
  margin-bottom: 16px;
  font-size: 16px;
}

button {
  padding: 8px 16px;
  border: none;
  border-radius: 6px;
  font-size: 14px;
  cursor: pointer;
  transition: all 0.2s;
  font-weight: 500;
}

button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.edit-btn {
  background: #4a6741;
  color: white;
}

.edit-btn:hover:not(:disabled) {
  background: #3a5331;
}

.reset-btn {
  background: #f5f5f5;
  color: #666;
}

.reset-btn:hover:not(:disabled) {
  background: #e8e8e8;
}

.setup-btn {
  background: #4a6741;
  color: white;
  padding: 12px 28px;
  font-size: 15px;
}

.setup-btn:hover:not(:disabled) {
  background: #3a5331;
  transform: translateY(-1px);
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
  min-width: 100px;
}

.submit-btn:hover:not(:disabled) {
  background: #3a5331;
}

@media (max-width: 768px) {
  .name-card {
    border-radius: 8px;
    padding: 20px;
  }
  
  .user-info {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }
  
  .name-actions {
    margin-left: 0;
    width: 100%;
  }
  
  .name-actions button {
    flex: 1;
  }
  
  .editor-actions {
    flex-direction: column;
  }
  
  .editor-actions button {
    width: 100%;
  }
}
</style> 