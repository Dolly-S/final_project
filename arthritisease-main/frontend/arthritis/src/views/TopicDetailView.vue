<template>
  <div class="topic-detail">
    <div class="topic-content">
      <h1>{{ topic.title }}</h1>
      <div class="topic-meta">
        <span class="date">{{ formatDate(topic.createdAt) }}</span>
        <span class="author">{{ topic.anonymousName }}</span>
      </div>
      <div class="content">{{ topic.content }}</div>
    </div>

    <div class="comments-section">
      <h2>评论区</h2>
      
      <!-- 评论输入框 -->
      <div class="comment-form">
        <div class="input-wrapper">
          <textarea 
            v-model="commentInput"
            placeholder="分享你的想法..."
            :maxlength="500"
          ></textarea>
          <div class="input-footer">
            <div class="input-status">
              <span class="char-count">{{ commentInput.length }}/500</span>
            </div>
            <div class="error-message" v-if="errorMsg">{{ errorMsg }}</div>
          </div>
        </div>
        <button 
          class="submit-btn"
          :disabled="!canSubmit || isSubmitting"
          @click="submitComment"
        >
          {{ isSubmitting ? '发送中...' : '发送' }}
        </button>
      </div>

      <!-- 评论列表 -->
      <div class="comments-list">
        <div v-for="comment in comments" :key="comment.commentId" class="comment-item">
          <div class="comment-header">
            <span class="author">{{ comment.anonymousName }}</span>
            <span class="date">{{ formatDate(comment.createdAt) }}</span>
          </div>
          <div class="comment-content">{{ comment.content }}</div>
        </div>
      </div>
    </div>

    <!-- 评论输入框下方插入弹窗 -->
    <ProfileDialog v-model:show="showProfileDialog" :is-edit="false" />
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { API_ENDPOINTS } from '@/config/api'
import { useRoute } from 'vue-router'
import ProfileDialog from '@/components/ProfileDialog.vue'

const route = useRoute()
const userStore = useUserStore()
const commentInput = ref('')
const errorMsg = ref('')
const isSubmitting = ref(false)
const comments = ref([])
const topic = ref({})
const showProfileDialog = ref(false)

// 提交评论
async function submitComment() {
  if (isSubmitting.value) return
  if (!userStore.anonymousName) {
    showProfileDialog.value = true
    errorMsg.value = '请先设置用户名'
    return
  }
  if (!userStore.sessionId) {
    userStore.resetSession()
  }
  if (!canSubmit.value) return
  try {
    isSubmitting.value = true
    errorMsg.value = ''

    // 先进行内容审核
    const filterResponse = await fetch('https://api.arthritisease.org/filterInappropriateComments/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        content: commentInput.value.trim()
      })
    })

    if (!filterResponse.ok) {
      throw new Error('内容审核服务异常')
    }

    const filterResult = await filterResponse.json()
    
    if (filterResult.isFlagged) {
      errorMsg.value = `评论内容不合适: ${filterResult.reason}`
      return
    }

    // 发送评论
    const response = await fetch(API_ENDPOINTS.COMMENTS, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        topicId: topic.value.topicId,
        content: commentInput.value.trim(),
        sessionId: userStore.sessionId,
        anonymousName: userStore.anonymousName
      })
    })

    if (!response.ok) {
      throw new Error('评论发送失败')
    }

    const data = await response.json()
    comments.value.unshift(data)
    commentInput.value = ''
  } catch (error) {
    errorMsg.value = error.message
  } finally {
    isSubmitting.value = false
  }
}

// 格式化日期
function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString('zh-CN', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// 是否可以提交
const canSubmit = computed(() => {
  return commentInput.value.trim().length > 0 && 
         commentInput.value.length <= 500 &&
         !errorMsg.value &&
         userStore.anonymousName
})

// 获取话题详情和评论
async function fetchTopicAndComments() {
  try {
    const [topicRes, commentsRes] = await Promise.all([
      fetch(`${API_ENDPOINTS.TOPICS}/${route.params.id}`),
      fetch(`${API_ENDPOINTS.COMMENTS}?topicId=${route.params.id}`)
    ])

    if (!topicRes.ok || !commentsRes.ok) {
      throw new Error('获取数据失败')
    }

    const [topicData, commentsData] = await Promise.all([
      topicRes.json(),
      commentsRes.json()
    ])

    topic.value = topicData
    comments.value = commentsData
  } catch (error) {
    console.error('获取数据失败:', error)
  }
}

onMounted(() => {
  fetchTopicAndComments()
})
</script>

<style scoped>
.topic-detail {
  max-width: 800px;
  margin: 0 auto;
  padding: 20px;
}

.topic-content {
  background: white;
  border-radius: 12px;
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.topic-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  margin: 12px 0;
  color: #666;
  font-size: 14px;
}

.content {
  margin-top: 20px;
  line-height: 1.6;
  color: #333;
}

.comments-section {
  background: white;
  border-radius: 12px;
  padding: 24px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.comment-form {
  margin-bottom: 24px;
}

.input-wrapper {
  margin-bottom: 12px;
}

textarea {
  width: 100%;
  min-height: 100px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 8px;
  resize: vertical;
  font-size: 14px;
}

textarea:focus {
  outline: none;
  border-color: #4a6741;
  box-shadow: 0 0 0 2px rgba(74, 103, 65, 0.1);
}

.input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.input-status {
  display: flex;
  align-items: center;
  gap: 12px;
}

.char-count {
  color: #999;
  font-size: 13px;
}

.error-message {
  color: #ff4d4f;
  font-size: 13px;
}

.submit-btn {
  background: #4a6741;
  color: white;
  border: none;
  padding: 8px 24px;
  border-radius: 6px;
  cursor: pointer;
  font-size: 14px;
  transition: all 0.2s;
}

.submit-btn:hover:not(:disabled) {
  background: #3a5331;
}

.submit-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
}

.comments-list {
  margin-top: 24px;
}

.comment-item {
  padding: 16px 0;
  border-bottom: 1px solid #eee;
}

.comment-item:last-child {
  border-bottom: none;
}

.comment-header {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 8px;
}

.author {
  color: #4a6741;
  font-weight: 500;
}

.date {
  color: #999;
  font-size: 13px;
}

.comment-content {
  color: #333;
  line-height: 1.5;
}
</style> 