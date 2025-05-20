<template>
  <div class="sports-list">
    <div class="header-section">
      <h2>Sports Suggestion For {{ capitalizeFirstLetter(level) }} Situation</h2>
      <p class="recommendation-text">
        {{ levelRecommendation }}<br />
        <span v-if="userProfile && userProfile.age">Recommended based on your age: {{userProfile.age}}, weight: {{userProfile.weight}}, body type: {{userProfile.silhouette}}</span>
      </p>
      <div class="filters-edit-row">
        <div class="filters">
          <button 
            class="filter-btn"
            :class="{ active: sortBy === 'name' }"
            @click="sortBy = 'name'"
          >
            Sort by Name
          </button>
          <button 
            class="filter-btn"
            :class="{ active: sortBy === 'duration' }"
            @click="sortBy = 'duration'"
          >
            Sort by Duration
          </button>
        </div>
        <button class="edit-profile-btn" @click="$emit('edit-profile')">Edit Profile</button>
      </div>
    </div>

    <TransitionGroup 
      name="sports-list" 
      tag="div" 
      class="sports-grid"
    >
      <div 
        v-for="sport in sortedCustomSports" 
        :key="sport.id || sport.name"
        class="sport-card"
        @click="selectedSport = sport"
        @mouseenter="hoveredSport = sport.name"
        @mouseleave="hoveredSport = null"
      >
        <div class="card-content">
          <div class="image-container">
            <img v-lazy="sport.image" :alt="sport.name" />
            <div class="duration-badge">{{ sport.duration || getRecommendedDuration(sport) }}</div>
            <!-- 删除按钮 -->
            <button v-if="hoveredSport === sport.name" class="delete-btn" @click.stop="removeSport(sport)">&times;</button>
          </div>
          <div class="sport-info">
            <h3>{{ sport.name }}</h3>
            <p>{{ sport.description }}</p>
          </div>
        </div>
      </div>
      <!-- +号卡片 -->
      <div class="sport-card add-card" @click="showAddModal = true" key="add">
        <div class="add-content">+</div>
      </div>
    </TransitionGroup>

    <!-- Detail Modal -->
    <Transition name="modal">
      <div v-if="selectedSport" class="modal-overlay" @click="selectedSport = null">
        <div class="modal-content" @click.stop>
          <button class="close-btn" @click="selectedSport = null">&times;</button>
          <img v-lazy="selectedSport.image" :alt="selectedSport.name" />
          <div class="modal-info">
            <h2>{{ selectedSport.name }}</h2>
            <span class="duration">{{ selectedSport.duration || getRecommendedDuration(selectedSport) }}</span>
            <p>{{ selectedSport.description }}</p>
            <div class="tips">
              <h4>Recommendations:</h4>
              <ul>
                <li>Start with proper warm-up exercises</li>
                <li>Monitor your exercise intensity</li>
                <li>Stop immediately if you feel discomfort</li>
                <li>Maintain regular exercise habits</li>
              </ul>
            </div>
          </div>
        </div>
      </div>
    </Transition>

    <!-- 添加运动弹窗 -->
    <Transition name="modal">
      <div v-if="showAddModal" class="modal-overlay" @click="showAddModal = false">
        <div class="modal-content add-modal-modern" @click.stop>
          <h3 class="add-modal-title">Add a Sport</h3>
          <div class="add-modal-section">
            <label class="add-modal-label">Select Sport</label>
            <select v-model="selectedToAdd" class="add-modal-select">
              <option v-for="sport in availableToAdd" :key="sport.name" :value="sport">
                {{ sport.name }}<span v-if="getLevelTip(sport.level)"> {{ getLevelTip(sport.level) }}</span>
              </option>
            </select>
          </div>
          <div v-if="selectedToAdd && selectedToAdd.image" class="add-detail add-modal-section">
            <img :src="selectedToAdd.image" :alt="selectedToAdd.name" class="add-detail-img" />
            <div class="add-detail-info">
              <h4>{{ selectedToAdd.name }}</h4>
              <div class="add-detail-duration">Recommended: {{ selectedToAdd && selectedToAdd.duration ? selectedToAdd.duration : getRecommendedDuration(selectedToAdd) }}</div>
              <div class="add-detail-desc">{{ selectedToAdd.description }}</div>
            </div>
          </div>
          <div class="add-modal-section">
            <label class="add-modal-label">Custom Duration (minutes)</label>
            <div style="display: flex; align-items: center; gap: 8px;">
              <input v-model="customMinDuration" @input="validateDuration" type="number" min="5" max="120" class="add-modal-input" placeholder="Min" style="width: 80px;" />
              <span style="font-size:1.2em; color:#888;">-</span>
              <input v-model="customMaxDuration" @input="validateDuration" type="number" min="5" max="120" class="add-modal-input" placeholder="Max" style="width: 80px;" />
            </div>
            <span v-if="durationError" class="add-modal-error">{{ durationError }}</span>
          </div>
          <div class="add-modal-footer">
            <button @click="addCustomSport" :disabled="!selectedToAdd || !!durationError || !customMinDuration || !customMaxDuration" class="add-modal-btn main">Add</button>
            <button @click="showAddModal = false" class="add-modal-btn">Cancel</button>
          </div>
        </div>
      </div>
    </Transition>
  </div>
</template>

<script setup>
import { computed, ref, watch, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'

const props = defineProps({
  level: {
    type: String,
    required: true,
  },
})

const selectedSport = ref(null)
const sortBy = ref('name')
const showAddModal = ref(false)
const selectedToAdd = ref(null)
const customSports = ref([])
const hoveredSport = ref(null)
const userStore = useUserStore()

//import img
import walkingImg from '../assets/walking.jpg'
import cyclingImg from '../assets/cycling.jpg'
import yogaImg from '../assets/yoga.jpg'
import taichiImg from '../assets/taichi.jpg'
import swimmingImg from '../assets/swimming.jpg'
import waterAerobicsImg from '../assets/water-aerobics.jpg'
import golfImg from '../assets/golf.jpg'
import ellipticalImg from '../assets/elliptical.jpg'
import chairExerciseImg from '../assets/chair-exercise.jpg'
import aquaticTherapyImg from '../assets/aquatic-therapy.jpg'
import stretchingImg from '../assets/stretching.jpg'
import adaptiveSportsImg from '../assets/adaptive-sports.jpg'

const levelRecommendations = {
  mild: "Choose 2-3 different activities from below and perform them 3-4 times per week. Start with shorter durations and gradually increase as comfortable.",
  moderate: "Select 2 activities and perform them 2-3 times per week. Focus on low-impact exercises and listen to your body.",
  severe: "Start with 1 activity and perform it 2-3 times per week. Keep sessions short and gentle, with rest days in between.",
}

const levelRecommendation = computed(() => {
  return levelRecommendations[props.level]
})

const sports = [
  // mild
  {
    id: 1,
    level: 'mild',
    name: 'Walking',
    duration: '20-30 mins',
    description: 'A low-impact activity that helps maintain joint flexibility and overall fitness. Start with 10 minutes and gradually increase.',
    image: walkingImg,
  },
  {
    id: 2,
    level: 'mild',
    name: 'Cycling',
    duration: '15-20 mins',
    description: 'Great for cardiovascular health and gentle on the joints. Use stationary bike for better stability.',
    image: cyclingImg,
  },
  {
    id: 3,
    level: 'mild',
    name: 'Yoga',
    duration: '20-25 mins',
    description: 'Improves flexibility and strength. Focus on gentle poses and avoid positions that cause discomfort.',
    image: yogaImg,
  },
  {
    id: 4,
    level: 'mild',
    name: 'Tai Chi',
    duration: '15-20 mins',
    description: 'Enhances balance and reduces pain through slow, controlled movements. Perfect for beginners.',
    image: taichiImg,
  },
  // moderate
  {
    id: 5,
    level: 'moderate',
    name: 'Swimming',
    duration: '15-20 mins',
    description: 'Provides a full-body workout without putting stress on the joints. Start with 5-10 minutes and take breaks as needed.',
    image: swimmingImg,
  },
  {
    id: 6,
    level: 'moderate',
    name: 'Water Aerobics',
    duration: '15-20 mins',
    description: 'Low-impact exercise in water. Focus on gentle movements and maintain good form.',
    image: waterAerobicsImg,
  },
  {
    id: 7,
    level: 'moderate',
    name: 'Golf',
    duration: '30-45 mins',
    description: 'Low-impact activity. Use a cart if needed and focus on proper form to protect joints.',
    image: golfImg,
  },
  {
    id: 8,
    level: 'moderate',
    name: 'Elliptical Training',
    duration: '10-15 mins',
    description: 'Cardiovascular exercise with minimal joint impact. Start slowly and maintain low resistance.',
    image: ellipticalImg,
  },
  // severe
  {
    id: 9,
    level: 'severe',
    name: 'Chair Exercises',
    duration: '10-15 mins',
    description: 'Safe, seated exercises focusing on gentle movements. Take breaks when needed.',
    image: chairExerciseImg,
  },
  {
    id: 10,
    level: 'severe',
    name: 'Aquatic Therapy',
    duration: '10-15 mins',
    description: 'Gentle water exercises under supervision. Focus on range of motion and relaxation.',
    image: aquaticTherapyImg,
  },
  {
    id: 11,
    level: 'severe',
    name: 'Stretching Routines',
    duration: '10-15 mins',
    description: 'Gentle stretching to maintain flexibility. Never force movements and stop if pain occurs.',
    image: stretchingImg,
  },
  {
    id: 12,
    level: 'severe',
    name: 'Adaptive Sports',
    duration: '10-15 mins',
    description: 'Modified activities adapted to your comfort level. Always start with guidance from a professional.',
    image: adaptiveSportsImg,
  },
]

const levelOrder = { mild: 1, moderate: 2, severe: 3 }

// 推荐池：当前level及更高level的所有运动
const recommendPool = computed(() => {
  return sports.filter(s => levelOrder[s.level] >= levelOrder[props.level])
})

// 随机推荐4个运动，每次依赖变化都重新随机
function getRandomSports(pool, n = 4) {
  const arr = [...pool]
  for (let i = arr.length - 1; i > 0; i--) {
    const j = Math.floor(Math.random() * (i + 1))
    ;[arr[i], arr[j]] = [arr[j], arr[i]]
  }
  return arr.slice(0, n)
}

function getRecommendedDuration(sport) {
  // 动态时长：mild推荐更长，severe更短
  let min = 10, max = 20
  if (sport.name === 'Walking') { min = 20; max = 30 }
  if (sport.name === 'Cycling') { min = 15; max = 20 }
  if (sport.name === 'Yoga') { min = 20; max = 25 }
  if (sport.name === 'Tai Chi') { min = 15; max = 20 }
  if (sport.name === 'Swimming') { min = 15; max = 20 }
  if (sport.name === 'Water Aerobics') { min = 15; max = 20 }
  if (sport.name === 'Golf') { min = 30; max = 45 }
  if (sport.name === 'Elliptical Training') { min = 10; max = 15 }
  if (sport.name === 'Chair Exercises') { min = 10; max = 15 }
  if (sport.name === 'Aquatic Therapy') { min = 10; max = 15 }
  if (sport.name === 'Stretching Routines') { min = 10; max = 15 }
  if (sport.name === 'Adaptive Sports') { min = 10; max = 15 }
  if (props.level === 'severe') {
    min = Math.max(5, min - 5)
    max = Math.max(10, max - 10)
  } else if (props.level === 'moderate') {
    min = Math.max(8, min - 2)
    max = Math.max(12, max - 5)
  } else if (props.level === 'mild') {
    min = min + 2
    max = Math.min(60, max + 10)
  }
  if (max - min < 5) max = min + 5
  if (max > 60) max = 60
  return `${min}-${max} mins`
}

// 推荐运动列表，每次依赖变化都重新随机
const recommendedSports = ref([])
function refreshRecommendations() {
  recommendedSports.value = getRandomSports(recommendPool.value, 4)
  customSports.value = [...recommendedSports.value]
  userStore.setExercisePlan(customSports.value)
}

onMounted(() => {
  if (!userStore.exercise_plan || userStore.exercise_plan.length === 0) {
    refreshRecommendations()
  } else {
    customSports.value = [...userStore.exercise_plan]
  }
})

let lastProfile = JSON.stringify(userStore.user_profile)
let lastLevel = props.level

watch([() => userStore.user_profile, () => props.level], ([newProfile, newLevel]) => {
  if (JSON.stringify(newProfile) !== lastProfile || newLevel !== lastLevel) {
    refreshRecommendations()
    lastProfile = JSON.stringify(newProfile)
    lastLevel = newLevel
  }
})

// 下拉添加运动：所有运动都可选，提示Above/Below current pain level
const availableToAdd = computed(() => {
  const currentNames = customSports.value.map(s => s.name)
  return sports.filter(s => !currentNames.includes(s.name))
})
function getLevelTip(level) {
  if (levelOrder[level] > levelOrder[props.level]) {
    return '(Above current pain level)'
  } else if (levelOrder[level] < levelOrder[props.level]) {
    return '(Below current pain level)'
  }
  return ''
}

// 自定义时长输入：区间
const customMinDuration = ref('')
const customMaxDuration = ref('')
const durationError = ref('')

// 监听选择运动时自动填入推荐时长区间
watch(selectedToAdd, (val) => {
  if (val) {
    const [min, max] = (getRecommendedDuration(val) || '').split('-').map(s => parseInt(s))
    customMinDuration.value = min || 10
    customMaxDuration.value = max || 20
    durationError.value = ''
  } else {
    customMinDuration.value = ''
    customMaxDuration.value = ''
    durationError.value = ''
  }
})

function validateDuration() {
  const min = Number(customMinDuration.value)
  const max = Number(customMaxDuration.value)
  if (!min || !max || isNaN(min) || isNaN(max)) {
    durationError.value = 'Please enter both min and max duration (minutes)'
    return false
  }
  if (min < 5 || max > 120 || min > max) {
    durationError.value = 'Duration must be 5-120 mins and min ≤ max'
    return false
  }
  durationError.value = ''
  return true
}

function addCustomSport() {
  if (selectedToAdd.value && validateDuration()) {
    customSports.value.push({ ...selectedToAdd.value, duration: `${customMinDuration.value}-${customMaxDuration.value} mins` })
    showAddModal.value = false
    selectedToAdd.value = null
    customMinDuration.value = ''
    customMaxDuration.value = ''
    durationError.value = ''
    userStore.setExercisePlan([...customSports.value])
  }
}
function removeSport(sport) {
  const idx = customSports.value.findIndex(s => s.name === sport.name)
  if (idx !== -1) {
    customSports.value.splice(idx, 1)
    userStore.setExercisePlan([...customSports.value])
  }
}

function capitalizeFirstLetter(string) {
  return string.charAt(0).toUpperCase() + string.slice(1)
}

const userProfile = computed(() => userStore.user_profile || {})

// 排序逻辑
const sortedCustomSports = computed(() => {
  if (sortBy.value === 'name') {
    return [...customSports.value].sort((a, b) => a.name.localeCompare(b.name))
  } else if (sortBy.value === 'duration') {
    // 提取最小时长进行排序
    return [...customSports.value].sort((a, b) => {
      const getMin = s => parseInt((s.duration || '').split('-')[0]) || 0
      return getMin(a) - getMin(b)
    })
  }
  return customSports.value
})
</script>

<style scoped>
.sports-list {
  padding: 20px;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.header-section {
  margin-bottom: 40px;
  text-align: center;
}

h2 {
  margin-bottom: 20px;
  font-size: 2rem;
  color: #2c3e50;
  font-weight: 600;
}

.recommendation-text {
  margin: 20px auto;
  max-width: 800px;
  color: #2c3e50;
  font-size: 1.1rem;
  line-height: 1.6;
  padding: 15px;
  background-color: #f8f9fa;
  border-radius: 8px;
  text-align: center;
}

.filters-edit-row {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 12px;
}

.filters {
  display: flex;
  gap: 10px;
  margin: 0 auto;
  justify-content: center;
  flex: 1;
}

.filter-btn {
  padding: 8px 16px;
  border: 2px solid #4a6741;
  border-radius: 20px;
  background: transparent;
  color: #4a6741;
  cursor: pointer;
  transition: all 0.3s ease;
}

.filter-btn.active {
  background: #4a6741;
  color: white;
}

.sports-grid {
  display: grid;
  grid-template-columns: repeat(auto-fill, minmax(300px, 1fr));
  gap: 30px;
  padding: 20px;
}

.sport-card {
  position: relative;
  border-radius: 16px;
  overflow: hidden;
  cursor: pointer;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.sport-card:hover {
  transform: translateY(-5px);
  box-shadow: 0 8px 20px rgba(0, 0, 0, 0.15);
}

.card-content {
  background: white;
  height: 100%;
}

.image-container {
  position: relative;
  width: 100%;
  height: 200px;
  overflow: hidden;
}

.image-container img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.3s ease;
}

.sport-card:hover .image-container img {
  transform: scale(1.05);
}

.duration-badge {
  position: absolute;
  top: 15px;
  right: 15px;
  background: rgba(74, 103, 65, 0.9);
  color: white;
  padding: 6px 12px;
  border-radius: 20px;
  font-size: 0.9rem;
  backdrop-filter: blur(4px);
}

.sport-info {
  padding: 20px;
}

.sport-info h3 {
  margin: 0 0 10px;
  color: #2c3e50;
  font-size: 1.3rem;
}

.sport-info p {
  color: #666;
  line-height: 1.5;
  margin: 0;
}

/* 动画效果 */
.sports-list-enter-active,
.sports-list-leave-active {
  transition: all 0.5s ease;
}

.sports-list-enter-from,
.sports-list-leave-to {
  opacity: 0;
  transform: translateY(30px);
}

/* 弹窗样式 */
.modal-overlay {
  position: fixed;
  top: 0;
  left: 0;
  right: 0;
  bottom: 0;
  background: rgba(0, 0, 0, 0.7);
  display: flex;
  justify-content: center;
  align-items: center;
  z-index: 1000;
  padding: 20px;
}

.modal-content {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(60, 120, 80, 0.08);
  max-width: 600px;
  width: 90%;
  max-height: 90vh;
  overflow-y: auto;
  position: relative;
  padding: 32px 28px 28px 28px;
  animation: modalPopIn 0.35s cubic-bezier(.68,-0.55,.27,1.55);
}
@keyframes modalPopIn {
  from { opacity: 0; transform: scale(0.92);}
  to { opacity: 1; transform: scale(1);}
}
.modal-content h3 {
  font-size: 1.5rem;
  font-weight: 700;
  color: #2d4739;
  margin-bottom: 18px;
  text-align: center;
  letter-spacing: 1px;
}
.modal-content h3::after {
  content: '';
  display: block;
  width: 60px;
  height: 3px;
  margin: 12px auto 0 auto;
  background: #e0e8d8;
  border-radius: 2px;
  opacity: 0.25;
}
select {
  width: 100%;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1.5px solid #b5cc7a;
  background: #f8f9fa;
  font-size: 1.08rem;
  margin-bottom: 12px;
  box-shadow: 0 1px 6px rgba(74,103,65,0.06);
  transition: border 0.3s, box-shadow 0.3s;
}
select:focus {
  border-color: #4a6741;
  box-shadow: 0 2px 12px #b5cc7a33;
}
.add-detail {
  background: linear-gradient(90deg, #f8f9fa 60%, #eaf5e1 100%);
  border-radius: 14px;
  box-shadow: 0 2px 12px rgba(74,103,65,0.08);
  padding: 16px 18px;
  margin: 18px 0 10px 0;
  display: flex;
  align-items: flex-start;
  gap: 18px;
  transition: background 0.4s;
}
.add-detail-img {
  width: 100px;
  height: 80px;
  object-fit: cover;
  border-radius: 12px;
  box-shadow: 0 4px 16px #b5cc7a33;
  border: 2.5px solid #e0e8d8;
  background: rgba(255,255,255,0.7);
  transition: box-shadow 0.3s;
}
.add-detail-info h4 {
  font-size: 1.18rem;
  color: #4a6741;
  font-weight: 600;
  margin-bottom: 6px;
}
.add-detail-duration {
  font-size: 1.01rem;
  color: #6b8f5e;
  margin-bottom: 4px;
  font-weight: 500;
}
.add-detail-desc {
  font-size: 0.97rem;
  color: #333;
  opacity: 0.92;
}
.modal-content button {
  margin: 10px 8px 0 0;
  padding: 10px 28px;
  border-radius: 20px;
  font-size: 1.08rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background 0.3s, color 0.3s, transform 0.15s;
  box-shadow: 0 2px 8px #b5cc7a22;
}
.modal-content button:first-of-type {
  background: linear-gradient(90deg, #4a6741 60%, #8dc26f 100%);
  color: #fff;
  animation: ctaBreath 2.2s infinite alternate;
}
@keyframes ctaBreath {
  from { box-shadow: 0 2px 8px #b5cc7a22; }
  to { box-shadow: 0 8px 24px #b5cc7a44; }
}
.modal-content button:first-of-type:active {
  transform: scale(0.97);
}
.modal-content button:last-of-type {
  background: linear-gradient(90deg, #e0e8d8 60%, #f8f9fa 100%);
  color: #4a6741;
}
.modal-content button:last-of-type:hover {
  background: #eaf5e1;
  color: #2c3e50;
}
.close-btn {
  position: absolute;
  top: 15px;
  right: 15px;
  background: white;
  border: none;
  width: 30px;
  height: 30px;
  border-radius: 50%;
  font-size: 20px;
  cursor: pointer;
  display: flex;
  align-items: center;
  justify-content: center;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
  z-index: 1;
}

.modal-content img {
  width: 100%;
  height: 300px;
  object-fit: cover;
}

.modal-info {
  padding: 30px;
}

.modal-info h2 {
  margin: 0 0 10px;
  font-size: 1.8rem;
}

.modal-info .duration {
  display: inline-block;
  background: #4a6741;
  color: white;
  padding: 5px 15px;
  border-radius: 20px;
  margin-bottom: 20px;
}

.tips {
  margin-top: 30px;
  background: #f8f9fa;
  padding: 20px;
  border-radius: 12px;
}

.tips h4 {
  margin: 0 0 15px;
  color: #2c3e50;
}

.tips ul {
  margin: 0;
  padding-left: 20px;
}

.tips li {
  margin-bottom: 8px;
  color: #666;
}

/* 弹窗动画 */
.modal-enter-active,
.modal-leave-active {
  transition: opacity 0.3s ease;
}

.modal-enter-from,
.modal-leave-to {
  opacity: 0;
}

@media (max-width: 768px) {
  .sports-grid {
    grid-template-columns: 1fr;
    padding: 10px;
  }

  .modal-content {
    width: 95%;
  }

  .modal-info {
    padding: 20px;
  }
}

.edit-profile-btn {
  margin-left: 18px;
  padding: 8px 18px;
  background: #fff;
  color: #4a6741;
  border: 2px solid #4a6741;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s, color 0.3s, box-shadow 0.3s, transform 0.2s;
  box-shadow: 0 1px 6px rgba(74,103,65,0.06);
  letter-spacing: 1px;
  display: inline-block;
}

.edit-profile-btn:hover {
  background: #4a6741;
  color: #fff;
  transform: scale(1.04);
  box-shadow: 0 4px 16px rgba(74,103,65,0.10);
}

.add-card {
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 2.5rem;
  color: #4a6741;
  background: #f8f9fa;
  border: 2px dashed #b5cc7a;
  cursor: pointer;
  transition: background 0.2s, border 0.2s;
  min-height: 220px;
}
.add-card:hover {
  background: #eaf5e1;
  border-color: #4a6741;
}
.add-content {
  font-size: 3rem;
  font-weight: bold;
}

.delete-btn {
  position: absolute;
  top: 10px;
  right: 10px;
  background: rgba(255,255,255,0.95);
  border: none;
  border-radius: 50%;
  width: 28px;
  height: 28px;
  font-size: 1.2rem;
  color: #e74c3c;
  box-shadow: 0 2px 8px rgba(0,0,0,0.08);
  cursor: pointer;
  opacity: 0.92;
  z-index: 2;
  transition: background 0.2s, color 0.2s, box-shadow 0.2s;
}
.delete-btn:hover {
  background: #e74c3c;
  color: #fff;
  box-shadow: 0 4px 16px #e74c3c33;
}

.add-modal-modern {
  background: #fff;
  border-radius: 18px;
  box-shadow: 0 4px 24px rgba(60, 120, 80, 0.12);
  max-width: 420px;
  width: 95%;
  padding: 32px 28px 24px 28px;
  display: flex;
  flex-direction: column;
  gap: 18px;
  animation: modalPopIn 0.35s cubic-bezier(.68,-0.55,.27,1.55);
}
.add-modal-title {
  font-size: 1.45rem;
  font-weight: 700;
  color: #2d4739;
  margin-bottom: 10px;
  text-align: center;
  letter-spacing: 1px;
}
.add-modal-section {
  margin-bottom: 10px;
  display: flex;
  flex-direction: column;
  gap: 6px;
}
.add-modal-label {
  font-size: 1rem;
  color: #4a6741;
  font-weight: 600;
  margin-bottom: 2px;
}
.add-modal-select {
  width: 100%;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1.5px solid #b5cc7a;
  background: #f8f9fa;
  font-size: 1.08rem;
  margin-bottom: 2px;
  box-shadow: 0 1px 6px rgba(74,103,65,0.06);
  transition: border 0.3s, box-shadow 0.3s;
}
.add-modal-select:focus {
  border-color: #4a6741;
  box-shadow: 0 2px 12px #b5cc7a33;
}
.add-modal-input {
  width: 100%;
  padding: 10px 14px;
  border-radius: 12px;
  border: 1.5px solid #b5cc7a;
  background: #f8f9fa;
  font-size: 1.08rem;
  margin-bottom: 2px;
  box-shadow: 0 1px 6px rgba(74,103,65,0.06);
  transition: border 0.3s, box-shadow 0.3s;
}
.add-modal-input:focus {
  border-color: #4a6741;
  box-shadow: 0 2px 12px #b5cc7a33;
}
.add-modal-error {
  color: #e74c3c;
  font-size: 0.97em;
  margin-top: 2px;
  min-height: 18px;
  font-weight: 500;
  letter-spacing: 0.01em;
}
.add-modal-footer {
  display: flex;
  gap: 12px;
  justify-content: flex-end;
  margin-top: 8px;
}
.add-modal-btn {
  padding: 10px 28px;
  border-radius: 20px;
  font-size: 1.08rem;
  font-weight: 600;
  border: none;
  cursor: pointer;
  transition: background 0.3s, color 0.3s, transform 0.15s;
  box-shadow: 0 2px 8px #b5cc7a22;
  background: linear-gradient(90deg, #e0e8d8 60%, #f8f9fa 100%);
  color: #4a6741;
}
.add-modal-btn.main {
  background: linear-gradient(90deg, #4a6741 60%, #8dc26f 100%);
  color: #fff;
  animation: ctaBreath 2.2s infinite alternate;
}
.add-modal-btn:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
  animation: none;
}
</style>
