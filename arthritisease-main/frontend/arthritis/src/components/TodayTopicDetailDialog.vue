<template>
  <div class="comment-page">
    <!-- Topic Card -->
    <div class="topic-card-modern">
      <h1 class="topic-title">Today's Topic</h1>
      <div class="topic-meta-modern">
        <span class="topic-date">{{ formatDate(topic.createdAt) }}</span>
        <span class="topic-author">{{ topic.anonymousName === '系统' ? 'System' : topic.anonymousName }}</span>
      </div>
      <div class="topic-content-modern">{{ topic.content }}</div>
    </div>
    <!-- Comments Card -->
    <div class="comments-card-modern">
      <h2 class="comments-title">Comments</h2>
      <div class="comment-input-modern">
        <textarea
          v-model="commentInput"
          placeholder="Share your thoughts..."
          :maxlength="500"
          @focus="inputFocused = true"
          @blur="inputFocused = false"
        ></textarea>
        <div class="comment-input-footer">
          <span class="char-count">{{ commentInput.length }}/500</span>
          <button
            class="send-btn-modern"
            :class="{ sending: isSubmitting }"
            :disabled="!canSubmit || isSubmitting"
            @click="submitComment"
          >
            <span v-if="isSubmitting" class="loader"></span>
            <span v-else>Send</span>
          </button>
        </div>
        <transition name="shake-fade">
          <div v-if="errorMsgVisible && errorMsg" class="error-message-modern">
            {{ errorMsg }}
          </div>
        </transition>
      </div>
      <div class="comments-list-modern">
        <transition-group name="fade-slide" tag="div">
          <div
            v-for="comment in comments"
            :key="comment.commentId"
            class="comment-item-modern"
          >
            <div class="comment-avatar">{{ getAvatar(comment.anonymousName) }}</div>
            <div class="comment-body">
              <div class="comment-header-modern">
                <span class="comment-author">{{ comment.anonymousName === '系统' ? 'System' : comment.anonymousName }}</span>
                <span class="comment-date">{{ formatDate(comment.createdAt) }}</span>
              </div>
              <div class="comment-content-modern">{{ comment.content }}</div>
            </div>
          </div>
        </transition-group>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { API_ENDPOINTS } from '@/config/api'

const props = defineProps({
  topic: {
    type: Object,
    required: true
  }
})
const emit = defineEmits(['update:comments'])

const userStore = useUserStore()
const commentInput = ref('')
const errorMsg = ref('')
const errorMsgVisible = ref(false)
const isSubmitting = ref(false)
const inputFocused = ref(false)
const comments = ref([])

function showErrorMsg(msg) {
  errorMsg.value = msg
  errorMsgVisible.value = true
  setTimeout(() => errorMsgVisible.value = false, 3000)
}

// Submit comment
async function submitComment() {
  if (!canSubmit.value || isSubmitting.value) return
  try {
    isSubmitting.value = true
    errorMsg.value = ''
    // Content moderation
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
      throw new Error('Content moderation service error')
    }
    const filterResult = await filterResponse.json()
    if (filterResult.isFlagged) {
      showErrorMsg(`Inappropriate comment: ${filterResult.reason}`)
      isSubmitting.value = false
      return
    }
    // Submit comment
    const response = await fetch(API_ENDPOINTS.COMMENTS, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json'
      },
      body: JSON.stringify({
        topicId: props.topic.topicId,
        content: commentInput.value.trim(),
        sessionId: userStore.sessionId,
        anonymousName: userStore.anonymousName
      })
    })
    if (!response.ok) {
      throw new Error('Failed to submit comment')
    }
    const data = await response.json()
    comments.value.unshift(data)
    commentInput.value = ''
    emit('update:comments', comments.value)
  } catch (error) {
    showErrorMsg(error.message)
  } finally {
    isSubmitting.value = false
  }
}

// Format date (English)
function formatDate(dateStr) {
  const date = new Date(dateStr)
  return date.toLocaleString('en-US', {
    year: 'numeric',
    month: '2-digit',
    day: '2-digit',
    hour: '2-digit',
    minute: '2-digit'
  })
}

// Can submit
const canSubmit = computed(() => {
  return commentInput.value.trim().length > 0 && 
         commentInput.value.length <= 500 &&
         !errorMsg.value &&
         userStore.anonymousName
})

// Fetch comments
async function fetchComments() {
  try {
    const commentsRes = await fetch(`${API_ENDPOINTS.COMMENTS}?topicId=${props.topic.topicId}`)
    if (!commentsRes.ok) {
      throw new Error('Failed to fetch comments')
    }
    const commentsData = await commentsRes.json()
    comments.value = commentsData
  } catch {
    comments.value = []
  }
}

onMounted(() => {
  fetchComments()
})
// Refresh comments if topicId changes
watch(() => props.topic.topicId, () => {
  fetchComments()
})

function getAvatar(name) {
  if (!name) return '?'
  return name[0].toUpperCase()
}
</script>

<style scoped>
.comment-page {
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: 32px 0;
  min-height: 100vh;
  background: #f6f8fa;
  max-height: 90vh;
  height: 90vh;
  overflow-y: auto;
  scrollbar-width: none;        /* Firefox */
  -ms-overflow-style: none;     /* IE 10+ */
}
.comment-page::-webkit-scrollbar {
  display: none;                /* Chrome/Safari/Edge */
}
.topic-card-modern {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(60, 120, 80, 0.08);
  padding: 32px;
  margin: 0 auto;
  max-width: 700px;
  width: 100%;
  animation: fadeIn 0.6s;
}
.topic-title {
  font-size: 2rem;
  font-weight: 700;
  color: #2d4739;
  margin-bottom: 12px;
}
.topic-meta-modern {
  display: flex;
  gap: 18px;
  color: #7a8b99;
  font-size: 0.98rem;
  margin-bottom: 18px;
}
.topic-content-modern {
  font-size: 1.15rem;
  color: #333;
  line-height: 1.7;
}
.comments-card-modern {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(60, 120, 80, 0.08);
  padding: 32px;
  margin: 0 auto;
  max-width: 700px;
  width: 100%;
  animation: fadeIn 0.6s;
}
.comments-title {
  font-size: 1.3rem;
  font-weight: 600;
  color: #2d4739;
  margin-bottom: 18px;
}
.comment-input-modern {
  margin-bottom: 28px;
}
.comment-input-modern textarea {
  width: 100%;
  min-height: 90px;
  border-radius: 12px;
  border: 1.5px solid #e0e5dd;
  padding: 16px;
  font-size: 1rem;
  transition: border 0.2s, box-shadow 0.2s;
  box-shadow: 0 2px 8px rgba(60, 120, 80, 0.04);
}
.comment-input-modern textarea:focus {
  border-color: #4a6741;
  box-shadow: 0 2px 12px rgba(60, 120, 80, 0.10);
}
.comment-input-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 10px;
}
.char-count {
  color: #999;
  font-size: 0.95rem;
}
.send-btn-modern {
  background: #4a6741;
  color: #fff;
  border: none;
  border-radius: 20px;
  padding: 8px 28px;
  font-size: 1rem;
  font-weight: 600;
  cursor: pointer;
  transition: background 0.2s, transform 0.1s;
}
.send-btn-modern:hover:not(:disabled) {
  background: #3a5331;
  transform: scale(1.05);
}
.send-btn-modern:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}
.send-btn-modern.sending {
  background: #b7cbb0;
}
.loader {
  border: 2px solid #fff;
  border-top: 2px solid #4a6741;
  border-radius: 50%;
  width: 18px;
  height: 18px;
  animation: spin 0.8s linear infinite;
  display: inline-block;
  vertical-align: middle;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
.error-message-modern {
  color: #dc3545;
  background: #fff0f0;
  border: 1px solid #ffb3b3;
  border-radius: 6px;
  padding: 8px 16px;
  margin-top: 10px;
  font-size: 0.98rem;
  animation: shake 0.4s, fadeIn 0.3s;
  transition: opacity 0.5s;
}
@keyframes shake {
  0% { transform: translateX(0);}
  20% { transform: translateX(-8px);}
  40% { transform: translateX(8px);}
  60% { transform: translateX(-6px);}
  80% { transform: translateX(6px);}
  100% { transform: translateX(0);}
}
@keyframes fadeIn {
  from { opacity: 0;}
  to { opacity: 1;}
}
.comments-list-modern {
  display: flex;
  flex-direction: column;
  gap: 18px;
  max-height: unset;
  overflow-y: unset;
  padding-right: 4px;
}
.comment-item-modern {
  display: flex;
  align-items: flex-start;
  gap: 14px;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 16px 18px;
  box-shadow: 0 2px 8px rgba(60, 120, 80, 0.04);
  transition: box-shadow 0.2s, background 0.2s;
}
.comment-item-modern:hover {
  background: #eaf5ea;
  box-shadow: 0 4px 16px rgba(60, 120, 80, 0.10);
}
.comment-avatar {
  width: 38px;
  height: 38px;
  background: linear-gradient(135deg, #4a6741, #6b8f5e);
  color: #fff;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.1rem;
  font-weight: 600;
  flex-shrink: 0;
}
.comment-body {
  flex: 1;
}
.comment-header-modern {
  display: flex;
  align-items: center;
  gap: 12px;
  margin-bottom: 6px;
}
.comment-author {
  color: #4a6741;
  font-weight: 600;
}
.comment-date {
  color: #999;
  font-size: 0.93rem;
}
.comment-content-modern {
  color: #333;
  font-size: 1.05rem;
  line-height: 1.6;
}
.fade-slide-enter-active, .fade-slide-leave-active {
  transition: all 0.4s cubic-bezier(.4,0,.2,1);
}
.fade-slide-enter-from, .fade-slide-leave-to {
  opacity: 0;
  transform: translateY(20px);
}
@media (max-width: 600px) {
  .topic-card-modern, .comments-card-modern {
    padding: 14px;
    max-width: 100vw;
  }
  .comment-item-modern {
    padding: 10px 8px;
  }
}
</style> 