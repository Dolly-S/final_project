<template>
  <div>
    <!-- Toggle Button -->
    <button
      class="toggle-button"
      @click="toggleChat"
      :class="{ active: isVisible }"
      aria-label="Sara Assistant"
    >
      <span v-if="!isVisible" class="button-icon">💬</span>
      <span v-else class="button-icon">✕</span>
      <span v-if="!isVisible" class="button-text">Sara</span>
    </button>

    <!-- Chat Window -->
    <div v-show="isVisible" class="sara-assistant">
      <div class="sara-header">
        <div class="sara-avatar">
          <span class="avatar-emoji">👩‍⚕️</span>
          <div class="status-dot" :class="{ active: !isLoading }"></div>
        </div>
        <div class="sara-info">
          <h3>Sara Assistant</h3>
          <p class="status">{{ isLoading ? 'Thinking...' : 'Ready to help' }}</p>
        </div>
        <button class="close-button" @click="toggleChat" aria-label="Close">✕</button>
      </div>

      <div class="chat-container" ref="chatContainer">
        <div v-for="(message, index) in chatHistory" :key="index" 
             class="message" :class="message.type">
          <div class="message-content">
            <p v-if="message.type === 'assistant'">
              <TypewriterText :text="message.content" :speed="18" @typing="scrollToBottom" />
            </p>
            <p v-else v-html="formatMessage(message.content)"></p>
            <span class="message-time">{{ formatTime(message.timestamp) }}</span>
          </div>
        </div>
      </div>

      <div class="input-container">
        <div class="input-wrapper" :class="{ 'is-typing': isTyping }">
          <input
            type="text"
            v-model="userInput"
            placeholder="Ask Sara about your arthritis condition..."
            @keyup.enter="sendMessage"
            @focus="isTyping = true"
            @blur="isTyping = false"
          />
          <button 
            class="send-button" 
            @click="sendMessage"
            :disabled="isLoading || !userInput.trim()"
          >
            <span v-if="!isLoading">Send</span>
            <span v-else class="loading-dots">
              <span class="dot"></span>
              <span class="dot"></span>
              <span class="dot"></span>
            </span>
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, nextTick, watch } from 'vue'
import { API_ENDPOINTS } from '@/config/api'
import TypewriterText from '@/components/TypewriterText.vue'

const userInput = ref('')
const isLoading = ref(false)
const isTyping = ref(false)
const isVisible = ref(false)
const chatHistory = ref([
  {
    type: 'assistant',
    content: 'Hi! I\'m Sara, your arthritis care assistant. How can I help you today?',
    timestamp: new Date()
  }
])
const chatContainer = ref(null)

function toggleChat() {
  isVisible.value = !isVisible.value
  if (isVisible.value) {
    nextTick(() => {
      if (chatContainer.value) {
        chatContainer.value.scrollTop = chatContainer.value.scrollHeight
      }
    })
  }
}

function scrollToBottom() {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
}

// Format message, convert line breaks to <br> tags
function formatMessage(message) {
  return message.replace(/\n/g, '<br>')
}

// Format timestamp
function formatTime(timestamp) {
  return new Date(timestamp).toLocaleTimeString([], { 
    hour: '2-digit', 
    minute: '2-digit' 
  })
}

// Send message to Sara API
async function sendMessage() {
  const message = userInput.value.trim()
  if (!message || isLoading.value) return

  // Add user message to chat history
  chatHistory.value.push({
    type: 'user',
    content: message,
    timestamp: new Date()
  })
  scrollToBottom()

  // Clear input and show loading state
  userInput.value = ''
  isLoading.value = true

  try {
    const response = await fetch(API_ENDPOINTS.SARA_CHAT, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json'
      },
      credentials: 'include',
      body: JSON.stringify({ question: message })
    });

    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }

    const data = await response.json();
    let reply;
    
    if (typeof data === 'string') {
      try {
        const parsedData = JSON.parse(data);
        reply = parsedData.reply;
      } catch (parseError) {
        console.error('Error parsing string data:', parseError);
        throw new Error('Invalid data format from server');
      }
    } else if (data && data.body) {
      if (typeof data.body === 'string') {
        try {
          const parsedBody = JSON.parse(data.body);
          reply = parsedBody.reply;
        } catch (parseError) {
          console.error('Error parsing body data:', parseError);
          throw new Error('Invalid data format from server');
        }
      } else {
        reply = data.body.reply || data.body;
      }
    } else {
      reply = data.reply;
    }

    if (!reply) {
      throw new Error('Invalid data format from server');
    }

    // Add Sara's reply to chat history
    chatHistory.value.push({
      type: 'assistant',
      content: reply,
      timestamp: new Date()
    });
  } catch (error) {
    console.error('Error details:', {
      message: error.message,
      stack: error.stack,
      name: error.name,
      cause: error.cause
    });
    
    let errorMessage = 'I apologize, but I encountered an error. ';
    if (error.message.includes('Failed to fetch')) {
      errorMessage += 'Unable to connect to the server. Please check your network connection or try again later.';
    } else if (error.message.includes('502')) {
      errorMessage += 'The server is temporarily unavailable. Please try again later.';
    } else {
      errorMessage += error.message;
    }

    chatHistory.value.push({
      type: 'assistant',
      content: errorMessage,
      timestamp: new Date()
    });
  } finally {
    isLoading.value = false;
  }
}

// Listen for chat history changes, auto scroll to bottom
watch(chatHistory, () => {
  nextTick(() => {
    if (chatContainer.value) {
      chatContainer.value.scrollTop = chatContainer.value.scrollHeight
    }
  })
})
</script>

<style scoped>
.toggle-button {
  position: fixed;
  bottom: 30px;
  right: 30px;
  display: flex;
  align-items: center;
  justify-content: center;
  background-color: #4a6741;
  color: white;
  border: none;
  border-radius: 50px;
  padding: 12px 20px;
  cursor: pointer;
  box-shadow: 0 4px 10px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
  z-index: 1000;
}

.toggle-button:hover {
  background-color: #3a5331;
  transform: translateY(-2px);
  box-shadow: 0 6px 12px rgba(0, 0, 0, 0.2);
}

.toggle-button.active {
  border-radius: 50%;
  padding: 12px;
  background-color: #bf4040;
}

.button-icon {
  font-size: 1.2rem;
  margin-right: 8px;
}

.toggle-button.active .button-icon {
  margin-right: 0;
}

.button-text {
  font-weight: bold;
}

.sara-assistant {
  position: fixed;
  bottom: 30px;
  right: 30px;
  background: #ffffff;
  border-radius: 16px;
  box-shadow: 0 6px 24px rgba(0, 0, 0, 0.15);
  padding: 20px;
  width: 350px;
  height: 500px;
  display: flex;
  flex-direction: column;
  z-index: 1000;
  transition: all 0.3s ease;
  border: 1px solid rgba(0, 0, 0, 0.1);
}

@media (max-width: 500px) {
  .sara-assistant {
    width: calc(100% - 40px);
    height: 400px;
  }
}

.sara-header {
  display: flex;
  align-items: center;
  padding-bottom: 16px;
  border-bottom: 1px solid #eee;
  margin-bottom: 16px;
  position: relative;
}

.sara-avatar {
  position: relative;
  width: 48px;
  height: 48px;
  background: #f0f7ea;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  margin-right: 12px;
}

.avatar-emoji {
  font-size: 24px;
}

.status-dot {
  position: absolute;
  bottom: 2px;
  right: 2px;
  width: 10px;
  height: 10px;
  border-radius: 50%;
  background: #ccc;
  border: 2px solid #fff;
}

.status-dot.active {
  background: #4CAF50;
}

.sara-info h3 {
  margin: 0;
  color: #333;
  font-size: 1.2rem;
}

.status {
  margin: 4px 0 0;
  color: #666;
  font-size: 0.9rem;
}

.close-button {
  position: absolute;
  right: -10px;
  top: -10px;
  width: 28px;
  height: 28px;
  border-radius: 50%;
  background: #bf4040;
  color: white;
  border: none;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 16px;
  transition: all 0.3s ease;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
}

.close-button:hover {
  background: #a33636;
  transform: scale(1.1);
}

.chat-container {
  flex: 1;
  overflow-y: auto;
  padding: 10px;
  margin: -10px;
  margin-bottom: 16px;
}

.message {
  margin-bottom: 16px;
  display: flex;
  flex-direction: column;
}

.message.user {
  align-items: flex-end;
}

.message-content {
  max-width: 80%;
  padding: 12px 16px;
  border-radius: 12px;
  position: relative;
}

.message.assistant .message-content {
  background: #f0f7ea;
  border-bottom-left-radius: 4px;
}

.message.user .message-content {
  background: #4a6741;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-content p {
  margin: 0;
  line-height: 1.5;
}

.message-time {
  font-size: 0.8rem;
  color: #999;
  margin-top: 4px;
}

.message.user .message-time {
  color: rgba(255, 255, 255, 0.7);
}

.input-container {
  margin-top: auto;
  padding-top: 16px;
  border-top: 1px solid #eee;
}

.input-wrapper {
  display: flex;
  gap: 8px;
  background: #f5f5f5;
  border-radius: 24px;
  padding: 4px;
  transition: all 0.3s ease;
}

.input-wrapper.is-typing {
  background: #fff;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.input-wrapper input {
  flex: 1;
  border: none;
  background: none;
  padding: 12px 16px;
  font-size: 1rem;
  outline: none;
  color: #333;
}

.input-wrapper input::placeholder {
  color: #999;
}

.send-button {
  background: #4a6741;
  color: white;
  border: none;
  padding: 8px 20px;
  border-radius: 20px;
  cursor: pointer;
  font-weight: 500;
  transition: all 0.3s ease;
}

.send-button:hover:not(:disabled) {
  background: #3a5331;
}

.send-button:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.loading-dots {
  display: flex;
  align-items: center;
  gap: 4px;
}

.dot {
  width: 4px;
  height: 4px;
  background: white;
  border-radius: 50%;
  animation: bounce 1.4s infinite ease-in-out;
}

.dot:nth-child(1) { animation-delay: -0.32s; }
.dot:nth-child(2) { animation-delay: -0.16s; }

@keyframes bounce {
  0%, 80%, 100% { transform: scale(0); }
  40% { transform: scale(1); }
}

/* Custom scrollbar */
.chat-container::-webkit-scrollbar {
  width: 6px;
}

.chat-container::-webkit-scrollbar-track {
  background: #f1f1f1;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb {
  background: #ccc;
  border-radius: 3px;
}

.chat-container::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style> 