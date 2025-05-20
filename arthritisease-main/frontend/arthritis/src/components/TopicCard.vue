<template>
  <div class="topic-card" @click="showDetails">
    <div class="card-content">
      <h3 class="card-title">{{ topic.title }}</h3>
      <p class="card-description">{{ truncatedDescription }}</p>
      
      <div class="card-stats">
        <div class="stat-item">
          <button class="comment-button" @click.stop="showDetails">
            <span class="icon">💬</span>
            <span class="count">{{ comments.length }}</span>
          </button>
        </div>
      </div>
    </div>

    <!-- Topic Details Dialog -->
    <Teleport to="body">
      <div v-if="showDialog" class="dialog-overlay" @click="closeDialog">
        <div class="dialog-content" @click.stop style="position: relative;">
          <button class="close-button" @click="closeDialog" aria-label="Close">×</button>
          <div class="comment-page">
            <!-- Topic Card -->
            <div class="topic-card-modern">
              <h1 class="topic-title">{{ topic.title }}</h1>
              <div class="topic-meta-modern">
                <span class="topic-date">{{ formatDate(topic.createdAt) }}</span>
                <span class="topic-author">{{ topic.author || topic.userHash || 'Anonymous' }}</span>
              </div>
              <div class="topic-content-modern">{{ topic.content }}</div>
            </div>
            <!-- Comments Card -->
            <div class="comments-card-modern">
              <h2 class="comments-title">Comments</h2>
              <div class="comment-input-modern">
                <textarea
                  v-model="newComment"
                  placeholder="Share your thoughts..."
                  :maxlength="500"
                  @focus="inputFocused = true"
                  @blur="inputFocused = false"
                ></textarea>
                <div class="comment-input-footer">
                  <span class="char-count">{{ newComment.length }}/500</span>
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
                    :key="comment.id"
                    class="comment-item-modern"
                  >
                    <div class="comment-avatar">{{ getAvatar(comment.userHash) }}</div>
                    <div class="comment-body">
                      <div class="comment-header-modern">
                        <span class="comment-author">{{ comment.userHash }}</span>
                        <span class="comment-date">{{ formatTime(comment.timestamp) }}</span>
                      </div>
                      <div class="comment-content-modern">{{ comment.content }}</div>
                    </div>
                  </div>
                </transition-group>
              </div>
            </div>
          </div>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { addComment, getComments } from '@/config/api'

const props = defineProps({
  topic: {
    type: Object,
    required: true
  }
})

const emit = defineEmits(['update:comments'])
const userStore = useUserStore()
const showDialog = ref(false)
const newComment = ref('')
const isSubmitting = ref(false)
const views = ref(0)
const comments = ref([])
const errorMsg = ref('')
const errorMsgVisible = ref(false)
const inputFocused = ref(false)
const canSubmit = computed(() => newComment.value.trim().length > 0 && newComment.value.length <= 500 && !errorMsg.value && userStore.anonymousName)

const truncatedDescription = computed(() => {
  const maxLength = 100
  const content = props.topic.content
  return content.length > maxLength ? content.slice(0, maxLength) + '...' : content
})

function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function showDetails() {
  showDialog.value = true
  document.body.style.overflow = 'hidden'
  views.value++
}

function closeDialog() {
  showDialog.value = false
  document.body.style.overflow = 'auto'
}

function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString('en-US', {
    hour: '2-digit',
    minute: '2-digit'
  })
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

function showErrorMsg(msg) {
  errorMsg.value = msg
  errorMsgVisible.value = true
  setTimeout(() => errorMsgVisible.value = false, 3000)
}

async function submitComment() {
  if (!userStore.anonymousName) {
    alert('Please set a nickname before posting a comment')
    return
  }

  if (!userStore.sessionId) {
    alert('Session expired, please refresh the page')
    return
  }

  if (!newComment.value.trim()) {
    alert('Comment content cannot be empty')
    return
  }

  isSubmitting.value = true

  try {
    // AI内容审核
    const filterResult = await filterInappropriateContent(newComment.value.trim())
    if (filterResult.isFlagged) {
      showErrorMsg(`Inappropriate comment: ${filterResult.reason}`)
      isSubmitting.value = false
      return
    }

    const commentData = {
      topicId: props.topic.topicId,
      sessionId: userStore.sessionId,
      content: newComment.value.trim(),
      anonymousName: userStore.anonymousName
    }

    console.log('Submitting comment:', commentData)

    const response = await addComment(commentData)
    console.log('Comment submission successful:', response)

    // Add new comment to list
    comments.value.unshift({
      ...response,
      userHash: userStore.anonymousName,
      timestamp: response.createdAt
    })

    // Clear input field
    newComment.value = ''
    
    // Notify parent component to update comments
    emit('update:comments', comments.value)
  } catch (error) {
    console.error('Comment submission failed:', error)
    alert('Comment submission failed, please try again later')
  } finally {
    isSubmitting.value = false
  }
}

function getAvatar(name) {
  if (!name) return '?'
  return name[0].toUpperCase()
}

onMounted(async () => {
  if (props.topic && props.topic.topicId) {
    try {
      const res = await getComments(props.topic.topicId)
      comments.value = Array.isArray(res) ? res : (res?.comments || [])
    } catch {
      comments.value = []
    }
  }
})
</script>

<style scoped>
.topic-card {
  background: white;
  border-radius: 12px;
  padding: 1.5rem;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  cursor: pointer;
  height: 100%;
  display: flex;
  flex-direction: column;
}

.topic-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 103, 65, 0.2);
}

.card-content {
  flex: 1;
  display: flex;
  flex-direction: column;
}

.card-title {
  color: #4a6741;
  font-size: 1.25rem;
  margin-bottom: 1rem;
  line-height: 1.4;
}

.card-description {
  color: #666;
  font-size: 0.95rem;
  line-height: 1.6;
  margin-bottom: 1.5rem;
  flex: 1;
}

.card-stats {
  display: flex;
  gap: 1rem;
  margin-top: auto;
}

.stat-item button {
  background: none;
  border: none;
  padding: 0.5rem;
  display: flex;
  align-items: center;
  gap: 0.5rem;
  cursor: pointer;
  color: #666;
  transition: all 0.3s ease;
}

.comment-button:hover {
  color: #4a6741;
}

.icon {
  font-size: 1.2rem;
}

.count {
  font-size: 0.9rem;
}

/* Dialog styles */
.dialog-overlay {
  position: fixed;
  top: 0; left: 0; right: 0; bottom: 0;
  background: rgba(0,0,0,0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  padding: 24px;
}
.dialog-content, .comment-page {
  background: #f6f8fa;
  border-radius: 24px;
  box-shadow: 0 8px 40px rgba(0,0,0,0.13);
  max-width: 800px;
  width: 100%;
  min-height: 0;
  display: flex;
  flex-direction: column;
  overflow-y: auto;
  padding: 0;
  gap: 0;
  max-height: 90vh;
  height: 90vh;
  scrollbar-width: none;        /* Firefox */
  -ms-overflow-style: none;     /* IE 10+ */
}
.dialog-content::-webkit-scrollbar,
.comment-page::-webkit-scrollbar {
  display: none;                /* Chrome/Safari/Edge */
}
.dialog-header {
  padding: 20px 24px;
  border-bottom: 1px solid #eee;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: white;
  position: sticky;
  top: 0;
  z-index: 2;
}

.dialog-header h2 {
  margin: 0;
  color: #4a6741;
  font-size: 1.5rem;
}

.close-button {
  position: absolute;
  right: 18px;
  top: 18px;
  width: 36px;
  height: 36px;
  border-radius: 50%;
  background: #f5f5f5;
  color: #333;
  border: none;
  font-size: 1.6rem;
  cursor: pointer;
  z-index: 10;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: background 0.2s, transform 0.3s;
}

.close-button:hover {
  background: #e0e0e0;
  transform: rotate(90deg);
}

.dialog-body {
  padding: 24px;
  overflow-y: auto;
  flex: 1;
}

.topic-detail {
  margin-bottom: 32px;
}

.topic-detail h3 {
  font-size: 1.4rem;
  color: #333;
  margin: 0 0 16px 0;
  line-height: 1.6;
}

.topic-meta {
  display: flex;
  justify-content: space-between;
  align-items: center;
  flex-wrap: wrap;
  gap: 16px;
}

.topic-description {
  margin-top: 20px;
  color: #333;
  line-height: 1.8;
  font-size: 1.1rem;
}

/* Comments section styles */
.comments-section {
  border-top: 1px solid #eee;
  padding-top: 24px;
}

.comments-section h4 {
  color: #4a6741;
  margin: 0 0 20px 0;
  font-size: 1.2rem;
}

.comment-input {
  margin-bottom: 24px;
  position: sticky;
  top: 0;
  background: white;
  padding: 16px;
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
}

.comment-input textarea {
  width: 100%;
  min-height: 100px;
  padding: 16px;
  border: 1px solid #e0e5dd;
  border-radius: 12px;
  resize: vertical;
  font-size: 1rem;
  transition: all 0.3s ease;
}

.comment-input textarea:focus {
  outline: none;
  border-color: #4a6741;
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.1);
}

.comment-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 12px;
}

.char-count {
  color: #666;
  font-size: 0.9rem;
}

.submit-comment-btn {
  background: #4a6741;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.submit-comment-btn:hover:not(:disabled) {
  background: #3a5331;
  transform: translateY(-1px);
}

.submit-comment-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.comments-list {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.no-comments {
  text-align: center;
  color: #666;
  padding: 32px;
  background: #f8f9fa;
  border-radius: 12px;
}

.comment {
  padding: 16px;
  border-radius: 12px;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.comment:hover {
  background: #f0f7ea;
}

.comment-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 12px;
}

.comment-user {
  display: flex;
  align-items: center;
  gap: 8px;
}

.user-avatar {
  width: 32px;
  height: 32px;
  background: linear-gradient(135deg, #4a6741, #6b8f5e);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 0.9rem;
  font-weight: 500;
}

.username {
  color: #4a6741;
  font-weight: 500;
}

.comment-time {
  color: #999;
  font-size: 0.85rem;
}

.comment-text {
  color: #333;
  line-height: 1.6;
  margin: 0 0 12px 0;
}

.comment .comment-actions {
  margin-top: 12px;
  justify-content: flex-start;
  gap: 16px;
}

@keyframes fadeIn {
  from {
    opacity: 0;
    backdrop-filter: blur(0);
  }
  to {
    opacity: 1;
    backdrop-filter: blur(4px);
  }
}

@keyframes slideIn {
  from {
    opacity: 0;
    transform: translateY(30px) translateZ(0);
  }
  to {
    opacity: 1;
    transform: translateY(0) translateZ(0);
  }
}

@media (max-width: 768px) {
  .dialog-overlay {
    padding: 10px;
  }

  .dialog-content {
    width: 100%;
    margin: 10px auto;
    max-height: calc(100vh - 20px);
  }

  .topic-meta {
    flex-direction: column;
    align-items: flex-start;
  }

  .comment-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 8px;
  }

  .comment-time {
    margin-left: 40px;
  }

  .comment-input {
    padding: 12px;
  }

  .comment-input textarea {
    min-height: 80px;
  }
}

.error-message {
  color: #dc3545;
  margin-top: 8px;
  font-size: 0.95rem;
  background: #fff0f0;
  border: 1px solid #ffb3b3;
  border-radius: 6px;
  padding: 8px 16px;
  box-shadow: 0 2px 8px rgba(220,53,69,0.08);
  animation: fadeIn 0.3s;
  transition: opacity 0.5s;
}
.error-message.shake {
  animation: shake 0.4s, fadeIn 0.3s;
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

.topic-card-modern,
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
    border-radius: 0;
  }
  .comment-item-modern {
    padding: 10px 8px;
  }
}
.dialog-content {
  position: relative;
}

/* 完全复刻今日话题详情页评论区气泡背景和滚动体验 */
.comment-page {
  display: flex;
  flex-direction: column;
  gap: 32px;
  padding: 32px 0;
  min-height: 100vh;
  background: #f6f8fa;
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