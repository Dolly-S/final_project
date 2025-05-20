<template>
  <div class="view-container">
    <NavBar />
    <div class="content-wrapper">
      <!-- User Profile Section -->
      <div class="profile-section" v-if="userStore.anonymousName">
        <div class="profile-info">
          <div class="avatar">{{ userStore.anonymousName[0].toUpperCase() }}</div>
          <div class="user-details">
            <span class="username">{{ userStore.anonymousName }}</span>
            <span class="join-date">Member since {{ formatDate(userStore.joinDate) }}</span>
          </div>
        </div>
        <div class="profile-actions">
          <button class="edit-profile-btn" @click="showProfileDialog = true">
            Edit Profile
          </button>
          <button class="new-topic-btn" @click="openNewTopicDialog">
            <span class="plus-icon">+</span>
            New Topic
          </button>
          <button class="new-topic-btn" @click="openQuiz"><span class="gamepad-animate">🎮</span> Quiz Challenge</button>
        </div>
      </div>
      <div class="profile-section" v-else>
        <div class="welcome-message">
          <h3>Welcome to our Community!</h3>
          <p>Join the discussion by setting up your profile.</p>
        </div>
        <div class="profile-actions">
          <button class="setup-profile-btn" @click="showProfileDialog = true">
            Set Up Profile
          </button>
          <button class="new-topic-btn" @click="openNewTopicDialog">
            <span class="plus-icon">+</span>
            New Topic
          </button>
          <button class="new-topic-btn" @click="openQuiz"><span class="gamepad-animate">🎮</span> Quiz Challenge</button>
        </div>
      </div>

      <!-- Main Content -->
      <div class="main-content">
        <!-- Categories -->
        <div class="categories-section">
          <h2>Categories</h2>
          <div class="category-list">
            <button 
              v-for="category in categories" 
              :key="category.id"
              :class="['category-btn', { active: selectedCategory === category.id }]"
              @click="selectCategory(category.id)"
            >
              <span class="category-icon">{{ category.icon }}</span>
              {{ category.name }}
              <span class="topic-count">({{ category.count }})</span>
            </button>
          </div>
        </div>

        <!-- Topics Section -->
        <div class="topics-section">
          <!-- Daily Topic -->
          <div class="section-header">
            <h2>Today's Topic</h2>
            <span class="date">{{ formatDate(new Date()) }}</span>
          </div>
          <DailyTopic class="daily-topic-card" />

          <!-- Recent Topics -->
          <div class="section-header">
            <h2>Recent Discussions</h2>
            <div class="sort-options">
              <select v-model="sortBy">
                <option value="recent">Most Recent</option>
                <option value="popular">Most Popular</option>
                <option value="active">Most Active</option>
              </select>
            </div>
          </div>

          <!-- Topics Grid -->
          <div v-if="isLoading" class="loading-state">
            <div class="loading-spinner"></div>
            <p>{{ LOADING_MESSAGES.TOPICS }}</p>
          </div>
          <div v-else-if="error" class="error-state">
            <p>{{ error }}</p>
            <button @click="fetchTopics">Try Again</button>
          </div>
          <div v-else-if="filteredTopics.length === 0" class="empty-state">
            <p>{{ ERROR_MESSAGES.NO_TOPICS }}</p>
            <button class="new-topic-btn" @click="openNewTopicDialog">
              Start a Discussion
            </button>
          </div>
          <div v-else class="topics-grid">
            <TopicCard
              v-for="topic in filteredTopics"
              :key="topic.id"
              :topic="topic"
              @update:comments="updateTopicComments(topic.id, $event)"
            />
          </div>

          <!-- Pagination -->
          <div class="pagination" v-if="totalPages > 1">
            <button 
              class="page-btn"
              :disabled="currentPage === 1"
              @click="currentPage--"
            >
              <span class="arrow">←</span> Previous
            </button>
            <div class="page-numbers">
              <button 
                v-for="page in displayedPages"
                :key="page"
                :class="['page-number', { active: currentPage === page }]"
                @click="currentPage = page"
              >
                {{ page }}
              </button>
            </div>
            <button 
              class="page-btn"
              :disabled="currentPage === totalPages"
              @click="currentPage++"
            >
              Next <span class="arrow">→</span>
            </button>
          </div>
        </div>
      </div>
    </div>

    <!-- Dialogs -->
    <ProfileDialog 
      v-if="showProfileDialog"
      v-model:show="showProfileDialog"
      :is-edit="!!userStore.anonymousName"
    />
    <NewTopicDialog
      v-model:show="showNewTopicDialog"
      @topic-created="handleTopicCreated"
    />
    <QuizDialog :show="showQuiz" @close="closeQuiz" />
    <AppFooter />
  </div>
</template>

<script setup>
import { ref, computed, onMounted, watch } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { API_ENDPOINTS } from '@/config/api'
import NavBar from '@/components/NavBar.vue'
import DailyTopic from '@/components/DailyTopic.vue'
import TopicCard from '@/components/TopicCard.vue'
import ProfileDialog from '@/components/ProfileDialog.vue'
import NewTopicDialog from '@/components/NewTopicDialog.vue'
import AppFooter from '@/components/AppFooter.vue'
import QuizDialog from '@/components/QuizDialog.vue'

const userStore = useUserStore()
const topics = ref([])
const isLoading = ref(true)
const error = ref(null)
const currentPage = ref(1)
const pageSize = 9
const searchQuery = ref('')
const sortBy = ref('recent')
const selectedCategory = ref(null)
const showProfileDialog = ref(false)
const showNewTopicDialog = ref(false)
const showQuiz = ref(false)

// Categories data
const categories = [
  { id: 'general', name: 'General Discussion', icon: '💭', count: 0 },
  { id: 'exercise', name: 'Exercise Tips', icon: '🏃', count: 0 },
  { id: 'diet', name: 'Diet & Nutrition', icon: '🥗', count: 0 },
  { id: 'medication', name: 'Medication', icon: '💊', count: 0 },
  { id: 'lifestyle', name: 'Lifestyle', icon: '🌟', count: 0 },
  { id: 'success', name: 'Success Stories', icon: '🌈', count: 0 },
  { id: 'research', name: 'Research & News', icon: '📚', count: 0 },
  { id: 'support', name: 'Support Group', icon: '🤝', count: 0 }
]

// Error messages
const ERROR_MESSAGES = {
  FETCH_FAILED: 'Failed to load topics. Please try again.',
  NETWORK_ERROR: 'Network connection error. Please check your connection.',
  SERVER_ERROR: 'Server error occurred. Please try again later.',
  NO_TOPICS: 'No topics found. Be the first to start a discussion!',
  INVALID_SESSION: 'Your session has expired. Please refresh the page.',
  UNAUTHORIZED: 'Please log in to perform this action.',
  TOPIC_CREATE_FAILED: 'Failed to create topic. Please try again.',
  PROFILE_UPDATE_FAILED: 'Failed to update profile. Please try again.'
}

// Loading states
const LOADING_MESSAGES = {
  TOPICS: 'Loading discussions...',
  COMMENTS: 'Loading comments...',
  PROFILE: 'Loading profile...',
  CREATING_TOPIC: 'Creating topic...',
  UPDATING_PROFILE: 'Updating profile...'
}

// Success messages
const SUCCESS_MESSAGES = {
  TOPIC_CREATED: 'Topic created successfully!',
  PROFILE_UPDATED: 'Profile updated successfully!',
  COMMENT_ADDED: 'Comment added successfully!',
  LIKE_ADDED: 'Like added successfully!',
  LIKE_REMOVED: 'Like removed successfully!'
}

// Computed properties
const filteredTopics = computed(() => {
  let result = [...topics.value]
  
  // Apply category filter
  if (selectedCategory.value) {
    result = result.filter(topic => topic.category === selectedCategory.value)
  }
  
  // Apply search filter
  if (searchQuery.value) {
    const query = searchQuery.value.toLowerCase()
    result = result.filter(topic => 
      topic.title.toLowerCase().includes(query) ||
      topic.description.toLowerCase().includes(query)
    )
  }
  
  // Apply sorting
  switch (sortBy.value) {
    case 'popular':
      result.sort((a, b) => b.likes - a.likes)
      break
    case 'active':
      result.sort((a, b) => b.comments.length - a.comments.length)
      break
    default:
      result.sort((a, b) => new Date(b.createdAt) - new Date(a.createdAt))
  }
  
  return result
})

const totalPages = computed(() => Math.ceil(filteredTopics.value.length / pageSize))

const displayedPages = computed(() => {
  const total = totalPages.value
  const current = currentPage.value
  const pages = []
  
  if (total <= 7) {
    for (let i = 1; i <= total; i++) pages.push(i)
  } else {
    if (current <= 3) {
      for (let i = 1; i <= 5; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    } else if (current >= total - 2) {
      pages.push(1)
      pages.push('...')
      for (let i = total - 4; i <= total; i++) pages.push(i)
    } else {
      pages.push(1)
      pages.push('...')
      for (let i = current - 1; i <= current + 1; i++) pages.push(i)
      pages.push('...')
      pages.push(total)
    }
  }
  
  return pages
})

// Methods
function formatDate(date) {
  return new Date(date).toLocaleDateString('en-US', {
    year: 'numeric',
    month: 'long',
    day: 'numeric'
  })
}

function selectCategory(categoryId) {
  selectedCategory.value = selectedCategory.value === categoryId ? null : categoryId
}

async function fetchTopics() {
  isLoading.value = true
  error.value = null
  
  try {
    const response = await fetch(API_ENDPOINTS.TOPICS)
    if (!response.ok) {
      throw new Error(ERROR_MESSAGES.FETCH_FAILED)
    }
    
    const data = await response.json()
    topics.value = data
    
    // Update category counts
    categories.forEach(category => {
      category.count = topics.value.filter(topic => topic.category === category.id).length
    })
  } catch (err) {
    console.error('Error fetching topics:', err)
    error.value = err.message.includes('fetch') 
      ? ERROR_MESSAGES.NETWORK_ERROR 
      : ERROR_MESSAGES.SERVER_ERROR
  } finally {
    isLoading.value = false
  }
}

function handleTopicCreated(newTopic) {
  topics.value.unshift(newTopic)
  const category = categories.find(c => c.id === newTopic.category)
  if (category) {
    category.count++
  }
  showNewTopicDialog.value = false
  // Show success message
  alert(SUCCESS_MESSAGES.TOPIC_CREATED)
}

function updateTopicComments(topicId, newComments) {
  const topic = topics.value.find(t => t.id === topicId)
  if (topic) {
    topic.comments = newComments
  }
}

// Watch changes
watch([currentPage, sortBy, selectedCategory], () => {
  fetchTopics()
})

onMounted(() => {
  // Auto-assign anonymous username if missing
  if (!userStore.anonymousName) {
    userStore.resetAnonymousName()
  }
  // Auto-assign sessionId if missing
  if (!userStore.sessionId) {
    userStore.resetSession()
  }
  console.log('CommunityView mounted')
  fetchTopics()
})

// 打开新话题对话框
function openNewTopicDialog() {
  showNewTopicDialog.value = true
}

function openQuiz() {
  showQuiz.value = true
}

function closeQuiz() {
  showQuiz.value = false
}
</script>

<style scoped>
.view-container {
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ea 0%, #ffffff 50%, #e8f3e0 100%);
  position: relative;
  overflow: hidden;
}

.view-container::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(74, 103, 65, 0.05) 0%, transparent 60%);
  animation: rotate 30s linear infinite;
}

@keyframes rotate {
  from { transform: rotate(0deg); }
  to { transform: rotate(360deg); }
}

.content-wrapper {
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  animation: fadeIn 0.8s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  z-index: 1;
}

.header-actions {
  display: flex;
  gap: 2rem;
  align-items: center;
}

.new-topic-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  background: linear-gradient(135deg, #4a6741 0%, #6b8f5e 100%);
  backdrop-filter: blur(8px);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 4px 16px rgba(74, 103, 65, 0.15);
  color: white;
  border: none;
  padding: 0.65rem 1.2rem;
  border-radius: 12px;
  font-size: 0.95rem;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  transform-origin: center;
  overflow: hidden;
  position: relative;
}

.new-topic-btn:hover {
  transform: scale(1.05) translateY(-2px);
  box-shadow: 0 8px 24px rgba(74, 103, 65, 0.2);
}

.plus-icon {
  font-size: 1.2rem;
  font-weight: bold;
  transition: transform 0.3s ease;
}

.new-topic-btn:hover .plus-icon {
  transform: rotate(90deg);
}

.profile-section {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(74, 103, 65, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  margin-bottom: 2rem;
  display: flex;
  justify-content: space-between;
  align-items: center;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.profile-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 4px;
  background: linear-gradient(90deg, #4a6741, #6b8f5e);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.profile-section:hover::before {
  opacity: 1;
}

.profile-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.profile-info {
  display: flex;
  align-items: center;
  gap: 1.5rem;
}

.avatar {
  width: 56px;
  height: 56px;
  background: linear-gradient(135deg, #4a6741 0%, #6b8f5e 100%);
  color: white;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 1.5rem;
  font-weight: 600;
  transition: all 0.3s ease;
  box-shadow: 0 8px 24px rgba(74, 103, 65, 0.2);
  transform-origin: center;
}

.profile-section:hover .avatar {
  transform: scale(1.1) rotate(10deg);
  transition: transform 0.6s cubic-bezier(0.34, 1.56, 0.64, 1);
}

.user-details {
  display: flex;
  flex-direction: column;
}

.username {
  font-size: 1.2rem;
  font-weight: 600;
  color: #333;
  margin-bottom: 0.25rem;
}

.join-date {
  font-size: 0.9rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.join-date::before {
  content: '🎉';
  font-size: 1rem;
}

.welcome-message {
  flex: 1;
}

.welcome-message h3 {
  margin: 0 0 0.5rem 0;
  color: #333;
  font-size: 1.3rem;
}

.welcome-message p {
  margin: 0;
  color: #666;
  line-height: 1.5;
}

.edit-profile-btn,
.setup-profile-btn {
  background: transparent;
  border: 2px solid #4a6741;
  color: #4a6741;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  font-weight: 500;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
}

.edit-profile-btn::before,
.setup-profile-btn::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(74, 103, 65, 0.1);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
}

.edit-profile-btn:hover::before,
.setup-profile-btn:hover::before {
  width: 300px;
  height: 300px;
}

.edit-profile-btn:hover,
.setup-profile-btn:hover {
  background: #4a6741;
  color: white;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 103, 65, 0.2);
}

.main-content {
  display: grid;
  grid-template-columns: 250px 1fr;
  gap: 2rem;
  animation: slideUp 0.5s ease-out;
}

@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(40px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

.categories-section {
  backdrop-filter: blur(10px);
  background: rgba(255, 255, 255, 0.8);
  border: 1px solid rgba(255, 255, 255, 0.2);
  box-shadow: 0 8px 32px rgba(74, 103, 65, 0.1);
  border-radius: 16px;
  padding: 1.5rem;
  height: fit-content;
  transition: all 0.3s ease;
  position: sticky;
  top: 2rem;
}

.categories-section:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.12);
}

.categories-section h2 {
  margin: 0 0 1.5rem 0;
  font-size: 1.2rem;
  color: #333;
  position: relative;
  padding-bottom: 0.5rem;
}

.categories-section h2::after {
  content: '';
  position: absolute;
  bottom: 0;
  left: 0;
  width: 40px;
  height: 3px;
  background: linear-gradient(90deg, #4a6741, #6b8f5e);
  border-radius: 2px;
  transition: width 0.3s ease;
}

.categories-section:hover h2::after {
  width: 60px;
}

.category-list {
  display: flex;
  flex-direction: column;
  gap: 0.75rem;
}

.category-btn {
  display: flex;
  align-items: center;
  gap: 0.75rem;
  padding: 0.75rem 1rem;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: #666;
  font-size: 0.95rem;
  cursor: pointer;
  transition: all 0.3s ease;
  text-align: left;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.05);
}

.category-btn::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  width: 4px;
  height: 100%;
  background: linear-gradient(135deg, #4a6741, #6b8f5e);
  opacity: 0;
  transition: all 0.3s ease;
}

.category-btn:hover::before,
.category-btn.active::before {
  opacity: 1;
}

.category-btn:hover {
  background: rgba(74, 103, 65, 0.1);
  color: #4a6741;
  padding-left: 1.5rem;
  transform: translateX(8px);
}

.category-btn.active {
  background: rgba(74, 103, 65, 0.1);
  color: #4a6741;
  font-weight: 500;
  padding-left: 1.5rem;
}

.category-icon {
  font-size: 1.2rem;
  transition: transform 0.3s ease;
}

.category-btn:hover .category-icon {
  transform: scale(1.2);
}

.topic-count {
  margin-left: auto;
  font-size: 0.85rem;
  color: #999;
  background: #f8f9fa;
  padding: 0.25rem 0.5rem;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.category-btn:hover .topic-count {
  background: #e8f0e6;
  color: #4a6741;
}

.topics-section {
  flex: 1;
  animation: fadeIn 0.5s ease-out;
}

.section-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.5rem;
  position: relative;
}

.section-header h2 {
  margin: 0;
  font-size: 1.3rem;
  color: #333;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.section-header h2::before {
  content: '📝';
  font-size: 1.4rem;
}

.date {
  color: #666;
  font-size: 0.9rem;
  background: #f8f9fa;
  padding: 0.5rem 1rem;
  border-radius: 20px;
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.date::before {
  content: '📅';
}

.sort-options select {
  padding: 0.75rem 2.5rem 0.75rem 1rem;
  border: 2px solid #e0e5dd;
  border-radius: 12px;
  font-size: 0.95rem;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  background: white url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='24' height='24' viewBox='0 0 24 24' fill='none' stroke='%23666' stroke-width='2' stroke-linecap='round' stroke-linejoin='round'%3E%3Cpolyline points='6 9 12 15 18 9'%3E%3C/polyline%3E%3C/svg%3E") no-repeat right 0.75rem center;
  background-size: 1rem;
  appearance: none;
}

.sort-options select:hover,
.sort-options select:focus {
  border-color: #4a6741;
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.1);
  outline: none;
}

.daily-topic-card {
  margin-bottom: 2rem;
  transition: all 0.3s ease;
  animation: float 6s ease-in-out infinite;
}

.daily-topic-card:hover {
  transform: translateY(-2px);
}

.topics-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(320px, 1fr));
  gap: 2rem;
  perspective: 1000px;
}

.topics-grid > * {
  animation: cardEntrance 0.8s cubic-bezier(0.34, 1.56, 0.64, 1) forwards;
  transform-origin: center;
}

@keyframes cardEntrance {
  from {
    opacity: 0;
    transform: scale(0.9) translateY(20px) rotateX(-10deg);
  }
  to {
    opacity: 1;
    transform: scale(1) translateY(0) rotateX(0);
  }
}

.loading-state {
  display: flex;
  flex-direction: column;
  align-items: center;
  padding: 3rem;
  background: white;
  border-radius: 16px;
  box-shadow: 0 4px 16px rgba(0, 0, 0, 0.08);
  animation: pulse 2s ease-in-out infinite;
}

.loading-spinner {
  width: 60px;
  height: 60px;
  border: 4px solid rgba(74, 103, 65, 0.1);
  border-top: 4px solid #4a6741;
  border-radius: 50%;
  animation: spin 1s cubic-bezier(0.68, -0.55, 0.265, 1.55) infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.error-state {
  text-align: center;
  padding: 2rem;
  background: #fff5f5;
  border-radius: 16px;
  color: #dc3545;
  animation: shake 0.5s ease-in-out;
}

@keyframes shake {
  0%, 100% { transform: translateX(0); }
  25% { transform: translateX(-10px); }
  75% { transform: translateX(10px); }
}

.error-state button {
  background: linear-gradient(45deg, #4a6741, #6b8f5e);
  color: white;
  border: none;
  padding: 0.75rem 1.5rem;
  border-radius: 12px;
  margin-top: 1rem;
  cursor: pointer;
  transition: all 0.3s ease;
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.2);
}

.error-state button:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 103, 65, 0.3);
}

.pagination {
  display: flex;
  justify-content: center;
  align-items: center;
  gap: 1rem;
  margin-top: 2rem;
}

.page-btn {
  display: flex;
  align-items: center;
  gap: 0.5rem;
  padding: 0.75rem 1.5rem;
  border: none;
  border-radius: 12px;
  background: linear-gradient(135deg, #4a6741 0%, #6b8f5e 100%);
  backdrop-filter: blur(8px);
  box-shadow: 0 4px 16px rgba(74, 103, 65, 0.15);
  color: white;
  cursor: pointer;
  transition: all 0.3s ease;
}

.page-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  background: #ccc;
  box-shadow: none;
}

.page-btn:not(:disabled):hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(74, 103, 65, 0.3);
}

.page-numbers {
  display: flex;
  gap: 0.75rem;
}

.page-number {
  width: 40px;
  height: 40px;
  display: flex;
  align-items: center;
  justify-content: center;
  border: none;
  border-radius: 12px;
  background: transparent;
  color: #666;
  cursor: pointer;
  transition: all 0.3s ease;
  position: relative;
  overflow: hidden;
  backdrop-filter: blur(8px);
  background: rgba(255, 255, 255, 0.6);
  border: 1px solid rgba(255, 255, 255, 0.1);
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.05);
}

.page-number::before {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(74, 103, 65, 0.1);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  transition: width 0.6s ease, height 0.6s ease;
}

.page-number:hover::before {
  width: 80px;
  height: 80px;
}

.page-number:hover:not(.active) {
  color: #4a6741;
}

.page-number.active {
  background: linear-gradient(135deg, #4a6741 0%, #6b8f5e 100%);
  color: white;
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.2);
}

@media (max-width: 1024px) {
  .main-content {
    grid-template-columns: 1fr;
  }

  .categories-section {
    position: static;
    margin-bottom: 2rem;
  }

  .category-list {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 0.75rem;
  }
}

@media (max-width: 768px) {
  .content-wrapper {
    padding: 1rem;
  }

  .page-header {
    flex-direction: column;
    gap: 1.5rem;
    align-items: stretch;
    text-align: center;
    padding: 1.5rem;
  }

  .header-actions {
    margin-left: 0;
    margin-top: 1rem;
    width: 100%;
  }

  .profile-section {
    flex-direction: column;
    gap: 1.5rem;
    text-align: center;
  }

  .profile-info {
    flex-direction: column;
  }

  .avatar {
    margin: 0 auto;
  }

  .topics-grid {
    gap: 1.5rem;
  }

  .page-numbers {
    display: none;
  }

  .section-header {
    flex-direction: column;
    gap: 1rem;
    align-items: stretch;
  }

  .sort-options select {
    width: 100%;
  }

  .container {
    padding: 1rem;
    margin: 0;
  }

  h1 {
    font-size: 2rem;
  }
}

@keyframes fadeInUp {
  from {
    opacity: 0;
    transform: translateY(20px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}

@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.9);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}

.fade-enter-active,
.fade-leave-active {
  transition: opacity 0.3s ease;
}

.fade-enter-from,
.fade-leave-to {
  opacity: 0;
}

.hover-lift {
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.hover-lift:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

::-webkit-scrollbar {
  width: 10px;
}

::-webkit-scrollbar-track {
  background: rgba(255, 255, 255, 0.6);
  backdrop-filter: blur(8px);
}

::-webkit-scrollbar-thumb {
  background: linear-gradient(135deg, #4a6741 0%, #6b8f5e 100%);
  border-radius: 5px;
  border: 2px solid rgba(255, 255, 255, 0.6);
}

::-webkit-scrollbar-thumb:hover {
  background: linear-gradient(135deg, #3a5331 0%, #4a6741 100%);
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-10px); }
  100% { transform: translateY(0px); }
}

.new-topic-btn::after,
.page-btn::after {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(circle at center, rgba(255, 255, 255, 0.2) 0%, transparent 60%);
  opacity: 0;
  transition: opacity 0.3s ease;
}

.new-topic-btn:hover::after,
.page-btn:hover::after {
  opacity: 1;
}

@keyframes pulse {
  0% { transform: scale(1); opacity: 1; }
  50% { transform: scale(1.1); opacity: 0.7; }
  100% { transform: scale(1); opacity: 1; }
}

.loading-state {
  animation: pulse 2s ease-in-out infinite;
}

.container {
  max-width: 1200px;
  margin: 0;
  padding: 2rem 1rem;
  flex: 1;
}

.back-link {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}

.quiz-btn {
  background: #4a6741;
  color: #fff;
  border: none;
  padding: 10px 24px;
  border-radius: 8px;
  font-size: 1.1rem;
  margin-left: 16px;
  cursor: pointer;
}

.quiz-btn:hover {
  background: #3a5331;
}

@keyframes gamepadWobble {
  0%   { transform: rotate(0deg) scale(1);}
  20%  { transform: rotate(-12deg) scale(1.08);}
  40%  { transform: rotate(10deg) scale(1.12);}
  60%  { transform: rotate(-8deg) scale(1.08);}
  80%  { transform: rotate(8deg) scale(1.05);}
  100% { transform: rotate(0deg) scale(1);}
}

.gamepad-animate {
  display: inline-flex;
  animation: gamepadWobble 1.6s infinite cubic-bezier(.68,-0.55,.27,1.55);
  will-change: transform;
}

.profile-actions {
  display: flex;
  align-items: center;
  gap: 1.2rem;
}
</style> 