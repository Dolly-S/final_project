<template>
  <div class="pain-check">
    <div class="form-container">
      <h2>Chronic Pain Grade Questionnaire (CPG) Of WHO</h2>

      <div class="question">
        <div class="question-header">
          <span class="question-number">1</span>
          <span class="question-title">Rate Current Pain</span>
        </div>
        <div class="question-subtitle">
          (0-10 scale at the present time, this is right now, where 0 is 'no pain' and 10 is 'pain
          as bad as it could be'?)
        </div>

        <div class="scale-container">
          <div class="scale-background">
            <div class="scale-numbers">
              <div class="scale-number left">0</div>
              <div class="scale-number right">10</div>
            </div>
            <div class="scale-slider">
              <div class="slider-track" :style="getSliderTrackStyle(answers[0])"></div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                v-model.number="answers[0]"
                class="slider"
                @input="saveAnswers"
                @mousemove="updateSlider"
                @mousedown="activeSlider = 0"
                @mouseup="activeSlider = -1"
                @touchmove="updateSlider"
                @touchstart="activeSlider = 0"
                @touchend="activeSlider = -1"
              />
              <div 
                class="slider-thumb" 
                :class="{ 'active': activeSlider === 0 }"
                :style="{ left: `calc(${answers[0] * 10}% - 15px)` }"
              >
                <span>{{ Math.round(answers[0]) }}</span>
              </div>
            </div>
            <div class="scale-label-container">
              <div class="scale-label left">No Pain</div>
              <div class="scale-label right">Bad Pain</div>
            </div>
          </div>
        </div>
      </div>

      <div class="question">
        <div class="question-header">
          <span class="question-number">2</span>
          <span class="question-title">Rate Worst Pain in the Past 6 Months</span>
        </div>
        <div class="question-subtitle">
          (0-10 scale where 0 is 'no pain' and 10 is 'pain as bad as it could be')
        </div>

        <div class="scale-container">
          <div class="scale-background">
            <div class="scale-numbers">
              <div class="scale-number left">0</div>
              <div class="scale-number right">10</div>
            </div>
            <div class="scale-slider">
              <div class="slider-track" :style="getSliderTrackStyle(answers[1])"></div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                v-model.number="answers[1]"
                class="slider"
                @input="saveAnswers"
                @mousemove="updateSlider"
                @mousedown="activeSlider = 1"
                @mouseup="activeSlider = -1"
                @touchmove="updateSlider"
                @touchstart="activeSlider = 1"
                @touchend="activeSlider = -1"
              />
              <div 
                class="slider-thumb" 
                :class="{ 'active': activeSlider === 1 }"
                :style="{ left: `calc(${answers[1] * 10}% - 15px)` }"
              >
                <span>{{ Math.round(answers[1]) }}</span>
              </div>
            </div>
            <div class="scale-label-container">
              <div class="scale-label left">No Pain</div>
              <div class="scale-label right">Bad Pain</div>
            </div>
          </div>
        </div>
      </div>

      <div class="question">
        <div class="question-header">
          <span class="question-number">3</span>
          <span class="question-title">Rate Average Pain in the Past 6 Months</span>
        </div>
        <div class="question-subtitle">
          (0-10 scale where 0 is 'no pain' and 10 is 'pain as bad as it could be'. This refers to
          your usual pain at times you were experiencing pain.)
        </div>

        <div class="scale-container">
          <div class="scale-background">
            <div class="scale-numbers">
              <div class="scale-number left">0</div>
              <div class="scale-number right">10</div>
            </div>
            <div class="scale-slider">
              <div class="slider-track" :style="getSliderTrackStyle(answers[2])"></div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                v-model.number="answers[2]"
                class="slider"
                @input="saveAnswers"
                @mousemove="updateSlider"
                @mousedown="activeSlider = 2"
                @mouseup="activeSlider = -1"
                @touchmove="updateSlider"
                @touchstart="activeSlider = 2"
                @touchend="activeSlider = -1"
              />
              <div 
                class="slider-thumb" 
                :class="{ 'active': activeSlider === 2 }"
                :style="{ left: `calc(${answers[2] * 10}% - 15px)` }"
              >
                <span>{{ Math.round(answers[2]) }}</span>
              </div>
            </div>
            <div class="scale-label-container">
              <div class="scale-label left">No Pain</div>
              <div class="scale-label right">Bad Pain</div>
            </div>
          </div>
        </div>
      </div>

      <div class="question">
        <div class="question-header">
          <span class="question-number">4</span>
          <span class="question-title">Days Kept from Usual Activities in the Past 6 Months</span>
        </div>
        <div class="question-subtitle">(Work, school, housework, etc., due to pain)</div>

        <div class="input-container">
          <input
            type="number"
            placeholder="Input a Number"
            class="number-input"
            v-model.number="answers[3]"
            min="0"
            max="190"
            @input="validateDaysInput"
          />
          <span class="days-label">day(s)</span>
          <p v-if="daysError" class="error-message">Please enter a number between 0 and 190</p>
        </div>
      </div>

      <div class="question">
        <div class="question-header">
          <span class="question-number">5</span>
          <span class="question-title"
            >Rate Pain Interference with Daily Activities in the Past 6 Months</span
          >
        </div>
        <div class="question-subtitle">
          (0-10 scale where 0 is 'no interference' and 10 is 'unable to carry on activities')
        </div>

        <div class="scale-container">
          <div class="scale-background">
            <div class="scale-numbers">
              <div class="scale-number left">0</div>
              <div class="scale-number right">10</div>
            </div>
            <div class="scale-slider">
              <div class="slider-track" :style="getSliderTrackStyle(answers[4])"></div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                v-model.number="answers[4]"
                class="slider"
                @input="saveAnswers"
                @mousemove="updateSlider"
                @mousedown="activeSlider = 4"
                @mouseup="activeSlider = -1"
                @touchmove="updateSlider"
                @touchstart="activeSlider = 4"
                @touchend="activeSlider = -1"
              />
              <div 
                class="slider-thumb" 
                :class="{ 'active': activeSlider === 4 }"
                :style="{ left: `calc(${answers[4] * 10}% - 15px)` }"
              >
                <span>{{ Math.round(answers[4]) }}</span>
              </div>
            </div>
            <div class="scale-label-container">
              <div class="scale-label left">No Interference</div>
              <div class="scale-label right">Unable</div>
            </div>
          </div>
        </div>
      </div>

      <div class="question">
        <div class="question-header">
          <span class="question-number">6</span>
          <span class="question-title"
            >Rate Change in Ability to Participate in Activities in the Past 6 Months</span
          >
        </div>
        <div class="question-subtitle">
          (Recreational, social, and family activities on a 0-10 scale where 0 is 'no change' and 10
          is 'extreme change')
        </div>

        <div class="scale-container">
          <div class="scale-background">
            <div class="scale-numbers">
              <div class="scale-number left">0</div>
              <div class="scale-number right">10</div>
            </div>
            <div class="scale-slider">
              <div class="slider-track" :style="getSliderTrackStyle(answers[5])"></div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                v-model.number="answers[5]"
                class="slider"
                @input="saveAnswers"
                @mousemove="updateSlider"
                @mousedown="activeSlider = 5"
                @mouseup="activeSlider = -1"
                @touchmove="updateSlider"
                @touchstart="activeSlider = 5"
                @touchend="activeSlider = -1"
              />
              <div 
                class="slider-thumb" 
                :class="{ 'active': activeSlider === 5 }"
                :style="{ left: `calc(${answers[5] * 10}% - 15px)` }"
              >
                <span>{{ Math.round(answers[5]) }}</span>
              </div>
            </div>
            <div class="scale-label-container">
              <div class="scale-label left">No Change</div>
              <div class="scale-label right">Extreme Change</div>
            </div>
          </div>
        </div>
      </div>

      <div class="question">
        <div class="question-header">
          <span class="question-number">7</span>
          <span class="question-title">Rate Change in Ability to Work in the Past 6 Months</span>
        </div>
        <div class="question-subtitle">
          (Including housework on a 0-10 scale where 0 is 'no change' and 10 is 'extreme change')
        </div>

        <div class="scale-container">
          <div class="scale-background">
            <div class="scale-numbers">
              <div class="scale-number left">0</div>
              <div class="scale-number right">10</div>
            </div>
            <div class="scale-slider">
              <div class="slider-track" :style="getSliderTrackStyle(answers[6])"></div>
              <input
                type="range"
                min="0"
                max="10"
                step="0.1"
                v-model.number="answers[6]"
                class="slider"
                @input="saveAnswers"
                @mousemove="updateSlider"
                @mousedown="activeSlider = 6"
                @mouseup="activeSlider = -1"
                @touchmove="updateSlider"
                @touchstart="activeSlider = 6"
                @touchend="activeSlider = -1"
              />
              <div 
                class="slider-thumb" 
                :class="{ 'active': activeSlider === 6 }"
                :style="{ left: `calc(${answers[6] * 10}% - 15px)` }"
              >
                <span>{{ Math.round(answers[6]) }}</span>
              </div>
            </div>
            <div class="scale-label-container">
              <div class="scale-label left">No Change</div>
              <div class="scale-label right">Extreme Change</div>
            </div>
          </div>
        </div>
      </div>

      <div class="button-container">
        <button class="submit-button" @click="submitForm" :disabled="daysError || !isFormValid">
          Submit for Suggestion of Sports
        </button>

        <button class="reset-button" @click="resetForm">Reset Form</button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { reactive, ref, computed, onMounted, watch } from 'vue'
import { useRouter } from 'vue-router'
import { useUserStore } from '@/stores/userStore'

const router = useRouter()
const userStore = useUserStore()
const daysError = ref(false)
const activeSlider = ref(-1)

const defaultAnswers = {
  0: 0,
  1: 0,
  2: 0,
  3: 0,
  4: 0,
  5: 0,
  6: 0,
}


const answers = reactive(loadAnswers())


watch(() => answers[3], validateDaysInput)


onMounted(() => {
  loadAnswers()
})

function loadAnswers() {
  try {
    const savedAnswers = localStorage.getItem('painCheckAnswers')
    if (savedAnswers) {
      return JSON.parse(savedAnswers)
    }
  } catch (error) {
    console.error('Error loading saved answers:', error)
  }
  return { ...defaultAnswers }
}

function saveAnswers() {
  try {
    localStorage.setItem('painCheckAnswers', JSON.stringify(answers))
  } catch (error) {
    console.error('Error saving answers:', error)
  }
}

function validateDaysInput() {
  const days = answers[3]
  if (days === null || days === undefined || days === '') {
    answers[3] = 0
    daysError.value = false
    return
  }

  const numDays = Number(days)
  daysError.value = isNaN(numDays) || numDays < 0 || numDays > 190


  if (!isNaN(numDays)) {
    answers[3] = Math.floor(numDays)
  }

  saveAnswers()
}

const isFormValid = computed(() => {
  return !daysError.value && answers[3] !== null && answers[3] !== undefined
})

function resetForm() {

  Object.keys(defaultAnswers).forEach((key) => {
    answers[key] = defaultAnswers[key]
  })


  daysError.value = false
  saveAnswers()
}

function submitForm() {
  if (daysError.value) return

  saveAnswers()

  const sum = Object.values(answers).reduce((total, value) => total + Number(value || 0), 0)
  let painLevel = 'mild'

  if (sum > 30) {
    painLevel = 'severe'
  } else if (sum > 15) {
    painLevel = 'moderate'
  }

  userStore.setPainCheckDone(true)
  router.push(`/sport-suggestion/${painLevel}`)
}

function getSliderTrackStyle(value) {
  // 根据值计算颜色
  const colors = {
    start: '#4CAF50',  // 绿色（轻微）
    middle: '#FFA726', // 橙色（中等）
    end: '#EF5350'     // 红色（严重）
  }
  
  const percent = (value / 10) * 100
  let gradient

  if (value <= 3.33) {
    // 0-3.33: 绿色到浅橙色
    gradient = `linear-gradient(to right, 
      ${colors.start} 0%, 
      ${colors.start} ${percent}%, 
      ${colors.middle} ${percent}%, 
      #ddd ${percent}%, 
      #ddd 100%)`
  } else if (value <= 6.66) {
    // 3.33-6.66: 浅橙色到橙色
    gradient = `linear-gradient(to right, 
      ${colors.start} 0%, 
      ${colors.middle} ${percent}%, 
      ${colors.end} ${percent}%, 
      #ddd ${percent}%, 
      #ddd 100%)`
  } else {
    // 6.66-10: 橙色到红色
    gradient = `linear-gradient(to right, 
      ${colors.start} 0%, 
      ${colors.middle} 33.3%, 
      ${colors.end} ${percent}%, 
      #ddd ${percent}%, 
      #ddd 100%)`
  }
  
  return {
    background: gradient,
    transition: 'none' // 移除过渡效果使颜色条立即跟随
  }
}

function updateSlider() {
  // 强制重新渲染颜色条
  if (activeSlider.value >= 0) {
    saveAnswers()
  }
}
</script>

<style scoped>
.pain-check {
  padding: 20px;
  background-color: #ffffff;
  min-height: 100vh;
}

.form-container {
  max-width: 800px;
  margin: 0 auto;
  background-color: #ffffff;
  padding: 30px;
  border-radius: 15px;
  box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
}

.form-container h2 {
  text-align: center;
  margin-bottom: 30px;
  color: #4a6741;
  font-size: 24px;
  padding-bottom: 15px;
  border-bottom: 2px solid #e8ebdd;
}

.question {
  background-color: #f8f8f8;
  border-radius: 10px;
  padding: 20px;
  margin-bottom: 25px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  transition: all 0.3s ease;
  border: 2px solid transparent;
  position: relative;
  overflow: hidden;
}

.question:hover {
  transform: translateY(-2px);
  box-shadow: 0 4px 8px rgba(74, 103, 65, 0.2);
  border-color: #4a6741;
}

.question::before {
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

.question:hover::before {
  left: 100%;
}

.question-header {
  display: flex;
  align-items: center;
  margin-bottom: 4px;
  transition: all 0.3s ease;
}

.question:hover .question-header {
  transform: translateX(5px);
}

.question-number {
  font-weight: bold;
  margin-right: 8px;
  background-color: #4a6741;
  color: white;
  width: 24px;
  height: 24px;
  border-radius: 50%;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.3s ease;
}

.question:hover .question-number {
  transform: scale(1.1);
  background-color: #3a5331;
}

.question-title {
  font-weight: bold;
}

.question-subtitle {
  font-size: 12px;
  color: #555;
  margin-bottom: 15px;
}

.scale-container {
  margin-top: 10px;
}

.scale-background {
  background-color: #e8ebdd;
  border-radius: 8px;
  padding: 15px 20px;
  position: relative;
  transition: all 0.2s ease;
}

.scale-background:hover {
  background-color: #e0e6d2;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.scale-numbers {
  display: flex;
  justify-content: space-between;
  margin-bottom: 15px;
  font-weight: bold;
}

.scale-slider {
  position: relative;
  height: 30px;
  margin: 0 10px;
}

.slider-track {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 100%;
  height: 6px;
  border-radius: 3px;
  transition: none;
  will-change: transform, background;
}

.slider {
  -webkit-appearance: none;
  appearance: none;
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  opacity: 0;
  cursor: pointer;
  z-index: 10;
  transition: none;
  touch-action: manipulation;
}

.slider-thumb {
  position: absolute;
  top: 50%;
  transform: translateY(-50%);
  width: 30px;
  height: 30px;
  border-radius: 50%;
  background: white;
  border: 2px solid #4a6741;
  display: flex;
  align-items: center;
  justify-content: center;
  font-weight: bold;
  color: #4a6741;
  z-index: 5;
  box-shadow: 0 2px 6px rgba(0, 0, 0, 0.2);
  transition: transform 0.1s ease, box-shadow 0.1s ease;
  will-change: transform, left;
  pointer-events: none;
}

.slider-thumb.active {
  transform: translateY(-50%) scale(1.1);
  box-shadow: 0 4px 12px rgba(74, 103, 65, 0.4);
  background-color: #f5f9f3;
  border-width: 3px;
}

.scale-label-container {
  display: flex;
  justify-content: space-between;
  margin-top: 15px;
}

.scale-label {
  font-size: 12px;
  font-weight: bold;
}

.input-container {
  position: relative;
  max-width: 300px;
  display: flex;
  align-items: center;
  gap: 8px;
}

.number-input {
  width: 150px;
  padding: 12px;
  border: 1px solid #ddd;
  border-radius: 4px;
  background-color: #e8ebdd;
  color: #333;
  font-size: 16px;
}

.number-input:focus {
  outline: none;
  border-color: #4a6741;
}

.days-label {
  font-size: 16px;
  color: #333;
}

.error-message {
  color: #d32f2f;
  font-size: 12px;
  margin-top: 5px;
  margin-bottom: 0;
  position: absolute;
  top: 100%;
  left: 0;
}

.button-container {
  display: flex;
  gap: 15px;
  margin-top: 20px;
}

.submit-button {
  background-color: #4a6741;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 15px;
  flex: 3;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.reset-button {
  background-color: #8f9490;
  color: white;
  border: none;
  border-radius: 4px;
  padding: 15px;
  flex: 1;
  font-size: 16px;
  font-weight: bold;
  cursor: pointer;
  transition: background-color 0.3s;
}

.submit-button:hover:not(:disabled) {
  background-color: #3a5331;
}

.reset-button:hover {
  background-color: #767c77;
}

.submit-button:disabled {
  background-color: #a0aca0;
  cursor: not-allowed;
}
</style>
