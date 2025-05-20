<template>
  <div class="daily-topic" :class="{ 'loading': isLoading }" @click="showTopicDetails">
    <div class="topic-header">
      <h2>Today's Topic</h2>
      <span class="date">{{ formatDisplayDate(topicDate) }}</span>
    </div>
    
    <div v-if="isLoading" class="loading-state">
      <div class="loading-spinner"></div>
      <p>Loading...</p>
    </div>
    
    <div v-else-if="error" class="error-state">
      {{ error }}
      <button @click="fetchDailyTopic" class="retry-button">Retry</button>
    </div>
    
    <div v-else class="topic-content">
      <div class="topic-main">
        <h3>{{ dailyTopic }}</h3>
        <div class="topic-stats">
          <div class="stat">
            <span class="icon">💬</span>
            <span>{{ comments.length }}</span>
          </div>
          <div class="stat">
            <span class="icon">👁️</span>
            <span>{{ views }}</span>
          </div>
        </div>
      </div>
      <div class="topic-footer">
        <button class="join-discussion-btn">
          <span>Join Discussion</span>
          <span class="arrow">→</span>
        </button>
      </div>
    </div>

    <!-- Topic Details Dialog -->
    <Teleport to="body">
      <div v-if="showDialog" class="dialog-overlay" @click="closeDialog">
        <div class="dialog-content" @click.stop>
          <TodayTopicDetailDialog :topic="todayTopicObj" :comments="comments" @update:comments="comments = $event" />
          <button class="close-button" @click="closeDialog" style="position:absolute;top:16px;right:16px;font-size:2rem;z-index:10;">×</button>
        </div>
      </div>
    </Teleport>
  </div>
</template>

<script setup>
import { ref, onMounted, computed } from 'vue'
import TodayTopicDetailDialog from './TodayTopicDetailDialog.vue'

const dailyTopic = ref('')
const topicDate = ref('')
const isLoading = ref(true)
const error = ref(null)
const showDialog = ref(false)
const comments = ref([])
const views = ref(0)

function formatDisplayDate(dateStr) {
  if (!dateStr) return ''
  
  const [day, month, year] = dateStr.split('/')
  const date = new Date(year, month - 1, day)
  
  return date.toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function getTodaysTopicId() {
  const today = new Date();
  const yyyy = today.getFullYear();
  const mm = String(today.getMonth() + 1).padStart(2, '0');
  const dd = String(today.getDate()).padStart(2, '0');
  return `todays-topic-${yyyy}${mm}${dd}`;
}

function showTopicDetails() {
  showDialog.value = true
  document.body.style.overflow = 'hidden'
  views.value++
}

function closeDialog() {
  showDialog.value = false
  document.body.style.overflow = 'auto'
}

async function fetchDailyTopic() {
  isLoading.value = true
  error.value = null
  
  try {
    console.log('Starting API request...')
    const response = await fetch('https://api.arthritisease.org/topicGenerateDaily/', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      body: JSON.stringify({})
    })

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`)
    }

    const data = await response.json()
    console.log('API response data:', data)
    
    if (!data) {
      throw new Error('Empty API response')
    }

    if (data.topic && data.date) {
      dailyTopic.value = data.topic
      topicDate.value = data.date
      console.log('Topic set successfully:', { topic: dailyTopic.value, date: topicDate.value })
    } else {
      throw new Error('Incomplete topic data')
    }
  } catch (e) {
    console.error('Failed to fetch daily topic:', e)
    error.value = e.message || 'Loading failed, please try again later'
  } finally {
    isLoading.value = false
  }
}

const todayTopicObj = computed(() => {
  return {
    topicId: getTodaysTopicId(),
    title: '今日话题',
    content: dailyTopic.value,
    createdAt: topicDate.value ? new Date(topicDate.value.split('/').reverse().join('-')).toISOString() : new Date().toISOString(),
    anonymousName: '系统'
  }
})

onMounted(() => {
  fetchDailyTopic()
})
</script>

<style scoped>
.daily-topic {
  background: white;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 32px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  cursor: pointer;
  position: relative;
  overflow: hidden;
}

.daily-topic::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #4a6741, #6b8f5e);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.daily-topic:hover {
  transform: translateY(-2px);
  box-shadow: 0 8px 30px rgba(74, 103, 65, 0.15);
}

.daily-topic:hover::before {
  opacity: 1;
}

.topic-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.topic-header h2 {
  color: #4a6741;
  margin: 0;
  font-size: 1.5rem;
  font-weight: 600;
}

.date {
  color: #666;
  font-size: 0.9rem;
  background: #f8f9fa;
  padding: 6px 12px;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 6px;
}

.date::before {
  content: '📅';
}

.topic-content {
  animation: fadeIn 0.5s ease-out;
}

.topic-main {
  margin-bottom: 20px;
}

.topic-main h3 {
  color: #333;
  font-size: 1.2rem;
  line-height: 1.6;
  margin: 0 0 16px 0;
}

.topic-stats {
  display: flex;
  gap: 20px;
}

.stat {
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 0.9rem;
}

.icon {
  font-size: 1.1rem;
}

.topic-footer {
  display: flex;
  justify-content: flex-end;
  margin-top: 16px;
}

.join-discussion-btn {
  background: none;
  border: none;
  color: #4a6741;
  font-size: 0.95rem;
  font-weight: 500;
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 8px 16px;
  border-radius: 20px;
  cursor: pointer;
  transition: all 0.3s ease;
}

.join-discussion-btn:hover {
  background: #f0f7ea;
}

.join-discussion-btn .arrow {
  transition: transform 0.3s ease;
}

.join-discussion-btn:hover .arrow {
  transform: translateX(4px);
}

/* Loading state */
.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 32px;
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid #f3f3f3;
  border-top: 3px solid #4a6741;
  border-radius: 50%;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

/* Dialog styles */
.dialog-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.6);
  display: flex;
  align-items: center;
  justify-content: center;
  z-index: 9999;
  animation: fadeIn 0.3s ease-out;
  overflow-y: auto;
  padding: 20px;
  backdrop-filter: blur(4px);
}

.dialog-content {
  background: white;
  width: 90%;
  max-width: 800px;
  margin: 20px auto;
  border-radius: 16px;
  box-shadow: 0 8px 40px rgba(0, 0, 0, 0.2);
  display: flex;
  flex-direction: column;
  animation: slideIn 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  max-height: calc(100vh - 40px);
  overflow: hidden;
  transform: translateZ(0);
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
  background: none;
  border: none;
  font-size: 1.8rem;
  color: #666;
  cursor: pointer;
  padding: 8px;
  line-height: 1;
  transition: all 0.3s ease;
  border-radius: 50%;
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
}

.close-button:hover {
  color: #4a6741;
  transform: rotate(90deg);
  background: rgba(74, 103, 65, 0.1);
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
  box-shadow: 0 0 0 2px rgba(74, 103, 65, 0.1);
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

.like-button,
.reply-button {
  background: none;
  border: none;
  padding: 6px 12px;
  border-radius: 16px;
  display: flex;
  align-items: center;
  gap: 6px;
  color: #666;
  font-size: 0.9rem;
  cursor: pointer;
  transition: all 0.3s ease;
}

.like-button:hover,
.reply-button:hover {
  background: #e8f0e6;
  color: #4a6741;
}

.like-button.liked {
  color: #4a6741;
  background: #e8f0e6;
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
  .daily-topic {
    padding: 20px;
  }

  .topic-header {
    flex-direction: column;
    align-items: flex-start;
    gap: 12px;
  }

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
</style> 