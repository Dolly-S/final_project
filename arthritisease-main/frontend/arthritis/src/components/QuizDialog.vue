<template>
  <div class="quiz-dialog-bg" v-if="show">
    <div class="quiz-card">
      <button class="close-btn" @click="close">×</button>
      <!-- 欢迎页 -->
      <transition name="fade">
        <div v-if="step==='welcome'" key="welcome" class="quiz-welcome">
          <h2 class="quiz-title-anim">🎯 Quiz Challenge</h2>
          <p class="desc">10 questions, race against time!<br>Can you beat most players?</p>
          <button class="start-btn" @click="startGame" :disabled="loading">Start Game</button>
        </div>
      </transition>
      <!-- 答题页 -->
      <transition name="slide-fade" mode="out-in">
        <div v-if="step==='question'" key="question" class="quiz-main">
          <QuizProgress :percent="progressPercent" :timeLeft="timeLeft" />
          <div class="quiz-q-header">
            <span class="quiz-q-index">Q{{ currentIndex+1 }}/{{ questions.length }}</span>
          </div>
          <transition name="zoom-fade" mode="out-in">
            <div :key="currentIndex" class="quiz-question-card">
              <div class="quiz-question">{{ currentQuestion.question }}</div>
              <div class="quiz-options">
                <button v-for="(opt, idx) in currentQuestion.options" :key="idx"
                  :class="optionClass(idx)"
                  @click="choose(idx)"
                  :disabled="answered"
                >
                  <span class="opt-label">{{ String.fromCharCode(65+idx) }}</span>
                  {{ opt }}
                  <span v-if="answered && currentQuestion.options && currentQuestion.options[idx] === currentQuestion.answer" class="icon-correct">✔</span>
                  <span v-if="answered && userAnswers[currentIndex] === idx && currentQuestion.options && currentQuestion.options[idx] !== currentQuestion.answer" class="icon-wrong">✖</span>
                </button>
              </div>
            </div>
          </transition>
        </div>
      </transition>
      <!-- 结算页 -->
      <transition name="fade">
        <div v-if="step==='result'" key="result" class="quiz-result-wrap">
          <div class="quiz-result">
            <h2>Quiz Finished!</h2>
            <div class="result-anim">
              <span class="score">
                ⏱ <span class="num-anim">{{ elapsed }}</span>s
              </span>
              <span class="beat">
                🏆 Beat <span class="num-anim">{{ beatPercentage }}</span>% players!
              </span>
              <span class="rate">
                🎯 Correct Rate: <span class="num-anim">{{ correctRate }}</span>%
              </span>
            </div>
            <button class="restart-btn" @click="restart">Try Again</button>
            <button class="close-btn2" @click="close">Close</button>
          </div>
        </div>
      </transition>
      <div class="fireworks-canvas-wrap-global" v-if="showFireworks">
        <canvas ref="fireworksCanvas" class="fireworks-canvas-global"></canvas>
      </div>
      <div v-if="loading" class="quiz-loading"><span class="loader"></span> Loading...</div>
      <div v-if="error" class="quiz-error">{{ error }}</div>
    </div>
  </div>
</template>

<script setup>
import { ref, computed, watch, nextTick, onUnmounted, onMounted } from 'vue'
import QuizProgress from './QuizProgress.vue'

const props = defineProps({
  show: Boolean
})
const emit = defineEmits(['close'])

const step = ref('welcome') // welcome | question | result
const currentIndex = ref(0)
const userAnswers = ref([])
const answered = ref(false)
const timeLeft = ref(15)
const timer = ref(null)
const loading = ref(false)
const error = ref('')
const elapsed = ref(0)
const showFireworks = ref(false)
const beatPercentage = ref(0)
const correctRate = ref(0)

const questions = ref([])

const progressPercent = computed(() => ((currentIndex.value) / questions.value.length) * 100)
const currentQuestion = computed(() => questions.value[currentIndex.value] || {})

const fireworksCanvas = ref(null)
let fireworksTimer = null
let particles = []
let fireworksEndTimer = null

function randomFireworkType() {
  const types = ['circle', 'heart', 'star']
  return types[Math.floor(Math.random() * types.length)]
}

function launchFirework(x, y, type) {
  const canvas = fireworksCanvas.value
  if (!canvas) return
  const width = canvas.width = window.innerWidth
  const height = canvas.height = window.innerHeight
  const centerX = x !== undefined ? x : width / 2
  const centerY = y !== undefined ? y : height / 2
  const colorBase = Math.random() * 360
  let count = 36
  if (type === 'star') count = 10
  if (type === 'heart') count = 40
  for (let i = 0; i < count; i++) {
    let angle, speed, vx, vy
    if (type === 'circle') {
      angle = (Math.PI * 2 / count) * i
      speed = 0.8 + Math.random() * 1.0
      vx = Math.cos(angle) * speed
      vy = Math.sin(angle) * speed
    } else if (type === 'heart') {
      // 心形参数方程
      const t = (Math.PI * 2 / count) * i
      vx = 16 * Math.pow(Math.sin(t), 3) * 0.7
      vy = -(13 * Math.cos(t) - 5 * Math.cos(2 * t) - 2 * Math.cos(3 * t) - Math.cos(4 * t)) * 0.7
      vx += (Math.random() - 0.5) * 2
      vy += (Math.random() - 0.5) * 2
    } else if (type === 'star') {
      // 五角星
      angle = (Math.PI * 2 / count) * i
      const r = i % 2 === 0 ? 1.5 : 0.7
      speed = 1.0 + Math.random() * 0.7
      vx = Math.cos(angle) * speed * r
      vy = Math.sin(angle) * speed * r
    }
    particles.push({
      x: centerX,
      y: centerY,
      vx,
      vy,
      alpha: 1,
      color: `hsl(${colorBase + i * 10}, 90%, 60%)`,
      size: 4 + Math.random() * 2,
      gravity: 0.03 + Math.random() * 0.015
    })
  }
}

function drawFireworksAnim() {
  const canvas = fireworksCanvas.value
  if (!canvas) return
  const ctx = canvas.getContext('2d')
  const width = canvas.width = window.innerWidth
  const height = canvas.height = window.innerHeight
  ctx.clearRect(0, 0, width, height)
  particles.forEach(p => {
    ctx.save()
    ctx.globalAlpha = p.alpha
    ctx.beginPath()
    ctx.arc(p.x, p.y, p.size, 0, Math.PI * 2)
    ctx.fillStyle = p.color
    ctx.shadowColor = p.color
    ctx.shadowBlur = 18
    ctx.fill()
    ctx.restore()
    p.x += p.vx
    p.y += p.vy
    p.vy += p.gravity
    p.alpha -= 0.0025 + Math.random() * 0.0015
  })
  particles = particles.filter(p => p.alpha > 0)
  if (particles.length > 0) {
    fireworksTimer = requestAnimationFrame(drawFireworksAnim)
  }
}

function startFireworksAnim() {
  particles = []
  const canvas = fireworksCanvas.value
  if (!canvas) return
  const width = window.innerWidth
  const height = window.innerHeight
  let count = 0
  const maxCount = 12 // 增加烟花数量
  function multiLaunch() {
    const x = width * (0.15 + 0.7 * Math.random())
    const y = height * (0.15 + 0.4 * Math.random())
    launchFirework(x, y, randomFireworkType())
    count++
    if (count < maxCount) {
      setTimeout(multiLaunch, 520)
    }
  }
  multiLaunch()
  fireworksTimer = requestAnimationFrame(drawFireworksAnim)
  // 持续3.5秒后自动停止
  clearTimeout(fireworksEndTimer)
  fireworksEndTimer = setTimeout(() => {
    stopFireworksAnim()
    showFireworks.value = false
  }, 5000)
}

function stopFireworksAnim() {
  if (fireworksTimer) cancelAnimationFrame(fireworksTimer)
  fireworksTimer = null
  particles = []
  if (fireworksCanvas.value) {
    const ctx = fireworksCanvas.value.getContext('2d')
    ctx && ctx.clearRect(0, 0, fireworksCanvas.value.width, fireworksCanvas.value.height)
  }
  clearTimeout(fireworksEndTimer)
}

async function getQuizQuestions() {
  loading.value = true
  error.value = ''
  try {
    const res = await fetch('https://api.arthritisease.org/quiz', { method: 'POST' })
    const data = await res.json()
    // 兼容 body 为字符串的情况
    let bodyObj = data
    if (typeof data.body === 'string') {
      bodyObj = JSON.parse(data.body)
    }
    questions.value = bodyObj.questions || []
  } catch {
    error.value = 'Failed to load quiz questions.'
    questions.value = []
  } finally {
    loading.value = false
  }
}

function close() {
  emit('close')
  reset()
}
async function startGame() {
  loading.value = true
  error.value = ''
  await getQuizQuestions()
  step.value = 'question'
  currentIndex.value = 0
  userAnswers.value = []
  answered.value = false
  timeLeft.value = 15
  elapsed.value = 0
  error.value = ''
  loading.value = false
  nextTick(startTimer)
}
function startTimer() {
  clearInterval(timer.value)
  timer.value = setInterval(() => {
    timeLeft.value--
    elapsed.value++
    if (timeLeft.value <= 0) {
      choose(-1)
    }
  }, 1000)
}
function choose(idx) {
  if (answered.value) return
  answered.value = true
  userAnswers.value[currentIndex.value] = idx
  clearInterval(timer.value)
  setTimeout(() => {
    next()
  }, 800)
}
function optionClass(idx) {
  if (!answered.value) return 'quiz-opt'
  // 用内容比对
  if (currentQuestion.value.options && currentQuestion.value.options[idx] === currentQuestion.value.answer) return 'quiz-opt correct'
  if (userAnswers.value[currentIndex.value] === idx) return 'quiz-opt wrong'
  return 'quiz-opt'
}
function next() {
  answered.value = false
  timeLeft.value = 15
  if (currentIndex.value < questions.value.length - 1) {
    currentIndex.value++
    nextTick(startTimer)
  } else {
    finish()
  }
}
function finish() {
  step.value = 'result'
  clearInterval(timer.value)
  // 计算分数和排名
  let correct = 0
  questions.value.forEach((q, i) => {
    if (q.options && q.options[userAnswers.value[i]] === q.answer) correct++
  })
  correctRate.value = questions.value.length > 0 ? ((correct / questions.value.length) * 100).toFixed(1) : 0
  // 假设 beat 百分比为正确题数/总题数*80+随机10-15
  beatPercentage.value = Math.min(100, Math.round((correct / questions.value.length) * 80 + 10 + Math.random() * 5))
  showFireworks.value = correct >= 0
  nextTick(() => setTimeout(startFireworksAnim, 500))
}
function restart() {
  step.value = 'welcome'
  reset()
}
function reset() {
  clearInterval(timer.value)
  currentIndex.value = 0
  userAnswers.value = []
  answered.value = false
  timeLeft.value = 15
  elapsed.value = 0
  error.value = ''
  showFireworks.value = false
  beatPercentage.value = 0
  step.value = 'welcome'
}

watch(() => props.show, (val) => {
  if (val) {
    reset()
    // 不再自动加载题目，等Start Game点击时再加载
  }
})

watch(() => step.value, (val) => {
  if (val === 'result') {
    nextTick(() => setTimeout(startFireworksAnim, 500))
  } else {
    stopFireworksAnim()
  }
})

onMounted(() => {
  // 监听窗口变化，自动调整canvas大小
  function resizeCanvas() {
    if (fireworksCanvas.value) {
      fireworksCanvas.value.width = window.innerWidth
      fireworksCanvas.value.height = window.innerHeight
    }
  }
  window.addEventListener('resize', resizeCanvas)
  resizeCanvas()
})

onUnmounted(stopFireworksAnim)
</script>

<style scoped>
.quiz-dialog-bg {
  position: fixed;
  z-index: 9999;
  inset: 0;
  background: rgba(30, 41, 59, 0.75);
  display: flex;
  align-items: center;
  justify-content: center;
  animation: fadeInBg 0.3s;
}
@keyframes fadeInBg {
  from { opacity: 0; }
  to { opacity: 1; }
}
.quiz-card {
  background: linear-gradient(135deg, #f0fdfa 0%, #e0e7ff 100%);
  border-radius: 2.2rem;
  box-shadow: 0 8px 32px 0 rgba(31, 41, 55, 0.18);
  min-width: 420px;
  max-width: 98vw;
  width: 520px;
  padding: 3.2rem 2.8rem 2.8rem 2.8rem;
  position: relative;
  z-index: 10001;
  overflow: visible;
  animation: popIn 0.4s cubic-bezier(.68,-0.55,.27,1.55);
}
@keyframes popIn {
  0% { transform: scale(0.7); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.close-btn, .close-btn2 {
  position: absolute;
  right: 1.2rem;
  top: 1.2rem;
  background: none;
  border: none;
  font-size: 2rem;
  color: #64748b;
  cursor: pointer;
  transition: transform 0.2s;
}
.close-btn:hover, .close-btn2:hover {
  transform: rotate(15deg) scale(1.08);
  color: #f87171;
}
.close-btn2 {
  position: static;
  margin-top: 1.5rem;
  font-size: 1.3rem;
  color: #64748b;
  background: #e0e7ff;
  border-radius: 1.2rem;
  padding: 0.5rem 1.5rem;
  display: block;
  margin-left: auto;
  margin-right: auto;
  transition: background 0.2s, color 0.2s;
}
.close-btn2:hover {
  background: #f87171;
  color: #fff;
}
.quiz-title-anim {
  font-size: 2.7rem;
  font-weight: 700;
  background: linear-gradient(90deg, #6366f1, #06b6d4 60%, #4ade80);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  animation: titlePop 0.7s;
}
@keyframes titlePop {
  0% { transform: scale(0.7); opacity: 0; }
  100% { transform: scale(1); opacity: 1; }
}
.quiz-welcome {
  text-align: center;
  padding: 1.5rem 0 0.5rem 0;
}
.quiz-welcome .desc {
  color: #64748b;
  font-size: 1.35rem;
  margin: 1.2rem 0 2.2rem 0;
}
.start-btn, .restart-btn {
  background: linear-gradient(90deg, #6366f1, #06b6d4 60%, #4ade80);
  color: #fff;
  font-size: 1.2rem;
  font-weight: 600;
  border: none;
  border-radius: 1.5rem;
  padding: 0.7rem 2.2rem;
  cursor: pointer;
  box-shadow: 0 2px 8px 0 rgba(31, 41, 55, 0.08);
  transition: background 0.2s, transform 0.2s;
}
.start-btn:hover, .restart-btn:hover {
  background: linear-gradient(90deg, #4ade80, #06b6d4 60%, #6366f1);
  transform: scale(1.07);
}
.quiz-main {
  padding: 0.5rem 0 0 0;
}
.quiz-q-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 1.1rem;
}
.quiz-q-index {
  font-size: 1.35rem;
  color: #6366f1;
  font-weight: 600;
}
.quiz-timer {
  display: flex;
  align-items: center;
  font-size: 1.1rem;
  color: #64748b;
}
.timer-icon {
  margin-right: 0.3rem;
}
.quiz-question-card {
  background: #fff;
  border-radius: 1.5rem;
  box-shadow: 0 2px 12px 0 rgba(31, 41, 55, 0.08);
  padding: 2rem 1.5rem 2.2rem 1.5rem;
  margin-bottom: 1.2rem;
  min-height: 150px;
  animation: fadeInCard 0.5s;
}
@keyframes fadeInCard {
  from { opacity: 0; transform: translateY(30px);}
  to { opacity: 1; transform: none;}
}
.quiz-question {
  font-size: 1.35rem;
  font-weight: 600;
  color: #334155;
  margin-bottom: 1.1rem;
}
.quiz-options {
  display: flex;
  flex-direction: column;
  gap: 0.7rem;
}
.quiz-opt {
  background: #f1f5f9;
  border: none;
  border-radius: 1.2rem;
  padding: 1rem 1.6rem;
  font-size: 1.22rem;
  color: #334155;
  text-align: left;
  cursor: pointer;
  transition: background 0.18s, color 0.18s, transform 0.18s;
  display: flex;
  align-items: center;
  gap: 0.7rem;
  position: relative;
}
.quiz-opt:hover:not(:disabled) {
  background: #e0e7ff;
  color: #6366f1;
  transform: scale(1.03);
}
.quiz-opt.correct {
  background: #bbf7d0;
  color: #16a34a;
  font-weight: 700;
}
.quiz-opt.wrong {
  background: #fee2e2;
  color: #dc2626;
  font-weight: 700;
}
.opt-label {
  font-weight: 700;
  font-size: 1.1rem;
  width: 1.5rem;
  display: inline-block;
}
.icon-correct {
  color: #16a34a;
  font-size: 1.2rem;
  margin-left: 0.5rem;
}
.icon-wrong {
  color: #dc2626;
  font-size: 1.2rem;
  margin-left: 0.5rem;
}
.quiz-result-wrap {
  position: relative;
  width: 100%;
  height: 100%;
}
.quiz-result {
  text-align: center;
  padding: 1.5rem 0 0.5rem 0;
  position: relative;
}
.result-anim {
  margin: 1.5rem 0 2.2rem 0;
  display: flex;
  flex-direction: column;
  gap: 1.7rem;
  align-items: center;
  position: relative;
}
.score, .beat, .rate {
  font-size: 1.45rem;
  font-weight: 600;
  color: #6366f1;
  background: #f1f5f9;
  border-radius: 1.2rem;
  padding: 0.8rem 2rem;
  display: inline-block;
}
.fireworks-canvas-wrap-global {
  position: fixed;
  left: 0; top: 0; right: 0; bottom: 0;
  width: 100vw; height: 100vh;
  pointer-events: none;
  z-index: 20000;
}
.fireworks-canvas-global {
  width: 100vw;
  height: 100vh;
  display: block;
  background: transparent;
  pointer-events: none;
}
.quiz-loading {
  position: absolute;
  left: 0; right: 0; top: 0; bottom: 0;
  background: rgba(255,255,255,0.7);
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: 2.2rem;
  font-size: 1.2rem;
  color: #6366f1;
  z-index: 10;
}
.loader {
  border: 3px solid #e0e7ff;
  border-top: 3px solid #6366f1;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  animation: spin 1s linear infinite;
  margin-right: 0.7rem;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
.quiz-error {
  color: #dc2626;
  background: #fee2e2;
  border-radius: 1.2rem;
  padding: 0.7rem 1.2rem;
  margin-top: 1.2rem;
  text-align: center;
  font-size: 1.08rem;
  animation: shake 0.3s;
}
@keyframes shake {
  0% { transform: translateX(0);}
  20% { transform: translateX(-6px);}
  40% { transform: translateX(6px);}
  60% { transform: translateX(-4px);}
  80% { transform: translateX(4px);}
  100% { transform: translateX(0);}
}
/* 动画 */
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.35s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
.slide-fade-enter-active {
  transition: all 0.45s cubic-bezier(.68,-0.55,.27,1.55);
}
.slide-fade-enter-from {
  opacity: 0;
  transform: translateY(40px) scale(0.95);
}
.slide-fade-leave-active {
  transition: all 0.25s;
}
.slide-fade-leave-to {
  opacity: 0;
  transform: translateY(-30px) scale(0.95);
}
.zoom-fade-enter-active, .zoom-fade-leave-active {
  transition: all 0.35s cubic-bezier(.68,-0.55,.27,1.55);
}
.zoom-fade-enter-from, .zoom-fade-leave-to {
  opacity: 0;
  transform: scale(0.85);
}
.rate {
  font-size: 1.15rem;
  font-weight: 600;
  color: #6366f1;
  background: #f1f5f9;
  border-radius: 1.2rem;
  padding: 0.6rem 1.5rem;
  display: inline-block;
}
</style>
  
  