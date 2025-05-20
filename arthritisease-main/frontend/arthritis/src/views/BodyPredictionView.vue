<template>
  <NavBar />
  <div class="body-prediction-page">
    <div class="container">
      <div class="back-link">
        <router-link to="/">
          <span class="back-arrow">←</span>
        </router-link>
        <h1>Body Prediction</h1>
      </div>
      <p class="subtitle">Predict your body changes and manage your health scientifically</p>
      <div class="big-prediction-card">
        <div class="card-left">
          <h2 class="big-title">Body Prediction</h2>
          <p class="big-subtitle">Predict your body changes and manage your health scientifically</p>
        </div>
        <div class="card-right">
          <form @submit.prevent="predict" class="prediction-form">
            <div class="user-info">
              <div class="info-item"><span>Height:</span> {{ user.height }} cm</div>
              <div class="info-item"><span>Weight:</span> {{ user.weight }} kg</div>
              <div class="info-item"><span>Age:</span> {{ user.age }}</div>
              <div class="info-item"><span>Gender:</span> {{ user.gender }}</div>
              <div class="info-item"><span>Silhouette:</span> {{ user.silhouette }}</div>
              <div class="info-item"><span>Somatotype:</span> {{ user.somatotype }}</div>
            </div>
            <div class="input-row">
              <label>Calories Burned Per Day
                <input :value="autoCalories" type="number" readonly class="calories-animated" />
              </label>
              <label>Duration
                <input value="1 Month" type="text" readonly class="duration-readonly" />
              </label>
            </div>
            <button class="predict-btn" :disabled="loading">
              <span v-if="!loading">Predict</span>
              <span v-else>
                Predicting
                <span class="btn-spinner"></span>
              </span>
            </button>
          </form>
        </div>
        <div class="card-decoration">
          <div class="circle circle-1"></div>
          <div class="circle circle-2"></div>
          <div class="circle circle-3"></div>
        </div>
      </div>
    </div>
    <div v-if="error" class="error-msg">{{ error }}</div>
    <div v-if="result" class="result-area">
      <div class="chart-and-cards">
        <div class="chart-card">
          <canvas ref="chartRef" height="180"></canvas>
          <div class="timeline-slider">
            <input type="range" min="0" :max="result.future_body_prediction_month.length-1" v-model="currentIndex" />
            <div class="timeline-labels">
              <span v-for="(row, i) in result.future_body_prediction_month" :key="i" :class="{ active: i === currentIndex }">Day {{ i*2 }}</span>
            </div>
          </div>
        </div>
        <div class="data-cards">
          <div class="data-card" v-for="(item, key) in currentData" :key="key">
            <div class="data-label">{{ cardLabels[key] }}</div>
            <div class="data-value">
              <CountUpNumber :value="Number(item)" />
            </div>
          </div>
        </div>
      </div>
      <div class="ai-summary">
        <div class="ai-avatar">🤖</div>
        <div class="ai-text">
          <TypewriterText :text="aiSummary" :speed="18" />
        </div>
      </div>
    </div>
  </div>
  <AppFooter />
</template>

<script setup>
import { ref, computed, watch, nextTick, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
import Chart from 'chart.js/auto'
import NavBar from '@/components/NavBar.vue'
import AppFooter from '@/components/AppFooter.vue'
import CountUpNumber from '@/components/CountUpNumber.vue'
import TypewriterText from '@/components/TypewriterText.vue'

const userStore = useUserStore()
const router = useRouter()
const user = computed(() => userStore.user_profile || { weight: 60 })

onMounted(() => {
  if (!userStore.user_profile) {
    window.$notify
      ? window.$notify({ type: 'warning', message: 'Please complete your profile first!' })
      : alert('Please complete your profile first!')
    router.push({ name: 'userProfile' })
  }
})

// METs 映射表
const METS_MAP = {
  Walking: 3.5,
  Cycling: 4.5,
  Yoga: 2.5,
  'Tai Chi': 3.0,
  Swimming: 6.0,
  'Water Aerobics': 5.5,
  Golf: 4.8,
  'Elliptical Training': 5.0,
  'Chair Exercises': 1.5,
  'Aquatic Therapy': 3.0,
  'Stretching Routines': 2.3,
  'Adaptive Sports': 3.0
}
const exercisePlan = computed(() => userStore.exercise_plan || [])
const autoCalories = computed(() => {
  const weight = Number(user.value.weight) || 60
  return exercisePlan.value.reduce((sum, sport) => {
    let minMins = 20
    if (sport.duration) {
      const match = sport.duration.match(/(\d+)/)
      if (match) minMins = Number(match[1])
    }
    const mets = METS_MAP[sport.name] || 3.5
    const hours = minMins / 60
    return sum + mets * weight * hours
  }, 0).toFixed(0)
})

const duration = ref('1 month')
const loading = ref(false)
const error = ref('')
const result = ref(null)
const chartRef = ref(null)
const chartInstance = ref(null)
const currentIndex = ref(0)
const aiSummary = ref('')
const cardLabels = {
  weight: 'Weight (kg)',
  body_fat: 'Body Fat (%)',
  skeletal_muscle_rate: 'Skeletal Muscle (kg)',
  active_mets: 'Active METs',
  basal_metabolic_rate: 'BMR (kcal)',
  body_fat_to_weight_ratio: 'Fat/Weight Ratio'
}
const currentData = computed(() => {
  if (!result.value) return {}
  return result.value.future_body_prediction_month[currentIndex.value] || {}
})

async function predict() {
  loading.value = true
  error.value = ''
  result.value = null
  aiSummary.value = ''
  try {
    const res = await fetch('https://api.arthritisease.org/bodyPrediction/', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        user_profile: user.value,
        calories_burned: autoCalories.value,
        goal_duration: duration.value
      })
    })
    const data = await res.json()
    let body = typeof data.body === 'string' ? JSON.parse(data.body) : data.body || data
    result.value = body
    currentIndex.value = 0
    await nextTick()
    renderChart()
    aiSummary.value = `Over the next month, your weight may drop from ${body.future_body_prediction_month[0].weight}kg to ${body.future_body_prediction_month.at(-1).weight}kg, body fat from ${body.future_body_prediction_month[0].body_fat}% to ${body.future_body_prediction_month.at(-1).body_fat}%. Keep exercising for better results!`
  } catch (e) {
    error.value = e.message || 'Prediction failed'
  } finally {
    loading.value = false
  }
}

function renderChart() {
  if (!result.value || !chartRef.value) return
  if (chartInstance.value) chartInstance.value.destroy()
  const labels = result.value.future_body_prediction_month.map((_, i) => `Day ${i*2}`)
  const dataArr = result.value.future_body_prediction_month
  chartInstance.value = new Chart(chartRef.value, {
    type: 'line',
    data: {
      labels,
      datasets: [
        {
          label: 'Weight (kg)',
          data: dataArr.map(d => d.weight),
          borderColor: '#4a6741',
          backgroundColor: '#eaf5e1',
          tension: 0.3,
          fill: false
        },
        {
          label: 'Body Fat (%)',
          data: dataArr.map(d => d.body_fat),
          borderColor: '#e67e22',
          backgroundColor: '#fbeee0',
          tension: 0.3,
          fill: false
        },
        {
          label: 'Skeletal Muscle (kg)',
          data: dataArr.map(d => d.skeletal_muscle_rate),
          borderColor: '#2980b9',
          backgroundColor: '#e0f0fb',
          tension: 0.3,
          fill: false
        }
      ]
    },
    options: {
      responsive: true,
      plugins: {
        legend: { position: 'top' },
        tooltip: { mode: 'index', intersect: false }
      },
      interaction: { mode: 'nearest', axis: 'x', intersect: false },
      scales: {
        x: { title: { display: true, text: 'Day' } },
        y: { title: { display: true, text: 'Value' }, beginAtZero: false }
      }
    }
  })
}

watch(currentIndex, () => {
  // 可加动画或联动
})
</script>

<style scoped>
.body-prediction-page {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ea 0%, #ffffff 50%, #e8f3e0 100%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.container {
  width: 100%;
  padding: 2rem 1rem;
  flex: 1;
}
.back-link {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
}
.back-arrow {
  font-size: 1.5rem;
  color: #4a6741;
  margin-right: 1rem;
  text-decoration: none;
  transition: transform 0.3s ease;
}
.back-arrow:hover {
  transform: translateX(-4px);
}
h1 {
  font-size: 2.5rem;
  margin: 0;
  background: linear-gradient(45deg, #4a6741, #6b8f5e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: left;
}
.subtitle {
  color: #666;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  text-align: left;
}
.big-prediction-card {
  position: relative;
  display: flex;
  justify-content: space-between;
  align-items: center;
  background: linear-gradient(120deg, #cad9a1 0%, #a5c77f 100%);
  border-radius: 28px;
  padding: 48px 48px 48px 48px;
  margin-bottom: 40px;
  box-shadow: 0 15px 35px rgba(165, 199, 127, 0.18);
  overflow: hidden;
  min-height: 260px;
}
.card-left {
  flex: 1.2;
  z-index: 2;
}
.card-right {
  flex: 1;
  z-index: 2;
  display: flex;
  flex-direction: column;
  align-items: flex-end;
}
.big-title {
  font-size: 2.2rem;
  color: #fff;
  font-weight: 800;
  margin-bottom: 14px;
  text-shadow: 0 2px 8px rgba(74,103,65,0.08);
}
.big-subtitle {
  color: #f5f8f3;
  font-size: 1.32rem;
  font-weight: 400;
  margin-bottom: 0;
  max-width: 420px;
  line-height: 1.6;
}
.prediction-form {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(74,103,65,0.10);
  padding: 32px 24px 24px 24px;
  margin-bottom: 0;
  margin-left: 0;
  margin-right: 0;
  min-width: 340px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  position: relative;
  z-index: 2;
  font-size: 0.92rem;
}
.user-info {
  display: flex;
  flex-wrap: wrap;
  gap: 18px;
  margin-bottom: 10px;
}
.info-item {
  background: #eaf5e1;
  border-radius: 14px;
  padding: 6px 10px;
  color: #4a6741;
  font-weight: 600;
  font-size: 0.82rem;
  box-shadow: 0 2px 8px rgba(74,103,65,0.06);
  margin-bottom: 0;
  opacity: 0;
  transform: translateY(30px) scale(0.96);
  animation: info-bounce-in 0.7s cubic-bezier(.4,1.4,.6,1) forwards;
  transition: box-shadow 0.3s, transform 0.3s;
}
.info-item:nth-child(1) { animation-delay: 0.05s; }
.info-item:nth-child(2) { animation-delay: 0.12s; }
.info-item:nth-child(3) { animation-delay: 0.19s; }
.info-item:nth-child(4) { animation-delay: 0.26s; }
.info-item:nth-child(5) { animation-delay: 0.33s; }
.info-item:nth-child(6) { animation-delay: 0.40s; }
.info-item:hover {
  transform: scale(1.04) translateY(-2px);
  box-shadow: 0 6px 24px rgba(74,103,65,0.13);
}
@keyframes info-bounce-in {
  0% { opacity: 0; transform: translateY(30px) scale(0.96); }
  60% { opacity: 1; transform: translateY(-8px) scale(1.04); }
  80% { transform: translateY(4px) scale(0.98); }
  100% { opacity: 1; transform: translateY(0) scale(1); }
}
.input-row {
  display: flex;
  gap: 18px;
  align-items: center;
}
.input-row label {
  display: flex;
  flex-direction: column;
  font-size: 0.82rem;
  color: #2c3e50;
  font-weight: 500;
}
.input-row input, .input-row .duration-readonly {
  margin-top: 4px;
  padding: 5px 7px;
  border-radius: 12px;
  border: 1.5px solid #b5cc7a;
  font-size: 0.82rem;
  background: #fff;
  transition: border 0.3s, box-shadow 0.3s;
  outline: none;
  box-shadow: 0 2px 8px rgba(74,103,65,0.06);
}
.input-row input:focus, .input-row .duration-readonly:focus {
  border: 2px solid #4a6741;
  box-shadow: 0 0 0 2px #eaf5e1;
  transition: border 0.3s, box-shadow 0.3s;
}
.predict-btn {
  margin-top: 10px;
  padding: 7px 0;
  background: #4a6741;
  color: #fff;
  border: none;
  border-radius: 12px;
  font-weight: bold;
  font-size: 0.88rem;
  cursor: pointer;
  transition: background 0.3s, transform 0.2s, box-shadow 0.3s;
  box-shadow: 0 2px 8px rgba(74,103,65,0.10);
  position: relative;
  overflow: hidden;
  z-index: 1;
  width: 100%;
}
.predict-btn:hover {
  background: linear-gradient(90deg, #6b8f5e 0%, #4a6741 100%);
  transform: scale(1.05);
  box-shadow: 0 6px 24px rgba(74,103,65,0.18);
}
.predict-btn:active {
  transform: scale(0.97);
}
.predict-btn .btn-spinner {
  display: inline-block;
  width: 20px; height: 20px;
  border: 3px solid #fff;
  border-top: 3px solid #4a6741;
  border-radius: 50%;
  animation: spin 1s linear infinite;
  margin-left: 8px;
  vertical-align: middle;
}
@keyframes spin {
  0% { transform: rotate(0deg);}
  100% { transform: rotate(360deg);}
}
.card-decoration {
  position: absolute;
  inset: 0;
  z-index: 1;
  pointer-events: none;
}
.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255,255,255,0.18);
  filter: blur(2px);
  animation: bubble-move 8s ease-in-out infinite alternate;
}
.circle-1 {
  width: 220px; height: 220px;
  left: 10%; top: 30%;
  animation-delay: 0s;
}
.circle-2 {
  width: 160px; height: 160px;
  right: 8%; top: 18%;
  animation-delay: 2s;
}
.circle-3 {
  width: 120px; height: 120px;
  left: 40%; bottom: 10%;
  animation-delay: 4s;
}
@keyframes bubble-move {
  0% { transform: translateY(0) scale(1); opacity: 0.7; }
  40% { transform: translateY(-18px) scale(1.08); opacity: 0.9; }
  60% { transform: translateY(12px) scale(0.96); opacity: 0.8; }
  100% { transform: translateY(-24px) scale(1.12); opacity: 1; }
}
.error-msg {
  color: #e74c3c;
  background: #fff0f0;
  border: 1px solid #ffb3b3;
  border-radius: 6px;
  padding: 8px 16px;
  margin: 18px auto;
  max-width: 400px;
  text-align: center;
  font-size: 1.05rem;
}
.result-area {
  margin-top: 32px;
}
.chart-and-cards {
  display: flex;
  gap: 32px;
  flex-wrap: wrap;
  align-items: flex-start;
}
.chart-card {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 2px 12px rgba(74,103,65,0.10);
  padding: 24px 18px 18px 18px;
  min-width: 380px;
  min-height: 220px;
  flex: 1 1 420px;
  display: flex;
  flex-direction: column;
  align-items: center;
}
.timeline-slider {
  width: 100%;
  margin-top: 18px;
}
.timeline-slider input[type=range] {
  width: 100%;
}
.timeline-labels {
  display: flex;
  justify-content: space-between;
  font-size: 0.95rem;
  color: #4a6741;
  margin-top: 4px;
}
.timeline-labels span.active {
  font-weight: bold;
  color: #e67e22;
}
.data-cards {
  display: flex;
  flex-direction: column;
  gap: 16px;
  min-width: 220px;
}
.data-card {
  background: linear-gradient(90deg, #eaf5e1 0%, #f8f9fa 100%);
  border-radius: 12px;
  box-shadow: 0 2px 8px rgba(74,103,65,0.06);
  padding: 16px 18px;
  display: flex;
  flex-direction: column;
  align-items: center;
  font-size: 1.08rem;
  color: #2c3e50;
  font-weight: 500;
  transition: 
    transform 0.25s cubic-bezier(.4,1.4,.6,1),
    box-shadow 0.25s cubic-bezier(.4,1.4,.6,1);
  will-change: transform, box-shadow;
}
.data-card:hover {
  transform: translateY(-8px) scale(1.06) rotate(-1deg);
  box-shadow: 0 8px 32px rgba(230,126,34,0.13), 0 2px 8px rgba(74,103,65,0.10);
  z-index: 2;
}
.data-label {
  color: #4a6741;
  font-size: 0.98rem;
  margin-bottom: 4px;
}
.data-value {
  font-size: 1.25rem;
  font-weight: bold;
  color: #e67e22;
}
.ai-summary {
  margin-top: 36px;
  display: flex;
  align-items: center;
  gap: 18px;
  background: #fff;
  border-radius: 14px;
  box-shadow: 0 2px 8px rgba(74,103,65,0.08);
  padding: 18px 24px;
  font-size: 1.08rem;
  color: #4a6741;
  position: relative;
}
.ai-avatar {
  font-size: 2.2rem;
  background: #eaf5e1;
  border-radius: 50%;
  width: 48px;
  height: 48px;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(74,103,65,0.08);
}
.duration-readonly {
  background: #f5f5f5;
  border: 1.5px solid #b5cc7a;
  border-radius: 8px;
  padding: 8px 12px;
  font-size: 1rem;
  color: #888;
  margin-top: 4px;
}
@media (max-width: 900px) {
  .big-prediction-card {
    flex-direction: column;
    padding: 32px 12px;
    min-height: unset;
  }
  .card-left, .card-right {
    align-items: flex-start;
    width: 100%;
  }
  .prediction-form {
    min-width: unset;
    width: 100%;
  }
}
</style> 