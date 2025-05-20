<template>
  <div class="humidity-page">
    <NavBar />

    <div class="container">
      <div class="back-link">
        <router-link to="/">
          <span class="back-arrow">←</span>
        </router-link>
        <h1>Humidity & Weather</h1>
      </div>
      <p class="subtitle">Customize it to your needs</p>

      <div class="postcode-container">
        <div class="postcode-content">
          <div class="postcode-info">
        <h2 class="postcode-title">Input Your Postcode</h2>
        <p class="postcode-description">
          Get the corresponding weather and humidity information for your outdoor activities!
        </p>
          </div>

          <div class="postcode-form">
            <div class="input-wrapper" :class="{ 'input-active': isInputActive, 'error': apiError }">
              <div class="input-icon">📍</div>
          <input
            type="text"
            v-model="postcode"
            placeholder="Enter postcode..."
            maxlength="4"
            @input="validatePostcode"
                @focus="isInputActive = true"
                @blur="isInputActive = false"
          />
          <div class="check-mark" v-if="postcode.length === 4 && !isNaN(postcode) && !apiError">✓</div>
        </div>

        <div v-if="apiError" class="error-message">
          {{ apiError }}
        </div>

        <button
          @click="searchWeather"
          :disabled="isLoading || postcode.length !== 4 || isNaN(postcode)"
          class="search-btn"
        >
              <div class="btn-content">
                <span v-if="!isLoading">Search Now</span>
                <span v-else>Loading...</span>
                <span class="arrow-icon" v-if="!isLoading">→</span>
                <span class="loading-spinner" v-else></span>
              </div>
              <div class="btn-background"></div>
        </button>
          </div>
      </div>

        <div class="postcode-decoration">
          <div class="decoration-circle decoration-circle-1"></div>
          <div class="decoration-circle decoration-circle-2"></div>
          <div class="decoration-circle decoration-circle-3"></div>
          <div class="decoration-circle decoration-circle-4"></div>
          <div class="decoration-circle decoration-circle-5"></div>
        </div>
      </div>

      <div v-if="isLoading" class="loading">
        <div class="loading-spinner"></div>
        <span>Loading weather data...</span>
      </div>

      <div v-if="apiError" class="error-message">
        {{ apiError }}
      </div>

      <div v-if="weatherData && !isLoading" class="weather-display">
        <!-- Weather and Charts Row -->
        <div class="info-charts-container">
          <!-- Weather Card -->
          <div class="weather-card">
            <h3 class="card-title">
              Current Weather
              <span class="update-badge" v-if="weatherData.fromCache">Updated</span>
            </h3>
          <div class="date-header">
              <p>{{ weatherData.date }}</p>
              <h3>Weather in {{ weatherData.location }}</h3>
              <div class="location-info">
                <span class="location-tag">🏙️ {{ weatherData.location }}</span>
                <span class="time-tag">🕒 Real-time data</span>
              </div>
          </div>

          <div class="weather-icon-container">
            <img
                v-lazy="weatherData.icon"
                :alt="weatherData.weather"
              class="weather-icon"
            />
              <div class="weather-status">{{ weatherData.weather }}</div>
          </div>

          <div class="weather-details">
              <div class="detail-card">
                <span class="detail-icon">🌡️</span>
                <div class="detail-info">
                  <div class="detail-label">Temperature Range</div>
                  <div class="detail-value">{{ weatherData.temperature.min }}°C - {{ weatherData.temperature.max }}°C</div>
          </div>
                <div class="detail-tip">{{ getTemperatureTip() }}</div>
        </div>

              <div class="detail-card">
                <span class="detail-icon">☁️</span>
                <div class="detail-info">
                  <div class="detail-label">Weather Condition</div>
                  <div class="detail-value">{{ weatherData.weather }}</div>
            </div>
                <div class="detail-tip" v-if="getWeatherTip()">{{ getWeatherTip() }}</div>
              </div>

              <div class="detail-card">
                <span class="detail-icon">💧</span>
                <div class="detail-info">
                  <div class="detail-label">Current Humidity</div>
                  <div class="detail-value">{{ weatherData.humidity }}%</div>
                </div>
                <div class="detail-tip">{{ getHumidityTip() }}</div>
              </div>
            </div>
          </div>

          <!-- Charts Card -->
          <div class="charts-card">
            <h3 class="card-title">
              Weather Trends
              <div class="chart-actions">
                <button class="refresh-btn" @click="refreshData" :disabled="isLoading">
                  <span class="refresh-icon">🔄</span>
                  <span v-if="isLoading">Updating...</span>
                  <span v-else>Refresh</span>
                </button>
              </div>
            </h3>

            <div class="weather-trends">
              <div class="charts-header">
                <button 
                  :class="['chart-tab', { active: activeChart === 'humidity' }]"
                  @click="switchChart('humidity')"
                >
                  <span class="tab-icon">💧</span>
                  Humidity Flow
                </button>
                <button 
                  :class="['chart-tab', { active: activeChart === 'temperature' }]"
                  @click="switchChart('temperature')"
                >
                  <span class="tab-icon">🌡️</span>
                  Temperature Flow
                </button>
              </div>

              <div class="chart-container">
                <div v-show="activeChart === 'humidity'" class="chart-wrapper">
                  <canvas ref="humidityChartRef"></canvas>
                </div>

                <div v-show="activeChart === 'temperature'" class="chart-wrapper">
              <canvas ref="temperatureChartRef"></canvas>
            </div>
            </div>

              <div class="trend-cards">
                <div class="trend-card">
                  <div class="trend-header">
                    <span class="trend-icon">🌡️</span>
                    <h4>Temperature Trend</h4>
                  </div>
                  <div class="trend-value">
                    {{ weatherData.temperature.min }}°C - {{ weatherData.temperature.max }}°C
                  </div>
                  <div class="trend-tip">{{ getTemperatureTip() }}</div>
                </div>

                <div class="trend-card">
                  <div class="trend-header">
                    <span class="trend-icon">💧</span>
                    <h4>Humidity Trend</h4>
                  </div>
                  <div class="trend-value">{{ getHumidityRange() }}</div>
                  <div class="trend-tip">{{ getHumidityTip() }}</div>
                </div>

                <div class="trend-card highlight">
                  <div class="trend-header">
                    <span class="trend-icon">⭐</span>
                    <h4>Optimal Activity Time</h4>
                  </div>
                  <div class="trend-value">{{ weatherData.bestTimeOutside }}</div>
                  <div class="trend-tip">{{ getActivityRecommendation() }}</div>
                </div>
              </div>
            </div>
          </div>
        </div>

        <!-- Risk Information -->
        <div class="risk-section" :class="getCurrentHumidityClass()">
          <div class="animated-background">
            <div class="circle circle-1"></div>
            <div class="circle circle-2"></div>
            <div class="circle circle-3"></div>
            <div class="circle circle-4"></div>
            <div class="circle circle-5"></div>
          </div>
          <div class="risk-content">
          <div class="risk-emoji">{{ getCurrentHumidityEmoji() }}</div>
          <h2>{{ getCurrentHumidityLevel().riskLevel }}</h2>
          <p class="risk-description">{{ getCurrentHumidityDescription() }}</p>

          <button type="button" @click.prevent="toggleSummary" class="summary-btn">
              <div class="btn-content">
            <span>The Meaning of Different Humidity</span>
            <span class="arrow-icon" :class="{ 'arrow-rotated': showSummary }">→</span>
              </div>
              <div class="btn-background"></div>
          </button>
          </div>
        </div>

        <!-- Summary Section -->
        <div v-show="showSummary" class="summary-section">
          <div class="summary-header">
            <h3 class="summary-title">Humidity Level Guide</h3>
            <button type="button" @click.prevent="toggleSummary" class="close-btn">
              <span class="close-icon">×</span>
            </button>
          </div>
          
          <div class="humidity-carousel">
            <!-- Current Level Card -->
            <div v-if="weatherData" class="current-level-card">
              <div class="current-level-header">
                <span class="current-badge">Current Level</span>
                <div class="current-humidity">{{ weatherData.humidity }}%</div>
              </div>
              <div class="current-level-content">
                <div class="level-emoji">{{ getCurrentHumidityEmoji() }}</div>
                <div class="level-info">
                  <h4>{{ getCurrentHumidityLevel().riskLevel }}</h4>
                  <p>{{ getCurrentHumidityDescription() }}</p>
                </div>
              </div>
            </div>

            <div class="humidity-levels">
              <div class="level-row" :class="{ 'active-level': isCurrentLevel('Below 15%') }">
                <div class="level-emoji">😊</div>
                <div class="level-info">
                  <div class="level-range">Below 15%</div>
                  <div class="level-description">
                    <h4>Low Humidity Environment</h4>
                    <div class="description-content">
                      <p class="main-desc">In this humidity range, arthritis symptoms are typically mild, but other health impacts should be monitored.</p>
                      
                      <div class="detail-section">
                        <h5>🌟 Positive Effects</h5>
                        <ul>
                          <li>Less joint pain and stiffness</li>
                          <li>Lower joint stress during activities</li>
                          <li>Reduced weather-related pain</li>
                        </ul>
                      </div>

                      <div class="detail-section">
                        <h5>⚠️ Watch Out For</h5>
                        <ul>
                          <li>Potential skin dryness</li>
                          <li>Respiratory discomfort</li>
                          <li>Reduced joint lubrication</li>
                        </ul>
                      </div>

                      <div class="detail-section">
                        <h5>💡 Recommendations</h5>
                        <ul>
                          <li>Use a humidifier indoors</li>
                          <li>Stay well hydrated</li>
                          <li>Use moisturizing products</li>
                          <li>Engage in moderate indoor activities</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="level-row" :class="{ 'active-level': isCurrentLevel('15% - 30%') }">
                <div class="level-emoji">😃</div>
                <div class="level-info">
                  <div class="level-range">15% - 30%</div>
                  <div class="level-description">
                    <h4>Moderately Low Humidity</h4>
                    <div class="description-content">
                      <p class="main-desc">This humidity range is relatively comfortable for arthritis patients but still requires attention.</p>
                      
                      <div class="detail-section">
                        <h5>🌟 Benefits</h5>
                        <ul>
                          <li>Good joint mobility</li>
                          <li>Suitable for outdoor activities</li>
                          <li>Minimal pain levels</li>
                        </ul>
                      </div>

                      <div class="detail-section">
                        <h5>💡 Guidelines</h5>
                        <ul>
                          <li>Maintain regular exercise</li>
                          <li>Stay hydrated</li>
                          <li>Use appropriate protection</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="level-row" :class="{ 'active-level': isCurrentLevel('30% - 45%') }">
                <div class="level-emoji">🙂</div>
                <div class="level-info">
                  <div class="level-range">30% - 45%</div>
                  <div class="level-description">
                    <h4>Optimal Humidity</h4>
                    <div class="description-content">
                      <p class="main-desc">This is the ideal humidity range for arthritis patients' activities.</p>
                      
                      <div class="detail-section">
                        <h5>🌟 Optimal Conditions</h5>
                        <ul>
                          <li>Maximum joint flexibility</li>
                          <li>Minimal pain sensation</li>
                          <li>Suitable for all activities</li>
                        </ul>
                      </div>

                      <div class="detail-section">
                        <h5>💡 Suggested Activities</h5>
                        <ul>
                          <li>Outdoor exercises</li>
                          <li>Enjoy sunshine activities</li>
                          <li>Maintain exercise routine</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="level-row" :class="{ 'active-level': isCurrentLevel('45% - 55%') }">
                <div class="level-emoji">😐</div>
                <div class="level-info">
                  <div class="level-range">45% - 55%</div>
                  <div class="level-description">
                    <h4>Moderately High Humidity</h4>
                    <div class="description-content">
                      <p class="main-desc">In this humidity range, joint health needs attention and activity intensity should be adjusted.</p>
                      
                      <div class="detail-section">
                        <h5>⚠️ Potential Effects</h5>
                        <ul>
                          <li>Possible mild joint discomfort</li>
                          <li>Increased fatigue during activities</li>
                          <li>Weather-sensitive symptoms</li>
                        </ul>
                      </div>

                      <div class="detail-section">
                        <h5>💡 Key Recommendations</h5>
                        <ul>
                          <li>Adjust exercise intensity</li>
                          <li>Choose indoor activities</li>
                          <li>Prepare protective gear</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>

              <div class="level-row" :class="{ 'active-level': isCurrentLevel('Above 55%') }">
                <div class="level-emoji">🙁</div>
                <div class="level-info">
                  <div class="level-range">Above 55%</div>
                  <div class="level-description">
                    <h4>High Humidity</h4>
                    <div class="description-content">
                      <p class="main-desc">This humidity range may intensify arthritis symptoms and requires special attention to physical condition.</p>
                      
                      <div class="detail-section">
                        <h5>⚠️ Key Concerns</h5>
                        <ul>
                          <li>Increased joint pain</li>
                          <li>Limited mobility</li>
                          <li>Affected sleep quality</li>
                        </ul>
                      </div>

                      <div class="detail-section">
                        <h5>💡 Special Recommendations</h5>
                        <ul>
                          <li>Prioritize indoor activities</li>
                          <li>Use dehumidification</li>
                          <li>Maintain ventilation</li>
                          <li>Keep pain relief medication handy</li>
                        </ul>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>

    <AppFooter />
  </div>
</template>

<script setup>
import { ref, watch, nextTick } from 'vue'
import Chart from 'chart.js/auto'
import NavBar from '@/components/NavBar.vue'
import AppFooter from '@/components/AppFooter.vue'

const postcode = ref('')
const isLoading = ref(false)
const apiError = ref(null)
const weatherData = ref(null)
const humidityChartRef = ref(null)
const temperatureChartRef = ref(null)
const showSummary = ref(false)
const activeChart = ref('humidity')
const lastRefreshTime = ref(new Date().toLocaleTimeString())
const isInputActive = ref(false)
let humidityChart = null
let temperatureChart = null

function validatePostcode() {
  // Remove any non-digit characters
  postcode.value = postcode.value.replace(/\D/g, '')
  apiError.value = null

  if (postcode.value.length > 4) {
    postcode.value = postcode.value.substring(0, 4)
  }
}

function getHumidityRange() {
  if (!weatherData.value || !weatherData.value.humidityFlow) return '45% - 65%'

  const humidityValues = weatherData.value.humidityFlow.map((item) => item.humidity)
  const min = Math.min(...humidityValues)
  const max = Math.max(...humidityValues)
  return `${min}% - ${max}%`
}

function getCurrentHumidityLevel() {
  if (!weatherData.value) return { riskLevel: '' }

  const humidity = weatherData.value.humidity

  if (humidity < 15) return { riskLevel: 'Below 15%' }
  if (humidity >= 15 && humidity < 30) return { riskLevel: '15% - 30%' }
  if (humidity >= 30 && humidity < 45) return { riskLevel: '30% - 45%' }
  if (humidity >= 45 && humidity < 55) return { riskLevel: '45% - 55%' }
  return { riskLevel: 'Above 55%' }
}

function getCurrentHumidityEmoji() {
  if (!weatherData.value) return '😐'

  const humidity = weatherData.value.humidity

  if (humidity < 15) return '😊'
  if (humidity >= 15 && humidity < 30) return '😃'
  if (humidity >= 30 && humidity < 45) return '🙂'
  if (humidity >= 45 && humidity < 55) return '😐'
  return '🙁'
}

function getCurrentHumidityDescription() {
  if (!weatherData.value) return ''

  const humidity = weatherData.value.humidity

  if (humidity < 15) {
    return 'Low risk of weather-related arthritis pain and severe pain'
  }
  if (humidity >= 15 && humidity < 30) {
    return 'Moderate risk of weather-related arthritis pain and severe pain'
  }
  if (humidity >= 30 && humidity < 45) {
    return 'Arthritis pain will not have a significant influence by the weather'
  }
  if (humidity >= 45 && humidity < 55) {
    return 'Risk of weather-related arthritis pain will increase'
  }
  return 'High risk of weather-related arthritis and more likely have severe pain'
}

function getCurrentHumidityClass() {
  if (!weatherData.value) return ''

  const humidity = weatherData.value.humidity

  if (humidity < 15) return 'risk-low'
  if (humidity >= 15 && humidity < 30) return 'risk-low-moderate'
  if (humidity >= 30 && humidity < 45) return 'risk-moderate'
  if (humidity >= 45 && humidity < 55) return 'risk-moderate-high'
  return 'risk-high'
}

function toggleSummary() {
  showSummary.value = !showSummary.value
}

async function fetchWeatherData() {
  try {
    isLoading.value = true
    apiError.value = null

    // Check postcode format first
    if (!/^\d{4}$/.test(postcode.value)) {
      throw new Error('INVALID_FORMAT')
    }

    const url = `https://api.arthritisease.org/getWeatherData/?postcode=${postcode.value}`

    console.log('Fetching weather data from:', url)
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        'Origin': window.location.origin
      },
      mode: 'cors'
    }).catch(() => {
      throw new Error('NETWORK_ERROR')
    })

    if (!response.ok) {
      if (response.status === 400) {
        throw new Error('INVALID_POSTCODE')
      } else if (response.status === 404) {
        throw new Error('POSTCODE_NOT_FOUND')
      } else if (response.status === 429) {
        throw new Error('TOO_MANY_REQUESTS')
      }
      throw new Error('SERVER_ERROR')
    }

    const data = await response.json()
    console.log('Weather data received:', data)

    if (!data || !data.location) {
      throw new Error('NO_WEATHER_DATA')
    }

    weatherData.value = data
    return data
  } catch (error) {
    console.error('Failed to fetch weather data:', error)

    switch(error.message) {
      case 'INVALID_FORMAT':
        apiError.value = 'Please enter a valid 4-digit postcode'
        break
      case 'INVALID_POSTCODE':
        apiError.value = 'This postcode appears to be invalid. Please check and try again'
        break
      case 'POSTCODE_NOT_FOUND':
        apiError.value = 'This postcode does not exist in our database. Please verify it exists'
        break
      case 'TOO_MANY_REQUESTS':
        apiError.value = 'Please wait a moment before trying again'
        break
      case 'NO_WEATHER_DATA':
        apiError.value = 'No weather data available for this postcode. Please try another one'
        break
      case 'NETWORK_ERROR':
        apiError.value = 'This postcode does not exist. Please check and try again'
        break
      case 'SERVER_ERROR':
      default:
        apiError.value = 'Server error. Please try again later'
        break
    }

    weatherData.value = null
    return null
  } finally {
    isLoading.value = false
  }
}

async function searchWeather() {
  if (postcode.value.length === 4 && !isNaN(postcode.value)) {
    const data = await fetchWeatherData()
    if (data) {
      nextTick(() => {
        createHumidityChart()
        createTemperatureChart()
      })
    }
  } else {
    apiError.value = 'Please enter a valid 4-digit postcode'
    weatherData.value = null
  }
}

function isCurrentLevel(range) {
  if (!weatherData.value) return false

  const humidity = weatherData.value.humidity

  if (range === 'Below 15%') return humidity < 15
  if (range === '15% - 30%') return humidity >= 15 && humidity < 30
  if (range === '30% - 45%') return humidity >= 30 && humidity < 45
  if (range === '45% - 55%') return humidity >= 45 && humidity < 55
  if (range === 'Above 55%') return humidity >= 55

  return false
}

function createHumidityChart() {
  if (!weatherData.value || !weatherData.value.humidityFlow || !humidityChartRef.value) return

  if (humidityChart) {
    humidityChart.destroy()
  }

  const ctx = humidityChartRef.value.getContext('2d')

  const times = weatherData.value.humidityFlow.map((item) => item.time)
  const humidityValues = weatherData.value.humidityFlow.map((item) => item.humidity)

  humidityChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: times,
      datasets: [
        {
          label: 'Humidity (%)',
          data: humidityValues,
          borderColor: '#8bb978',
          backgroundColor: 'rgba(139, 185, 120, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          borderWidth: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: false,
          min: Math.min(...humidityValues) - 5 > 0 ? Math.min(...humidityValues) - 5 : 0,
          max: Math.max(...humidityValues) + 5,
          grid: {
            display: false,
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  })
}

function createTemperatureChart() {
  if (!weatherData.value || !weatherData.value.temperatureFlow || !temperatureChartRef.value) return

  if (temperatureChart) {
    temperatureChart.destroy()
  }

  const ctx = temperatureChartRef.value.getContext('2d')

  const times = weatherData.value.temperatureFlow.map((item) => item.time)
  const temperatureValues = weatherData.value.temperatureFlow.map((item) => item.temperature)

  temperatureChart = new Chart(ctx, {
    type: 'line',
    data: {
      labels: times,
      datasets: [
        {
          label: 'Temperature (°C)',
          data: temperatureValues,
          borderColor: '#8bb978',
          backgroundColor: 'rgba(139, 185, 120, 0.1)',
          tension: 0.4,
          fill: true,
          pointRadius: 0,
          borderWidth: 3,
        },
      ],
    },
    options: {
      responsive: true,
      maintainAspectRatio: true,
      scales: {
        y: {
          beginAtZero: false,
          min: Math.min(...temperatureValues) - 2,
          max: Math.max(...temperatureValues) + 2,
          grid: {
            display: false,
          },
        },
        x: {
          grid: {
            display: false,
          },
        },
      },
      plugins: {
        legend: {
          display: false,
        },
      },
    },
  })
}

function switchChart(chart) {
  activeChart.value = chart
}

watch(weatherData, () => {
  if (weatherData.value) {
    nextTick(() => {
      createHumidityChart()
      createTemperatureChart()
    })
  }
})

async function refreshData() {
  if (postcode.value) {
    await searchWeather()
    lastRefreshTime.value = new Date().toLocaleTimeString()
  }
}

function getWeatherTip() {
  if (!weatherData.value) return ''
  const weather = weatherData.value.weather.toLowerCase()
  
  if (weather.includes('rain')) {
    return 'Rainy conditions may increase joint pain. Stay dry and warm. Consider indoor activities. If you must go out, wear waterproof clothing and use an umbrella.'
  } else if (weather.includes('cloud')) {
    return 'Cloudy weather is generally good for outdoor activities. UV exposure is lower, but still wear sunscreen. Temperature changes may be less noticeable.'
  } else if (weather.includes('clear') || weather.includes('sunny')) {
    return 'Sunny weather is great for vitamin D! Use SPF 30+ sunscreen, wear a hat, and stay hydrated. Best to exercise in early morning or late afternoon.'
  } else if (weather.includes('storm')) {
    return 'Stormy weather can significantly affect joint pain. Stay indoors, keep warm, and consider gentle indoor exercises. Monitor weather updates.'
  } else if (weather.includes('snow')) {
    return 'Cold and snowy conditions can increase joint stiffness. Wear warm layers, avoid slippery areas, and consider indoor activities. Keep your joints warm.'
  }
  return 'Monitor how weather changes affect your joints and adjust activities accordingly.'
}

function getHumidityTip() {
  if (!weatherData.value) return ''
  const humidity = weatherData.value.humidity
  
  if (humidity < 30) {
    return `Low humidity (${humidity}%) can cause:
• Increased joint stiffness
• Dry skin and respiratory issues
Recommendations:
• Use a humidifier indoors
• Stay well-hydrated
• Apply moisturizer to protect skin
• Consider indoor exercises
• Monitor joint comfort`
  } else if (humidity > 60) {
    return `High humidity (${humidity}%) may:
• Increase joint pain and inflammation
• Make breathing feel more difficult
• Increase risk of dehydration
Recommendations:
• Use air conditioning or dehumidifier
• Choose indoor activities during peak humidity
• Stay hydrated
• Wear light, breathable clothing
• Monitor symptoms closely`
  }
  return `Optimal humidity (${humidity}%) for joint comfort:
• Good conditions for outdoor activities
• Maintain regular exercise routine
• Stay hydrated
• Monitor any changes in joint comfort
• Perfect time for gentle stretching`
}

function getTemperatureTip() {
  if (!weatherData.value) return ''
  const temp = (weatherData.value.temperature.max + weatherData.value.temperature.min) / 2
  
  if (temp < 10) {
    return `Cold temperature (${temp}°C) considerations:
• Increased risk of joint stiffness
• Longer warm-up needed
Recommendations:
• Wear warm, layered clothing
• Perform indoor exercises
• Use heat therapy before activities
• Gentle stretching is essential
• Keep joints warm and protected`
  } else if (temp > 25) {
    return `Warm temperature (${temp}°C) considerations:
• Risk of dehydration
• Increased fatigue possible
Recommendations:
• Exercise during cooler hours
• Stay well-hydrated
• Wear light, breathable clothing
• Use sun protection
• Monitor exertion levels`
  }
  return `Ideal temperature (${temp}°C) for activities:
• Perfect for outdoor exercises
• Maintain regular routine
• Stay hydrated
• Monitor comfort levels
• Enjoy moderate activity`
}

function getActivityRecommendation() {
  if (!weatherData.value) return ''
  const { humidity, temperature } = weatherData.value
  const avgTemp = (temperature.max + temperature.min) / 2

  let recommendation = 'Activity Recommendations:\n'

  // Temperature-based recommendations
  if (avgTemp < 10) {
    recommendation += '• Indoor exercises recommended\n• Warm up thoroughly\n• Focus on flexibility\n'
  } else if (avgTemp > 25) {
    recommendation += '• Early morning or evening activities\n• Light to moderate intensity\n• Pool exercises ideal\n'
  } else {
    recommendation += '• Ideal for outdoor activities\n• Regular exercise routine\n• All activity types suitable\n'
  }

  // Humidity-based additions
  if (humidity < 30) {
    recommendation += '• Indoor humidity-controlled environment\n• Stay hydrated\n• Monitor breathing comfort\n'
  } else if (humidity > 60) {
    recommendation += '• Reduce activity intensity\n• Indoor climate-controlled exercise\n• Extra hydration needed\n'
  } else {
    recommendation += '• Optimal conditions\n• Regular intensity suitable\n• Normal hydration needs\n'
  }

  return recommendation
}
</script>

<style scoped>
.humidity-page {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ea 0%, #ffffff 50%, #e8f3e0 100%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;  /* 添加左对齐 */
}

.container {
  width: 100%;  /* 改为100%宽度 */
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
  text-align: left;  /* 添加左对齐 */
}

.subtitle {
  color: #666;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  text-align: left;  /* 添加左对齐 */
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
    margin: 0;  /* 确保在移动端也靠左对齐 */
  }

  h1 {
    font-size: 2rem;
  }
}

/* Postcode input section */
.postcode-container {
  position: relative;
  background: linear-gradient(135deg, #cad9a1 0%, #a5c77f 100%);
  padding: 40px;
  border-radius: 16px;
  margin-bottom: 40px;
  box-shadow: 0 15px 35px rgba(165, 199, 127, 0.2);
  overflow: hidden;
  transition: all 0.3s ease;
}

.postcode-container:hover {
  box-shadow: 0 20px 40px rgba(165, 199, 127, 0.3);
  transform: translateY(-2px);
}

.postcode-content {
  position: relative;
  z-index: 2;
  display: flex;
  justify-content: space-between;
  align-items: center;
  gap: 40px;
}

.postcode-info {
  flex: 1;
}

.postcode-title {
  position: relative;
  font-size: 2.2rem;
  color: #fff;
  margin: 0 0 20px 0;
  display: inline-block;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.postcode-title::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -8px;
  width: 60px;
  height: 4px;
  background: rgba(255, 255, 255, 0.6);
  border-radius: 4px;
  transition: all 0.3s ease;
}

.postcode-container:hover .postcode-title::after {
  width: 100%;
  background: rgba(255, 255, 255, 0.8);
}

.postcode-description {
  color: rgba(255, 255, 255, 0.9);
  margin-bottom: 0;
  max-width: 500px;
  line-height: 1.6;
  font-size: 1.1rem;
  transition: all 0.3s ease;
}

.postcode-form {
  display: flex;
  flex-direction: column;
  gap: 15px;
  flex: 1;
  max-width: 400px;
}

.input-wrapper {
  position: relative;
  width: 100%;
  display: flex;
  align-items: center;
  background-color: white;
  border-radius: 12px;
  padding: 0 15px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  overflow: hidden;
}

.input-wrapper.error {
  border-color: #ff6b6b;
  animation: shake 0.5s cubic-bezier(0.36, 0.07, 0.19, 0.97) both;
}

@keyframes shake {
  10%, 90% {
    transform: translate3d(-1px, 0, 0);
  }
  20%, 80% {
    transform: translate3d(2px, 0, 0);
  }
  30%, 50%, 70% {
    transform: translate3d(-4px, 0, 0);
  }
  40%, 60% {
    transform: translate3d(4px, 0, 0);
  }
}

.error-message {
  background: #fff5f5;
  color: #e53e3e;
  padding: 12px 16px;
  border-radius: 8px;
  margin: 16px 0;
  display: flex;
  align-items: center;
  gap: 8px;
  border: 1px solid #fed7d7;
  font-size: 0.95rem;
  animation: slideIn 0.3s ease-out;
}

.error-message::before {
  content: '⚠️';
  font-size: 1.2rem;
}

@keyframes slideIn {
  from {
    transform: translateY(-10px);
    opacity: 0;
  }
  to {
    transform: translateY(0);
    opacity: 1;
  }
}

.input-wrapper::before {
  content: '';
  position: absolute;
  top: 0;
  left: -100%;
  width: 100%;
  height: 100%;
  background: linear-gradient(
    90deg,
    transparent,
    rgba(255, 255, 255, 0.2),
    transparent
  );
  transition: all 0.5s ease;
}

.input-wrapper:hover::before {
  left: 100%;
}

.input-wrapper.input-active {
  border-color: #4a6741;
  box-shadow: 0 8px 25px rgba(74, 103, 65, 0.15);
  transform: translateY(-2px);
}

.input-icon {
  font-size: 1.4rem;
  color: #4a6741;
  margin-right: 12px;
  transition: all 0.3s ease;
  transform-style: preserve-3d;
  perspective: 1000px;
}

.input-active .input-icon {
  animation: icon-rotate-in 0.6s ease-out forwards;
}

.input-wrapper:not(.input-active) .input-icon {
  animation: icon-rotate-out 0.6s ease-out forwards;
}

@keyframes icon-rotate-in {
  0% {
    transform: rotateY(0deg);
  }
  100% {
    transform: rotateY(360deg);
  }
}

@keyframes icon-rotate-out {
  0% {
    transform: rotateY(360deg);
  }
  100% {
    transform: rotateY(0deg);
  }
}

.input-wrapper input {
  width: 100%;
  padding: 16px 0;
  border: none;
  outline: none;
  font-size: 1.1rem;
  color: #333;
  background-color: transparent;
  /* 添加以下属性来移除竖线 */
  -webkit-appearance: none;
  -moz-appearance: textfield;
  appearance: none;
  -webkit-text-fill-color: currentColor;
}

.input-wrapper input:focus {
  outline: none;
  border: none;
  box-shadow: none;
  -webkit-appearance: none;
  -moz-appearance: textfield;
  appearance: none;
}

.check-mark {
  position: absolute;
  right: 15px;
  top: 50%;
  transform: translateY(-50%) scale(0);
  color: #4a6741;
  font-weight: bold;
  font-size: 1.4rem;
  animation: pop-in 0.3s ease forwards;
}

@keyframes pop-in {
  0% {
    transform: translateY(-50%) scale(0);
    opacity: 0;
  }
  70% {
    transform: translateY(-50%) scale(1.2);
    opacity: 0.7;
  }
  100% {
    transform: translateY(-50%) scale(1);
    opacity: 1;
  }
}

.search-btn {
  position: relative;
  width: 100%;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
}

.search-btn .btn-content {
  position: relative;
  z-index: 2;
  display: flex;
  align-items: center;
  justify-content: center;
  gap: 12px;
  padding: 16px 30px;
  font-size: 1.1rem;
  color: white;
  font-weight: 500;
}

.search-btn .btn-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: #4a6741;
  border-radius: 12px;
  transition: all 0.5s ease;
  z-index: 1;
}

.search-btn:not(:disabled):hover .btn-background {
  transform: scale(1.02);
  background: #3a5331;
  box-shadow: 
    0 5px 15px rgba(0, 0, 0, 0.1),
    0 0 20px rgba(255, 255, 255, 0.2),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.search-btn:not(:disabled):active .btn-background {
  transform: scale(0.98);
}

.search-btn .arrow-icon {
  display: inline-block;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.search-btn:not(:disabled):hover .arrow-icon {
  transform: translateX(5px);
}

.loading-spinner {
  width: 20px;
  height: 20px;
  border: 3px solid rgba(255, 255, 255, 0.3);
  border-radius: 50%;
  border-top-color: #fff;
  animation: spin 1s linear infinite;
}

@keyframes spin {
  0% { transform: rotate(0deg); }
  100% { transform: rotate(360deg); }
}

.decoration-circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.2);
  transition: all 0.5s ease;
}

.decoration-circle-1 {
  width: 180px;
  height: 180px;
  top: -60px;
  right: -30px;
  animation-delay: 0s;
}

.decoration-circle-2 {
  width: 120px;
  height: 120px;
  bottom: 30px;
  right: 100px;
  animation-delay: -5s;
}

.decoration-circle-3 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  left: 30%;
  animation-delay: -10s;
}

.decoration-circle-4 {
  width: 100px;
  height: 100px;
  top: 40%;
  left: 10%;
  animation-delay: -15s;
}

.decoration-circle-5 {
  width: 140px;
  height: 140px;
  top: 20%;
  right: 20%;
  animation-delay: -7s;
}

@keyframes float-decoration {
  0% {
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.3;
  }
  25% {
    transform: translate(10px, 15px) rotate(90deg) scale(1.1);
    opacity: 0.4;
  }
  50% {
    transform: translate(15px, -10px) rotate(180deg) scale(1);
    opacity: 0.3;
  }
  75% {
    transform: translate(-10px, 10px) rotate(270deg) scale(1.1);
    opacity: 0.4;
  }
  100% {
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.3;
  }
}

@media (max-width: 768px) {
  .postcode-container {
    padding: 30px 20px;
  }

  .postcode-content {
    flex-direction: column;
  text-align: center;
    gap: 30px;
}

  .postcode-title {
    font-size: 1.8rem;
  }

  .postcode-title::after {
    left: 50%;
    transform: translateX(-50%);
  }
  
  .postcode-form {
    max-width: 100%;
    width: 100%;
}

  .postcode-description {
    max-width: 100%;
    font-size: 1rem;
  }

  .input-wrapper input {
    padding: 14px 0;
    font-size: 1rem;
  }

  .search-btn .btn-content {
    padding: 14px 25px;
    font-size: 1rem;
  }

  .decoration-circle {
    opacity: 0.2;
  }
}

/* Weather display section */
.weather-display {
  display: flex;
  flex-direction: column;
  gap: 20px;
  margin-bottom: 30px;
}

.info-charts-container {
  display: grid;
  grid-template-columns: repeat(2, 1fr);
  gap: 24px;
  margin-bottom: 30px;
}

.weather-card, .charts-card {
  background: #ffffff;
  border-radius: 16px;
  padding: 24px;
  box-shadow: rgba(17, 12, 46, 0.15) 0px 48px 100px 0px;
  transition: all 0.3s ease;
  border: 2px solid #e8e8e8;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.weather-card::before, .charts-card::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  height: 4px;
  background: linear-gradient(90deg, #8bb978, #4a6741);
}

.weather-card:hover, .charts-card:hover {
  transform: translateY(-2px);
  box-shadow: rgba(17, 12, 46, 0.2) 0px 48px 120px 0px;
  border-color: #d0d0d0;
}

.card-title {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 20px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e8e8e8;
  font-weight: 600;
  position: relative;
}

.card-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #8bb978, #4a6741);
}

.charts-header {
  display: flex;
  gap: 12px;
  margin-bottom: 24px;
  padding: 6px;
  background: #edf1ea;
  border-radius: 12px;
  border: 1px solid #e0e5dd;
}

.chart-tab {
  flex: 1;
  padding: 12px 20px;
  border: none;
  background-color: transparent;
  color: #4a6741;
  border-radius: 8px;
  cursor: pointer;
  transition: all 0.3s ease;
  font-size: 1rem;
  font-weight: 500;
  text-align: center;
}

.chart-tab:hover {
  background-color: rgba(139, 185, 120, 0.15);
}

.chart-tab.active {
  background-color: #ffffff;
  color: #4a6741;
  box-shadow: 0 4px 12px rgba(74, 103, 65, 0.15);
  font-weight: 600;
}

.weather-details {
  margin-top: 24px;
}

.weather-details p {
  padding: 12px 16px;
  background: #f5f8f3;
  border: 1px solid #e0e5dd;
  border-radius: 8px;
  margin: 8px 0;
  display: flex;
  align-items: center;
  transition: all 0.3s ease;
}

.weather-details p:hover {
  background: #edf1ea;
  border-color: #d5dbd2;
}

.detail-icon {
  margin-right: 12px;
  font-size: 1.2rem;
}

.weather-icon-container {
  text-align: center;
  padding: 24px 0;
  margin: 16px 0;
  background: #f5f8f3;
  border: 1px solid #e0e5dd;
  border-radius: 12px;
  transition: all 0.3s ease;
}

.weather-icon-container:hover {
  background: #edf1ea;
  border-color: #d5dbd2;
}

.weather-icon {
  width: 100px;
  height: 100px;
}

.chart-insights {
  margin-top: 20px;
  padding: 16px;
  background: #f5f8f3;
  border: 1px solid #e0e5dd;
  border-radius: 8px;
}

.chart-insights p {
  margin: 8px 0;
  padding: 12px;
  border-radius: 6px;
  transition: all 0.3s ease;
  background: rgba(255, 255, 255, 0.6);
}

.chart-insights p:hover {
  background: #ffffff;
}

.date-header {
  background: #f5f8f3;
  padding: 16px;
  border-radius: 12px;
  border: 1px solid #e0e5dd;
  margin-bottom: 20px;
}

.date-header p {
  color: #666;
  margin: 0 0 8px 0;
}

.date-header h3 {
  color: #333;
  margin: 0;
  font-size: 1.2rem;
}

@media (max-width: 992px) {
  .info-charts-container {
    grid-template-columns: 1fr;
  }
  
  .weather-card, .charts-card {
    padding: 20px;
  }
  
  .chart-container {
    min-height: 250px;
  }
}

@media (max-width: 576px) {
  .weather-card, .charts-card {
    padding: 16px;
  }
  
  .card-title {
    font-size: 1.2rem;
  }
  
  .chart-tab {
    padding: 8px 12px;
    font-size: 0.9rem;
  }
}

/* Risk section */
.risk-section {
  grid-column: span 2;
  text-align: center;
  padding: 40px 20px;
  border-radius: 16px;
  margin-bottom: 30px;
  color: #fff;
  position: relative;
  overflow: hidden;
  z-index: 1;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.risk-section::before {
  content: '';
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  z-index: -1;
  transition: all 0.5s ease;
  opacity: 0.8;
}

.risk-low::before { 
  background: linear-gradient(135deg, #95c675 0%, #7ab55c 100%);
}

.risk-low-moderate::before { 
  background: linear-gradient(135deg, #8bb978 0%, #71a55f 100%);
}

.risk-moderate::before { 
  background: linear-gradient(135deg, #82ae7a 0%, #669657 100%);
}

.risk-moderate-high::before { 
  background: linear-gradient(135deg, #e9b857 0%, #d6a543 100%);
}

.risk-high::before { 
  background: linear-gradient(135deg, #e6923c 0%, #d67a23 100%);
}

.animated-background {
  position: absolute;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  overflow: hidden;
  z-index: 0;
}

.circle {
  position: absolute;
  border-radius: 50%;
  background: rgba(255, 255, 255, 0.15);
  box-shadow: inset 0 0 20px rgba(255, 255, 255, 0.2);
  transition: all 0.5s ease;
}

/* Common animation for all risk levels */
.risk-section .animated-background::before {
  content: '';
  position: absolute;
  top: -50%;
  left: -50%;
  width: 200%;
  height: 200%;
  background: radial-gradient(
    circle at center,
    rgba(255, 255, 255, 0.1) 0%,
    rgba(255, 255, 255, 0.05) 30%,
    transparent 70%
  );
  animation: rotate-gradient 15s linear infinite;
}

.risk-section .circle {
  animation: morph-float 12s infinite;
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
}

/* Risk level specific animations */
.risk-low .circle {
  animation: morph-float-low 12s infinite;
}

.risk-low-moderate .circle {
  animation: morph-float-low-moderate 12s infinite;
}

.risk-moderate .circle {
  animation: morph-float-moderate 12s infinite;
}

.risk-moderate-high .circle {
  animation: morph-float-moderate-high 12s infinite;
}

.risk-high .circle {
  animation: morph-float-high 12s infinite;
}

/* Circle positions and delays */
.circle-1 {
  width: 180px;
  height: 180px;
  top: -60px;
  right: -30px;
  animation-delay: 0s;
  animation-duration: 10s;
}

.circle-2 {
  width: 120px;
  height: 120px;
  bottom: 30px;
  right: 100px;
  animation-delay: -3s;
  animation-duration: 12s;
}

.circle-3 {
  width: 150px;
  height: 150px;
  bottom: -50px;
  left: 30%;
  animation-delay: -6s;
  animation-duration: 14s;
}

.circle-4 {
  width: 100px;
  height: 100px;
  top: 40%;
  left: 10%;
  animation-delay: -4s;
  animation-duration: 11s;
}

.circle-5 {
  width: 140px;
  height: 140px;
  top: 20%;
  right: 20%;
  animation-delay: -2s;
  animation-duration: 13s;
}

/* Animation keyframes for different risk levels */
@keyframes morph-float-low {
  0% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.2;
  }
  25% {
    border-radius: 60% 40% 30% 70%;
    transform: translate(10px, 15px) rotate(90deg) scale(1.05);
    opacity: 0.3;
  }
  50% {
    border-radius: 30% 60% 70% 40%;
    transform: translate(15px, -10px) rotate(180deg) scale(1);
    opacity: 0.2;
}
  75% {
    border-radius: 40% 70% 60% 30%;
    transform: translate(-10px, 10px) rotate(270deg) scale(1.05);
    opacity: 0.3;
  }
  100% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.2;
  }
}

@keyframes morph-float-low-moderate {
  0% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.25;
  }
  25% {
    border-radius: 55% 45% 35% 65%;
    transform: translate(12px, 18px) rotate(90deg) scale(1.08);
    opacity: 0.35;
  }
  50% {
    border-radius: 35% 55% 65% 45%;
    transform: translate(18px, -12px) rotate(180deg) scale(1);
    opacity: 0.25;
  }
  75% {
    border-radius: 45% 65% 55% 35%;
    transform: translate(-12px, 12px) rotate(270deg) scale(1.08);
    opacity: 0.35;
  }
  100% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.25;
  }
}

@keyframes morph-float-moderate {
  0% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.3;
  }
  25% {
    border-radius: 50% 50% 40% 60%;
    transform: translate(15px, 20px) rotate(90deg) scale(1.1);
    opacity: 0.4;
  }
  50% {
    border-radius: 40% 50% 60% 50%;
    transform: translate(20px, -15px) rotate(180deg) scale(1);
    opacity: 0.3;
  }
  75% {
    border-radius: 50% 60% 50% 40%;
    transform: translate(-15px, 15px) rotate(270deg) scale(1.1);
    opacity: 0.4;
}
  100% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.3;
  }
}

@keyframes morph-float-moderate-high {
  0% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.35;
  }
  25% {
    border-radius: 45% 55% 45% 55%;
    transform: translate(18px, 22px) rotate(90deg) scale(1.12);
    opacity: 0.45;
  }
  50% {
    border-radius: 45% 45% 55% 55%;
    transform: translate(22px, -18px) rotate(180deg) scale(1);
    opacity: 0.35;
  }
  75% {
    border-radius: 55% 55% 45% 45%;
    transform: translate(-18px, 18px) rotate(270deg) scale(1.12);
    opacity: 0.45;
  }
  100% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.35;
  }
}

@keyframes morph-float-high {
  0% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(0deg) scale(1);
    opacity: 0.4;
  }
  25% {
    border-radius: 40% 60% 40% 60%;
    transform: translate(30px, 35px) rotate(90deg) scale(1.25);
    opacity: 0.55;
  }
  50% {
    border-radius: 40% 40% 60% 60%;
    transform: translate(35px, -30px) rotate(180deg) scale(1);
    opacity: 0.4;
  }
  75% {
    border-radius: 60% 60% 40% 40%;
    transform: translate(-30px, 30px) rotate(270deg) scale(1.25);
    opacity: 0.55;
  }
  100% {
    border-radius: 50%;
    transform: translate(0, 0) rotate(360deg) scale(1);
    opacity: 0.4;
  }
}

@keyframes rotate-gradient {
  0% {
    transform: rotate(0deg);
  }
  100% {
    transform: rotate(360deg);
  }
}

.risk-content {
  position: relative;
  z-index: 2;
  padding: 20px;
  border-radius: 12px;
  background: rgba(255, 255, 255, 0.1);
  box-shadow: 0 8px 32px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
}

.risk-content:hover {
  transform: translateY(-2px);
  box-shadow: 0 12px 40px rgba(0, 0, 0, 0.15);
  background: rgba(255, 255, 255, 0.15);
}

.risk-emoji {
  font-size: 3.5rem;
  margin-bottom: 15px;
  position: relative;
  animation: bounce 2s infinite;
  text-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
}

.risk-section h2 {
  font-size: 2rem;
  margin: 15px 0;
  font-weight: 600;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.2);
  transition: all 0.3s ease;
}

.risk-description {
  font-size: 1.3rem;
  max-width: 700px;
  margin: 0 auto 25px;
  line-height: 1.5;
  text-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
}

.summary-btn {
  position: relative;
  background: none;
  border: none;
  padding: 0;
  cursor: pointer;
  overflow: hidden;
  transition: all 0.3s ease;
  transform-style: preserve-3d;
  perspective: 1000px;
}

.btn-content {
  position: relative;
  z-index: 2;
  display: inline-flex;
  align-items: center;
  gap: 10px;
  padding: 14px 30px;
  font-size: 1.1rem;
  color: white;
  font-weight: 500;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.btn-background {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  background: rgba(74, 103, 65, 0.9);
  border-radius: 12px;
  transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
  z-index: 1;
  backdrop-filter: blur(5px);
  transform-origin: center;
}

.summary-btn:hover .btn-background {
  transform: scale(1.02) translateZ(20px);
  background: rgba(58, 83, 49, 0.95);
  box-shadow: 
    0 5px 15px rgba(0, 0, 0, 0.1),
    0 0 20px rgba(255, 255, 255, 0.2),
    inset 0 0 15px rgba(255, 255, 255, 0.1);
}

.summary-btn:active .btn-background {
  transform: scale(0.98) translateZ(-10px);
}

.summary-btn:active .btn-content {
  transform: translateZ(-5px);
}

.arrow-icon {
  display: inline-block;
  transition: transform 0.5s cubic-bezier(0.4, 0, 0.2, 1);
}

.arrow-rotated {
  transform: rotate(90deg) translateZ(10px);
}

.summary-btn:hover .arrow-icon {
  animation: bounce-rotate 1s infinite;
}

@keyframes bounce-rotate {
  0%, 100% {
    transform: translateX(0) rotate(0deg);
  }
  50% {
    transform: translateX(5px) rotate(15deg);
  }
}

.risk-high {
  background: linear-gradient(135deg, #e6a23c 0%, #d4a76a 100%);
}

.risk-high .circle { 
  background: radial-gradient(circle at 30% 30%, rgba(255, 255, 255, 0.2), rgba(255, 255, 255, 0.1));
  animation-name: morph-float-high;
}

.risk-high .circle-1 {
  animation-delay: 0s;
  animation-duration: 6s;
}

.risk-high .circle-2 {
  animation-delay: -2s;
  animation-duration: 7s;
}

.risk-high .circle-3 {
  animation-delay: -4s;
  animation-duration: 8s;
}

.risk-high .circle-4 {
  animation-delay: -3s;
  animation-duration: 6.5s;
}

.risk-high .circle-5 {
  animation-delay: -1s;
  animation-duration: 7.5s;
}

.summary-btn::after {
  content: '';
  position: absolute;
  top: 50%;
  left: 50%;
  width: 0;
  height: 0;
  background: rgba(255, 255, 255, 0.2);
  border-radius: 50%;
  transform: translate(-50%, -50%);
  opacity: 0;
  z-index: 1;
  transition: all 0.5s ease;
}

.summary-btn:active::after {
  width: 200%;
  height: 200%;
  opacity: 1;
  transition: 0s;
}

.summary-section {
  background: #fff;
  border-radius: 12px;
  padding: 20px;
  margin-top: 20px;
  box-shadow: 0 2px 12px rgba(0, 0, 0, 0.1);
}

.summary-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.summary-title {
  font-size: 1.5rem;
  color: #333;
  margin: 0;
}

.close-btn {
  background: none;
  border: none;
  font-size: 1.5rem;
  color: #666;
  cursor: pointer;
  padding: 5px;
}

.humidity-carousel {
  overflow-y: auto;
  max-height: 480px;
}

.humidity-levels {
  display: flex;
  flex-direction: column;
  gap: 20px;
}

.level-row {
  display: flex;
  padding: 20px;
  border-radius: 12px;
  background: #f8f9fa;
  transition: all 0.3s ease;
}

.level-row:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.1);
}

.active-level {
  background: #f0f7ea;
  border-left: 4px solid #8bb978;
}

.level-emoji {
  font-size: 2rem;
  margin-right: 20px;
  display: flex;
  align-items: center;
}

.level-info {
  flex: 1;
}

.level-range {
  font-weight: bold;
  color: #4a6741;
  margin-bottom: 8px;
}

.level-description {
  color: #333;
}

.description-content {
  margin-top: 10px;
}

.main-desc {
  margin-bottom: 15px;
  color: #666;
}

.detail-section {
  margin-bottom: 15px;
}

.detail-section h5 {
  color: #4a6741;
  margin-bottom: 8px;
  font-size: 1rem;
}

.detail-section ul {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.detail-section li {
  margin-bottom: 5px;
  color: #666;
  padding-left: 20px;
  position: relative;
}

.detail-section li::before {
  content: "•";
  position: absolute;
  left: 0;
  color: #8bb978;
}

@media (max-width: 768px) {
  .level-row {
    flex-direction: column;
  }

  .level-emoji {
    margin-right: 0;
    margin-bottom: 10px;
  }

  .level-info {
    width: 100%;
}
}

.loading-dot {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: white;
  margin-left: 8px;
  animation: pulse-dot 1.4s cubic-bezier(0.4, 0, 0.6, 1) infinite;
}

@keyframes pulse-dot {
  0% { transform: scale(0.8); opacity: 0.6; }
  50% { transform: scale(1.2); opacity: 1; }
  100% { transform: scale(0.8); opacity: 0.6; }
}

.update-badge {
  font-size: 0.8rem;
  background: #4a6741;
  color: white;
  padding: 4px 8px;
  border-radius: 12px;
  margin-left: 10px;
  font-weight: normal;
}

.location-info {
  display: flex;
  gap: 12px;
  margin-top: 8px;
}

.location-tag, .time-tag {
  font-size: 0.9rem;
  color: #666;
  display: flex;
  align-items: center;
  gap: 4px;
}

.weather-status {
  margin-top: 12px;
  font-size: 1.2rem;
  color: #4a6741;
  font-weight: 500;
}

.detail-card {
  background: #ffffff;
  border: 1px solid #e0e5dd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 16px;
  transition: all 0.3s ease;
}

.detail-card:hover {
  border-color: #8bb978;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.detail-card.highlight {
  background: linear-gradient(135deg, #f0f7ea, #ffffff);
  border-color: #8bb978;
}

.detail-info {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.detail-label {
  color: #666;
  font-size: 0.9rem;
}

.detail-value {
  color: #333;
  font-size: 1.1rem;
  font-weight: 500;
}

.detail-tip {
  grid-column: 1 / -1;
  color: #4a6741;
  font-size: 0.9rem;
  padding-top: 8px;
  border-top: 1px dashed #e0e5dd;
}

.chart-actions {
  float: right;
}

.refresh-btn {
  background: none;
  border: 1px solid #e0e5dd;
  border-radius: 8px;
  padding: 6px 12px;
  font-size: 0.9rem;
  color: #4a6741;
  cursor: pointer;
  display: flex;
  align-items: center;
  gap: 6px;
  transition: all 0.3s ease;
}

.refresh-btn:hover:not(:disabled) {
  background: #f0f7ea;
  border-color: #8bb978;
}

.refresh-btn:disabled {
  opacity: 0.6;
  cursor: not-allowed;
}

.tab-icon {
  margin-right: 6px;
}

.insight-card {
  background: #ffffff;
  border: 1px solid #e0e5dd;
  border-radius: 12px;
  padding: 16px;
  margin-bottom: 12px;
  display: grid;
  grid-template-columns: auto 1fr;
  gap: 16px;
  transition: all 0.3s ease;
}

.insight-card:hover {
  border-color: #8bb978;
  transform: translateY(-2px);
  box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
}

.insight-content {
  display: flex;
  flex-direction: column;
  gap: 4px;
}

.insight-title {
  color: #666;
  font-size: 0.9rem;
}

.insight-value {
  color: #333;
  font-size: 1.1rem;
  font-weight: 500;
}

.insight-tip {
  color: #4a6741;
  font-size: 0.9rem;
  margin-top: 8px;
  padding-top: 8px;
  border-top: 1px dashed #e0e5dd;
}

.health-advisory {
  margin-top: 30px;
  padding: 24px;
  background: linear-gradient(135deg, #f9f9f9 0%, #f5f8f3 100%);
  border-radius: 16px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  border: 1px solid #e0e5dd;
}

.advisory-title {
  font-size: 1.4rem;
  color: #333;
  margin-bottom: 24px;
  padding-bottom: 12px;
  border-bottom: 2px solid #e0e5dd;
  font-weight: 600;
  position: relative;
  display: flex;
  align-items: center;
  gap: 10px;
}

.advisory-icon {
  font-size: 1.6rem;
}

.advisory-title::after {
  content: '';
  position: absolute;
  bottom: -2px;
  left: 0;
  width: 60px;
  height: 2px;
  background: linear-gradient(90deg, #8bb978, #4a6741);
}

.advisory-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}

.advisory-card {
  background-color: #ffffff;
  border-radius: 12px;
  padding: 20px;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.05);
  border: 1px solid #e0e5dd;
  transition: all 0.3s ease;
}

.advisory-card:hover {
  transform: translateY(-2px);
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.08);
  border-color: #8bb978;
}

.advisory-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 16px;
  padding-bottom: 12px;
  border-bottom: 1px dashed #e0e5dd;
}

.advisory-type {
  font-size: 1.1rem;
  color: #333;
  font-weight: 600;
}

.impact-level {
  font-size: 0.9rem;
  color: #fff;
  padding: 4px 12px;
  border-radius: 20px;
  font-weight: 500;
}

.impact-level.low {
  background-color: #8bb978;
}

.impact-level.moderate {
  background-color: #f0ad4e;
}

.impact-level.high {
  background-color: #d9534f;
}

.advisory-list {
  list-style: none;
  padding-left: 0;
  margin: 0;
}

.advisory-list li {
  position: relative;
  padding: 8px 0 8px 24px;
  border-bottom: 1px solid #f5f5f5;
  color: #555;
  font-size: 0.95rem;
  line-height: 1.4;
}

.advisory-list li:last-child {
  border-bottom: none;
}

.advisory-list li::before {
  content: '•';
  position: absolute;
  left: 8px;
  color: #8bb978;
  font-weight: bold;
}

.activity-item, .tip-item {
  display: flex;
  align-items: center;
  gap: 8px;
  transition: all 0.3s ease;
}

.activity-item:hover, .tip-item:hover {
  background-color: #f9f9f9;
  padding-left: 12px;
  border-radius: 4px;
}

@media (max-width: 992px) {
  .advisory-cards {
    grid-template-columns: 1fr;
  }

  .advisory-card {
    margin-bottom: 16px;
  }
}

@media (max-width: 576px) {
  .health-advisory {
    padding: 16px;
  }
  
  .advisory-title {
    font-size: 1.2rem;
  }
  
  .advisory-type {
    font-size: 1rem;
  }
  
  .advisory-list li {
    font-size: 0.9rem;
  }
}

.weather-trends {
  display: flex;
  flex-direction: column;
  gap: 24px;
}

.trend-cards {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 16px;
  margin-bottom: 24px;
}

.trend-card {
  background: #ffffff;
  border: 1px solid #e0e5dd;
  border-radius: 12px;
  padding: 16px;
  transition: all 0.3s ease;
  }

.trend-card:hover {
  border-color: #8bb978;
  transform: translateY(-1px);
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.03);
}

.trend-card.highlight {
  background: linear-gradient(135deg, #f0f7ea, #ffffff);
  border-color: #8bb978;
}

.trend-header {
  display: flex;
  align-items: center;
  gap: 8px;
  margin-bottom: 12px;
}

.trend-icon {
  font-size: 1.4rem;
}

.trend-header h4 {
  margin: 0;
  color: #333;
  font-size: 1rem;
  font-weight: 600;
}

.trend-value {
  font-size: 1.2rem;
  color: #4a6741;
  font-weight: 500;
  margin-bottom: 8px;
}

.trend-tip {
  font-size: 0.9rem;
  color: #666;
  line-height: 1.4;
}

.chart-container {
  background: #ffffff;
  border: 1px solid #e0e5dd;
  border-radius: 12px;
  padding: 20px;
  height: 300px;
  margin-bottom: 24px;
}

.chart-wrapper {
  height: 100%;
  width: 100%;
}

@media (max-width: 992px) {
  .trend-cards {
    grid-template-columns: 1fr;
  }

  .chart-container {
    height: 250px;
  }
}

@media (max-width: 576px) {
  .trend-card {
    padding: 12px;
  }
  
  .trend-header h4 {
    font-size: 0.9rem;
  }
  
  .trend-value {
    font-size: 1.1rem;
  }
  
  .trend-tip {
    font-size: 0.85rem;
  }
}

.current-level-card {
  background: linear-gradient(135deg, #f0f7ea, #ffffff);
  border: 2px solid #8bb978;
  border-radius: 16px;
  padding: 24px;
  margin-bottom: 30px;
  box-shadow: 0 4px 20px rgba(139, 185, 120, 0.15);
}

.current-level-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
}

.current-badge {
  background: #4a6741;
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  font-weight: 500;
}

.current-humidity {
  font-size: 2rem;
  font-weight: 600;
  color: #4a6741;
}

.current-level-content {
  display: flex;
  align-items: center;
  gap: 24px;
}

.current-level-content .level-emoji {
  font-size: 3rem;
  margin: 0;
}

.current-level-content .level-info h4 {
  font-size: 1.5rem;
  color: #333;
  margin: 0 0 10px 0;
  }

.current-level-content .level-info p {
  font-size: 1.1rem;
  color: #666;
  margin: 0;
  line-height: 1.4;
}

@media (max-width: 768px) {
  .current-level-content {
    flex-direction: column;
    text-align: center;
    gap: 16px;
  }

  .current-level-content .level-info h4 {
    font-size: 1.3rem;
  }

  .current-level-content .level-info p {
    font-size: 1rem;
  }
}

/* Remove Sara section styles */
.sara-section {
  display: none;
}

@media (max-width: 768px) {
  .sara-section {
    display: none;
  }
}
</style>


