<template>
  <div class="home">
    <NavBar />

    <!-- Hero Banner -->
    <div class="hero-banner" :style="{ backgroundImage: `url(${careJobSceneImg})` }" @mouseenter="onBannerEnter" @mousemove="onBannerMove" @mouseleave="onBannerLeave">
      <div class="css-particles">
        <span
          v-for="(p, i) in cssParticles"
          :key="'main-' + i"
          class="css-particle"
          :style="{
            width: p.size + 'px',
            height: p.size + 'px',
            left: p.left,
            top: p.top,
            background: p.gradient,
            opacity: p.opacity,
            animation: `css-particle-float ${p.duration}s linear infinite alternate`,
            animationDelay: p.delay + 's',
            '--float-distance': `-${p.distance}px`,
            boxShadow: p.glow ? '0 0 8px 2px #FFD70088' : 'none'
          }"
        ></span>
        <span
          v-for="(p, i) in tinyGoldParticles"
          :key="'tiny-' + i"
          class="css-particle tiny-gold"
          :style="{
            width: p.size + 'px',
            height: p.size + 'px',
            left: p.left,
            top: p.top,
            background: p.color,
            opacity: p.opacity,
            animation: `css-particle-float ${p.duration}s linear infinite alternate`,
            animationDelay: p.delay + 's',
            '--float-distance': `-${p.distance}px`
          }"
        ></span>
        <span
          v-for="(p, i) in rightSunParticles"
          :key="'right-' + i"
          class="css-particle right-sun"
          :style="{
            width: p.size + 'px',
            height: p.size + 'px',
            left: p.left,
            top: p.top,
            background: p.color,
            opacity: p.opacity,
            animation: `css-particle-float ${p.duration}s linear infinite alternate`,
            animationDelay: p.delay + 's',
            '--float-distance': `-${p.distance}px`,
            boxShadow: p.glow ? '0 0 8px 2px #fffbe688' : 'none'
          }"
        ></span>
      </div>
      <div class="hero-content" :class="{ show: showHeroContent }">
        <h1>We are here to <br />help your arthritis condition</h1>
        <button class="cta-button" @click="handleBegin">Begin With Pain Check! <span class="cta-arrow">→</span></button>
      </div>
    </div>

    <!-- Four Main Functions Section -->
    <div class="functions-section">
      <div class="section-header">
        <h2>Four main functions,</h2>
        <p>using them step by step ensures the best experience.</p>
        <!-- Decoration line below "best experience" -->
        <div class="decoration-container">
          <div class="decoration-line" :style="{ backgroundImage: `url(${brushStrokeImg})` }"></div>
        </div>
      </div>

      <div class="function-list">
        <!-- Step 1: Humidity -->
        <router-link
          to="/humidity"
          class="function-card"
          :class="{ highlight: highlightedStep === 1 }"
          @mouseover="highlightedStep = 1"
          @mouseleave="highlightedStep = null"
        >
          <div class="step-number">Step 1</div>
          <h3>Humidity</h3>
          <p>Find the best time for outdoor activities.</p>
          <ul class="feature-list">
            <li>Based on your postcode</li>
            <li>Real-time humidity</li>
            <li>Daily humidity & temperature trends</li>
            <li>Weather explanation</li>
          </ul>
        </router-link>
        <!-- Step 2: Sport Suggestion -->
        <router-link
          to="/sport-suggestion/mild"
          class="function-card"
          :class="{ highlight: highlightedStep === 2 }"
          @mouseover="highlightedStep = 2"
          @mouseleave="highlightedStep = null"
        >
          <div class="step-number">Step 2</div>
          <h3>Sport Suggestion</h3>
          <p>Personalized exercise ideas for you.</p>
          <ul class="feature-list">
            <li>Customized by pain level</li>
            <li>4 recommended exercises</li>
            <li>Suggested duration</li>
            <li>Easy to follow</li>
          </ul>
        </router-link>
        <!-- Step 3: Body Prediction -->
        <router-link
          to="/symptom-prediction"
          class="function-card"
          :class="{ highlight: highlightedStep === 3 }"
          @mouseover="highlightedStep = 3"
          @mouseleave="highlightedStep = null"
        >
          <div class="step-number">Step 3</div>
          <h3>Body Prediction</h3>
          <p>See tomorrow's results today.</p>
          <ul class="feature-list">
            <li>Input your data</li>
            <li>Intelligent prediction</li>
            <li>Track your progress</li>
            <li>Stay motivated</li>
          </ul>
        </router-link>
        <!-- Step 4: Community -->
        <router-link
          to="/community"
          class="function-card"
          :class="{ highlight: highlightedStep === 4 }"
          @mouseover="highlightedStep = 4"
          @mouseleave="highlightedStep = null"
        >
          <div class="step-number">Step 4</div>
          <h3>Community</h3>
          <p>Share and connect with others.</p>
          <ul class="feature-list">
            <li>Post your experience</li>
            <li>Get support</li>
            <li>Learn from others</li>
            <li>Stay engaged</li>
          </ul>
        </router-link>
      </div>
    </div>

    <!-- CTA Section -->
    <!-- <div class="cta-section">
      <h2>How to do the suitable exercise?</h2>
      <p>Check with pain level first.</p>
      <router-link to="/pain-check" class="check-now-btn">Check Now! →</router-link>
    </div> -->
    <ExerciseCTA />

    <!-- Chart Section -->
    <div class="chart-section">
      <div class="chart-container">
        <div class="chart-info">
          <h2>Arthritis Over the Years</h2>
          <p>
            The number of arthritis cases in various states of Australia has continued to increase
            over the past two decades, and arthritis has become an increasingly important health
            challenge nationwide. We need more attention and strategies!
          </p>
        </div>
        <div class="chart-display">
          <div v-if="isChartLoading" class="chart-loading">
            <div class="loading-spinner"></div>
            <span>Loading arthritis data...</span>
          </div>
          <div v-else-if="chartError" class="chart-error">
            {{ chartError }}
            <button @click="retryFetchData" class="retry-button">Retry</button>
          </div>
          <canvas v-else ref="arthritisChartRef" height="250"></canvas>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import AppFooter from '@/components/AppFooter.vue'
import ExerciseCTA from '@/components/ExerciseCTA.vue'
import { ref, onMounted, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import careJobSceneImg from '@/assets/care-job-scene-with-senior-patient-being-cared.jpg'
import brushStrokeImg from '@/assets/brush-stroke.png'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const highlightedStep = ref(null)

const arthritisChartRef = ref(null)
let arthritisChart = null
const isChartLoading = ref(true)
const chartError = ref(null)

const router = useRouter()
const userStore = useUserStore()

// 生成30个特别精致的金色粒子参数
const goldGradients = [
  'radial-gradient(circle at 60% 40%, #fffbe6 0%, #FFD700 60%, #FFC300 100%)',
  'radial-gradient(circle at 50% 50%, #FFF9E3 0%, #FFD700 70%, #FFC300 100%)',
  'radial-gradient(circle at 60% 40%, #FFF6C3 0%, #FFD700 80%, #FFECB3 100%)',
  'radial-gradient(circle at 55% 45%, #FFFBE6 0%, #FFF6C3 60%, #FFD700 100%)',
  'radial-gradient(circle at 60% 40%, #FFF9E3 0%, #FFD700 60%, #FFC300 100%)'
]
const cssParticles = Array.from({ length: 30 }).map((_, i) => {
  let left, top;
  // 避开两个人脸区域
  do {
    left = (Math.random() * 90 + 2);
    top = (Math.random() * 80 + 5);
  } while (
    (left >= 40 && left <= 70 && top >= 20 && top <= 60) || // 区域1
    (left >= 15 && left <= 35 && top >= 10 && top <= 35)    // 区域2
  );
  return {
    size: (Math.random() * 6 + 3).toFixed(1), // 3~9px
    left: left.toFixed(1) + '%',
    top: top.toFixed(1) + '%',
    gradient: goldGradients[Math.floor(Math.random() * goldGradients.length)],
    opacity: (Math.random() * 0.08 + 0.10).toFixed(2), // 0.10~0.18
    duration: (i % 3 === 0)
      ? (Math.random() * 2 + 2).toFixed(1) // 2~4s更快
      : (Math.random() * 4 + 5).toFixed(1), // 5~9s
    delay: (Math.random() * 5).toFixed(1),
    distance: (Math.random() * 14 + 8).toFixed(1), // 8~22px
    glow: i % 5 === 0 // 每5个粒子加发光
  }
})

// 生成12个特别细小的纯金色粒子
const tinyGoldParticles = Array.from({ length: 12 }).map((_, i) => {
  let left, top;
  do {
    left = (Math.random() * 90 + 2);
    top = (Math.random() * 80 + 5);
  } while (
    (left >= 40 && left <= 70 && top >= 20 && top <= 60) ||
    (left >= 15 && left <= 35 && top >= 10 && top <= 35)
  );
  return {
    size: (Math.random() * 1.5 + 2).toFixed(1), // 2~3.5px
    left: left.toFixed(1) + '%',
    top: top.toFixed(1) + '%',
    color: i % 2 === 0 ? '#FFD700' : '#FFC300',
    opacity: (Math.random() * 0.08 + 0.10).toFixed(2),
    duration: (i % 3 === 0)
      ? (Math.random() * 2 + 2).toFixed(1)
      : (Math.random() * 4 + 5).toFixed(1),
    delay: (Math.random() * 5).toFixed(1),
    distance: (Math.random() * 14 + 8).toFixed(1)
  }
})

// 生成8个右侧淡金色粒子（更亮更可见）
const rightSunParticles = Array.from({ length: 8 }).map((_, i) => {
  let left, top;
  do {
    left = (Math.random() * 16 + 80); // 80%~96%
    top = (Math.random() * 80 + 5);   // 5%~85%
  } while (
    (left >= 40 && left <= 70 && top >= 20 && top <= 60) ||
    (left >= 15 && left <= 35 && top >= 10 && top <= 35)
  );
  const colorPool = ['#FFFBE6', '#FFF9E3', '#FFD700', '#fff'];
  return {
    size: (Math.random() * 2 + 2.5).toFixed(1), // 2.5~4.5px
    left: left.toFixed(1) + '%',
    top: top.toFixed(1) + '%',
    color: colorPool[Math.floor(Math.random() * colorPool.length)],
    opacity: (Math.random() * 0.07 + 0.15).toFixed(2), // 0.15~0.22
    duration: (Math.random() * 3 + 4).toFixed(1), // 4~7s
    delay: (Math.random() * 5).toFixed(1),
    distance: (Math.random() * 10 + 6).toFixed(1),
    glow: i % 2 === 0 // 一半粒子加发光
  }
})

// 控制内容显示的响应式变量和定时器
const showHeroContent = ref(false)
let hideTimer = null

function onBannerEnter() {
  showHeroContent.value = true
  resetHideTimer()
}
function onBannerMove() {
  showHeroContent.value = true
  resetHideTimer()
}
function onBannerLeave() {
  showHeroContent.value = false
  clearHideTimer()
}
function resetHideTimer() {
  clearHideTimer()
  hideTimer = setTimeout(() => {
    showHeroContent.value = false
  }, 2000)
}
function clearHideTimer() {
  if (hideTimer) {
    clearTimeout(hideTimer)
    hideTimer = null
  }
}

// 从 API 获取数据
async function fetchArthritisData() {
  try {
    console.log('Starting to retrieve data...')
    isChartLoading.value = true
    chartError.value = null

    // Direct API call
    try {
      // Use direct URL instead of proxy
      const response = await fetch('https://api.arthritisease.org/getArthritisDataFromRDS/', {
        method: 'GET',
        headers: {
          'Content-Type': 'application/json',
          'Accept': 'application/json',
          'Origin': 'https://arthritisease.org',
          'Referer': 'https://arthritisease.org/'
        },
        mode: 'cors'
      })

      if (!response.ok) {
        throw new Error(`API request failed: ${response.status}`)
      }

      const data = await response.json()

      // Handle different response formats
      if (typeof data === 'string') {
        return JSON.parse(data)
      }

      if (data && data.body) {
        if (typeof data.body === 'string') {
          return JSON.parse(data.body)
        }
        return data.body
      }

      return data
    } catch (error) {
      console.error('Error fetching arthritis data:', error)
      chartError.value = `Unable to load data: ${error.message}`
      return null
    } finally {
      isChartLoading.value = false
    }
  } catch (error) {
    console.error('Error fetching arthritis data:', error)
    chartError.value = `Unable to load data: ${error.message}`
    return null
  }
}

function createArthritisChart(data) {
  try {
    console.log('Start creating chart:', data ? 'valid data' : 'Invalid data')
    if (!arthritisChartRef.value || !data) {
      console.error(
        'Unable to create chart:',
        !arthritisChartRef.value ? 'Canvas element not found' : 'No data',
      )
      return
    }

    
    const years = [...new Set(data.map((item) => item.Year_numeric))].sort()

    // 定义要显示的主要州（为了可读性）
    const mainStates = ['New South Wales', 'Victoria', 'Queensland', 'Western Australia']

    // 按州分组数据
    const stateData = {}

    // 初始化每个州的数据结构
    mainStates.forEach((state) => {
      stateData[state] = data
        .filter((item) => item.State === state)
        .sort((a, b) => a.Year_numeric - b.Year_numeric)
    })

    // 为每个州定义颜色
    const stateColors = {
      'New South Wales': '#4a6741',
      Victoria: '#2980b9',
      Queensland: '#e67e22',
      'Western Australia': '#8e44ad',
    }

    const datasets = mainStates.map((state) => {
      return {
        label: state,
        data: stateData[state].map((item) => item['Arthritis Value']),
        borderColor: stateColors[state],
        backgroundColor: `${stateColors[state]}20`,
        tension: 0.3,
        fill: false,
        pointRadius: 4,
        pointHoverRadius: 6,
      }
    })

    if (arthritisChart) {
      arthritisChart.destroy()
    }

    const ctx = arthritisChartRef.value.getContext('2d')

    arthritisChart = new Chart(ctx, {
      type: 'line',
      data: {
        labels: years,
        datasets: datasets,
      },
      options: {
        responsive: true,
        maintainAspectRatio: false,
        plugins: {
          legend: {
            position: 'top',
            labels: {
              usePointStyle: true,
              boxWidth: 10,
            },
          },
          tooltip: {
            mode: 'index',
            intersect: false,
          },
          title: {
            display: false,
          },
        },
        scales: {
          x: {
            title: {
              display: true,
              text: 'Year',
            },
          },
          y: {
            title: {
              display: true,
              text: 'Arthritis Cases (thousands)',
            },
            beginAtZero: false,
          },
        },
      },
    })
    console.log('Chart created successfully')
  } catch (error) {
    console.error('Chart creation error:', error)
    chartError.value = `Chart creation failed: ${error.message}`
  }
}

function retryFetchData() {
  loadArthritisData()
}

async function loadArthritisData() {
  try {
    const data = await fetchArthritisData()

    if (data && data.length > 0) {
      console.log('Creating chart using API data')
      nextTick(() => {
        createArthritisChart(data)
      })
    } else {
      chartError.value = 'No data available. Please try again later.'
    }
  } catch (error) {
    console.error('Data loading error:', error)
    chartError.value = `Error loading data: ${error.message}`
  }
}

function handleBegin() {
  if (!userStore.user_profile) {
    router.push({ name: 'userProfile' })
  } else if (userStore.painCheckDone) {
    router.push('/sport-suggestion/mild')
  } else {
    router.push({ name: 'painCheck' })
  }
}

onMounted(() => {
  loadArthritisData()
})
</script>

<style scoped>
.home {
  width: 100%;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  font-family: Arial, sans-serif;
}

/* Hero Banner */
.hero-banner {
  position: relative;
  height: 80vh;
  min-height: 400px;
  max-height: 100vh;
  background-size: cover;
  background-position: center;
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 0;
  overflow: hidden;
  animation: hero-zoom 18s ease-in-out infinite alternate;
}
@keyframes hero-zoom {
  0% { transform: scale(1); }
  100% { transform: scale(1.08); }
}
.css-particles {
  position: absolute;
  left: 0; top: 0; width: 100%; height: 100%;
  pointer-events: none;
  z-index: 1;
}
.css-particle {
  position: absolute;
  border-radius: 50%;
  will-change: transform;
}
@keyframes css-particle-float {
  0% { transform: translateY(0) scale(1);}
  100% { transform: translateY(var(--float-distance, -18px)) scale(1.08);}
}
.hero-content {
  position: absolute;
  left: 80px;
  bottom: 40px;
  top: auto;
  right: auto;
  transform: none;
  z-index: 2;
  color: #fff;
  max-width: 700px;
  min-width: 0;
  width: auto;
  text-align: left;
  margin: 0;
  padding: 0 10px;
  box-sizing: border-box;
  border-radius: 0;
  background: none;
  box-shadow: none;
  backdrop-filter: none;
  -webkit-backdrop-filter: none;
  border: none;
  opacity: 0;
  pointer-events: none;
  transition: opacity 0.4s;
  max-width: 90vw;
}
.hero-content.show {
  opacity: 1;
  pointer-events: auto;
}
.hero-content h1 {
  font-size: clamp(1.1rem, 3vw, 1.7rem);
  margin-bottom: 14px;
  font-weight: bold;
  line-height: 1.2;
  text-shadow: 0 4px 24px rgba(0,0,0,0.18), 0 1px 2px rgba(0,0,0,0.12);
}
.cta-button {
  position: relative;
  overflow: hidden;
  font-size: 0.95rem;
  padding: 8px 16px;
  display: inline-flex;
  align-items: center;
  gap: 0.5em;
  background: linear-gradient(90deg, #4a6741 0%, #8dc26f 100%);
  color: #fff;
  border-radius: 20px;
  font-weight: bold;
  box-shadow: 0 2px 12px rgba(74,103,65,0.10);
  transition: box-shadow 0.5s, transform 0.5s;
  letter-spacing: 1px;
  cursor: pointer;
  text-decoration: none;
  animation: cta-breath 1.8s ease-in-out infinite alternate;
  z-index: 1;
  width: auto;
  min-width: 0;
  justify-content: center;
  border: none;
}
.cta-button::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(90deg, #8dc26f 0%, #4a6741 100%);
  opacity: 0;
  transition: opacity 0.5s;
  z-index: 0;
  pointer-events: none;
}
.cta-button:hover::before {
  opacity: 1;
}
.cta-button > * {
  position: relative;
  z-index: 1;
  color: #fff;
}
.cta-arrow {
  font-size: 1.1em;
  transition: transform 0.5s;
}
.cta-button:hover .cta-arrow {
  transform: translateX(4px) scale(1.15);
}
.cta-button:hover {
  /* 不再切换background */
  transform: scale(1.06);
  box-shadow: 0 6px 24px rgba(74,103,65,0.18), 0 0 12px #8dc26f88;
}
@keyframes cta-breath {
  0% { transform: scale(1); box-shadow: 0 2px 12px rgba(74,103,65,0.10); }
  100% { transform: scale(1.07); box-shadow: 0 6px 24px rgba(74,103,65,0.18), 0 0 16px #8dc26f55; }
}

/* Functions Section */
.functions-section {
  padding: 50px 20px;
  max-width: 1200px;
  margin: 0 auto;
}

.section-header {
  text-align: center;
  margin-bottom: 40px;
  position: relative;
}

.section-header h2 {
  font-size: 2rem;
  color: #4a6741;
  margin-bottom: 5px;
}

.section-header p {
  font-size: 1.5rem;
  color: #4a6741;
  margin-top: 0;
  margin-bottom: 10px;
}

.decoration-container {
  display: flex;
  justify-content: center;
  width: 100%;
}

.decoration-line {
  width: 400px;
  height: 10px;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  margin-top: 5px;
}

.function-list {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 20px;
  margin-top: 30px;
}

.function-card {
  background: white;
  border-radius: 15px;
  padding: 25px;
  text-decoration: none;
  color: inherit;
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.function-card.highlight {
  background-color: #eaf5e1;
  border-color: rgba(74,103,65,0.18);
}

.function-card:hover {
  background-color: #eaf5e1;
  border-color: rgba(74,103,65,0.18);
  box-shadow: 0 4px 16px rgba(74,103,65,0.08);
  transform: translateY(-5px);
}

.function-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(74, 103, 65, 0.05),
    transparent
  );
  transition: 0.5s;
}

.function-card:hover::before {
  left: 100%;
}

.step-number {
  color: #4a6741;
  font-weight: bold;
  font-size: 1.2rem;
  margin-bottom: 10px;
  transition: all 0.3s ease;
}

.function-card:hover .step-number {
  transform: scale(1.1);
  color: #3a5331;
}

.function-card h3 {
  transition: all 0.3s ease;
}

.function-card:hover h3 {
  color: #4a6741;
}

.function-card p {
  color: #666;
  margin-bottom: 15px;
}

.feature-list {
  list-style-type: none;
  padding: 0;
  margin-bottom: 20px;
}

.feature-list li {
  position: relative;
  padding-left: 20px;
  margin-bottom: 8px;
}

.feature-list li::before {
  content: '✓';
  position: absolute;
  left: 0;
  color: #4a6741;
}

/* CTA Section */
.cta-section {
  background-color: #eaf5e1;
  padding: 70px 20px;
  text-align: center;
}

.cta-section h2 {
  font-size: 2.2rem;
  color: #333;
  margin-bottom: 10px;
}

.cta-section p {
  font-size: 1.2rem;
  color: #4a6741;
  margin-bottom: 30px;
}

.check-now-btn {
  display: inline-block;
  background-color: #4a6741;
  color: white;
  padding: 12px 30px;
  text-decoration: none;
  border-radius: 4px;
  font-weight: bold;
  transition: background-color 0.3s;
  font-size: 1rem;
}

.check-now-btn:hover {
  background-color: #3a5331;
}

/* Chart Section */
.chart-section {
  padding: 50px 20px;
  background-color: #f8f8f8;
  position: relative;
  overflow: hidden;
}

.chart-container {
  max-width: 1200px;
  margin: 0 auto;
  background: white;
  border-radius: 15px;
  padding: 30px;
  box-shadow: 0 10px 30px rgba(74, 103, 65, 0.15);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
  overflow: hidden;
}

.chart-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 20px 40px rgba(74, 103, 65, 0.2);
}

.chart-container::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    120deg,
    transparent,
    rgba(74, 103, 65, 0.1),
    transparent
  );
  transition: 0.6s;
}

.chart-container:hover::before {
  left: 100%;
}

.chart-info {
  opacity: 0.8;
  transform: translateY(10px);
  transition: all 0.4s ease;
}

.chart-container:hover .chart-info {
  opacity: 1;
  transform: translateY(0);
}

.chart-info h2 {
  font-size: 2rem;
  color: #333;
  margin-bottom: 20px;
  position: relative;
  display: inline-block;
}

.chart-info h2::after {
  content: '';
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 0;
  height: 2px;
  background-color: #4a6741;
  transition: width 0.4s ease;
}

.chart-container:hover .chart-info h2::after {
  width: 100%;
}

.chart-info p {
  color: #4a6741;
  font-size: 1.1rem;
  line-height: 1.6;
  transform: translateX(-10px);
  opacity: 0.8;
  transition: all 0.4s ease;
}

.chart-container:hover .chart-info p {
  transform: translateX(0);
  opacity: 1;
}

.chart-display {
  margin-top: 30px;
  background-color: white;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.4s ease;
}

.chart-container:hover .chart-display {
  box-shadow: 0 8px 25px rgba(74, 103, 65, 0.1);
}

.chart-loading,
.chart-error {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  background-color: rgba(255, 255, 255, 0.95);
  padding: 20px;
  text-align: center;
  gap: 15px;
  border-radius: 12px;
  transition: all 0.3s ease;
  backdrop-filter: blur(3px);
}

.loading-spinner {
  width: 40px;
  height: 40px;
  border: 3px solid rgba(74, 103, 65, 0.1);
  border-radius: 50%;
  border-top: 4px solid #4a6741;
  border-left: 4px solid transparent;
  animation: spin 1.2s cubic-bezier(0.4, 0.1, 0.3, 1) infinite;
  margin-bottom: 16px;
  box-shadow: 0 2px 10px rgba(74, 103, 65, 0.1);
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  50% { transform: rotate(180deg); }
  100% { transform: rotate(360deg); }
}

.chart-loading span {
  font-size: 1.1rem;
  font-weight: 500;
  color: #4a6741;
  animation: pulse 1.5s infinite cubic-bezier(0.4, 0, 0.6, 1);
  letter-spacing: 0.5px;
  margin-top: 5px;
}

@keyframes pulse {
  0% { opacity: 0.7; transform: scale(0.98); }
  50% { opacity: 1; transform: scale(1.02); }
  100% { opacity: 0.7; transform: scale(0.98); }
}

.chart-error {
  color: #e74c3c;
}

.retry-button {
  background-color: #4a6741;
  color: white;
  padding: 8px 16px;
  border: none;
  border-radius: 4px;
  cursor: pointer;
  margin-top: 15px;
  font-size: 0.9rem;
  transition: background-color 0.3s;
}

.retry-button:hover {
  background-color: #3a5331;
}

@media (max-width: 1100px) {
  .function-list {
    grid-template-columns: repeat(2, 1fr);
  }

  .decoration-line {
    width: 300px;
  }
}

@media (max-width: 900px) {
  .hero-banner {
    height: 60vh;
    min-height: 320px;
  }
  .hero-content h1 {
    font-size: clamp(1.5rem, 7vw, 2.2rem);
  }
}

@media (max-width: 600px) {
  .hero-banner {
    height: 45vh;
    min-height: 180px;
  }
  .hero-content {
    left: 10px;
    bottom: 10px;
    top: auto;
    right: auto;
    max-width: 98vw;
    padding: 0 4px;
  }
  .hero-content h1 {
    font-size: clamp(0.9rem, 4vw, 1.2rem);
  }
  .cta-button {
    font-size: 0.85rem;
    padding: 6px 12px;
  }
}

.tiny-gold {
  border-radius: 50%;
  box-shadow: none !important;
  background: #FFD700 !important;
}

.right-sun {
  border-radius: 50%;
  box-shadow: none !important;
  background: #FFF9E3 !important;
}
</style>

<style>
@keyframes css-particle-float {
  0% { transform: translateY(0) scale(1);}
  100% { transform: translateY(var(--float-distance, -18px)) scale(1.08);}
}
</style>
