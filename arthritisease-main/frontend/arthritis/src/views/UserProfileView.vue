<template>
  <div class="user-profile">
    <NavBar />
    <div class="container">
      <div class="back-link">
        <router-link to="#" @click.prevent="handleBack">
          <span class="back-arrow">←</span>
        </router-link>
        <h1>User Profile</h1>
      </div>
      <p class="subtitle">Please complete your personal information before using the system</p>
      <div class="divider"></div>
      <form class="user-profile-form animate-fade-in" @submit.prevent="submitProfile">
        <div class="form-title">Personal Information Form</div>
        <label>Age:
          <input v-model.number="profile.age" type="number" min="1" max="120" required placeholder="Enter your age" :class="{ error: errors.age && touched.age }" @input="validate" @blur="markTouched('age')" />
          <span v-if="touched.age && errors.age" class="error-msg modern-error">{{ errors.age }}</span>
        </label>
        <label>Gender:
          <select v-model="profile.gender" required :class="{ error: errors.gender && touched.gender }" @input="validate" @blur="markTouched('gender')">
            <option value="" disabled>Select gender</option>
            <option value="male">Male</option>
            <option value="female">Female</option>
          </select>
          <span v-if="touched.gender && errors.gender" class="error-msg modern-error">{{ errors.gender }}</span>
        </label>
        <label>Height (cm):
          <input v-model.number="profile.height" type="number" min="50" max="250" required placeholder="e.g. 170" :class="{ error: errors.height && touched.height }" @input="validate" @blur="markTouched('height')" />
          <span v-if="touched.height && errors.height" class="error-msg modern-error">{{ errors.height }}</span>
        </label>
        <label>Weight (kg):
          <input v-model.number="profile.weight" type="number" min="20" max="300" required placeholder="e.g. 65" :class="{ error: errors.weight && touched.weight }" @input="validate" @blur="markTouched('weight')" />
          <span v-if="touched.weight && errors.weight" class="error-msg modern-error">{{ errors.weight }}</span>
        </label>
        <label>Silhouette:
          <select v-model="profile.silhouette" required :class="{ error: errors.silhouette && touched.silhouette }" @input="validate" @blur="markTouched('silhouette')">
            <option value="" disabled>Select silhouette</option>
            <option value="apple">Apple</option>
            <option value="pear">Pear</option>
            <option value="rectangle">Rectangle</option>
            <option value="hourglass">Hourglass</option>
            <option value="inverted">Inverted Triangle</option>
          </select>
          <span v-if="touched.silhouette && errors.silhouette" class="error-msg modern-error">{{ errors.silhouette }}</span>
        </label>
        <label>Somatotype:
          <select v-model="profile.somatotype" required :class="{ error: errors.somatotype && touched.somatotype }" @input="validate" @blur="markTouched('somatotype')">
            <option value="" disabled>Select somatotype</option>
            <option value="ectomorph">Ectomorph (slim)</option>
            <option value="mesomorph">Mesomorph (athletic)</option>
            <option value="endomorph">Endomorph (round)</option>
          </select>
          <span v-if="touched.somatotype && errors.somatotype" class="error-msg modern-error">{{ errors.somatotype }}</span>
        </label>
        <button type="submit" class="cta-button" :disabled="!isFormValid">
          Save and Continue <span class="cta-arrow">→</span>
        </button>
      </form>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import AppFooter from '@/components/AppFooter.vue'
import { ref, computed, onMounted } from 'vue'
import { useUserStore } from '@/stores/userStore'
import { useRouter } from 'vue-router'
const userStore = useUserStore()
const router = useRouter()
const profile = ref({
  age: '',
  gender: '',
  height: '',
  weight: '',
  silhouette: '',
  somatotype: ''
})
const errors = ref({
  age: '',
  gender: '',
  height: '',
  weight: '',
  silhouette: '',
  somatotype: ''
})
const touched = ref({
  age: false,
  gender: false,
  height: false,
  weight: false,
  silhouette: false,
  somatotype: false
})
function validate() {
  errors.value.age = !profile.value.age ? 'Age is required.' : (profile.value.age < 1 || profile.value.age > 120 ? 'Age must be between 1 and 120.' : '')
  errors.value.gender = !profile.value.gender ? 'Gender is required.' : ''
  errors.value.height = !profile.value.height ? 'Height is required.' : (profile.value.height < 50 || profile.value.height > 250 ? 'Height must be between 50 and 250 cm.' : '')
  errors.value.weight = !profile.value.weight ? 'Weight is required.' : (profile.value.weight < 20 || profile.value.weight > 300 ? 'Weight must be between 20 and 300 kg.' : '')
  errors.value.silhouette = !profile.value.silhouette ? 'Silhouette is required.' : ''
  errors.value.somatotype = !profile.value.somatotype ? 'Somatotype is required.' : ''
}
const isFormValid = computed(() => {
  validate()
  return Object.values(errors.value).every(e => !e) && Object.values(profile.value).every(v => v)
})
function submitProfile() {
  validate()
  if (!isFormValid.value) return
  userStore.setUserProfile(profile.value)
  userStore.setExercisePlan(null)
  router.replace({ name: 'painCheck' })
}
function handleBack() {
  router.push('/')
}
function markTouched(field) {
  touched.value[field] = true
}
onMounted(() => {
  errors.value = {
    age: '', gender: '', height: '', weight: '', silhouette: '', somatotype: ''
  }
  touched.value = {
    age: false, gender: false, height: false, weight: false, silhouette: false, somatotype: false
  }
})
</script>

<style scoped>
.user-profile {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ea 0%, #ffffff 50%, #e8f3e0 100%);
  display: flex;
  flex-direction: column;
  align-items: flex-start;
}
.container {
  width: 100%;
  max-width: 1200px;
  margin: 0 auto;
  padding: 2rem 1rem;
  flex: 1;
}
.back-link {
  display: flex;
  align-items: center;
  margin-bottom: 0.5rem;
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  padding: 0 1rem;
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
  color: #333;
  margin: 0;
  background: linear-gradient(45deg, #4a6741, #6b8f5e);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  text-align: left;
}
.divider {
  width: 100%;
  max-width: 600px;
  height: 2px;
  background: linear-gradient(90deg, #b5cc7a 0%, #eaf5e1 100%);
  margin: 0 auto 18px auto;
  border-radius: 2px;
}
.subtitle {
  color: #666;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  text-align: left;
}
.user-profile-form {
  max-width: 400px;
  margin: 60px auto;
  background: #f8f9fa;
  border-radius: 12px;
  padding: 32px 24px 24px 24px;
  box-shadow: 0 2px 12px rgba(74,103,65,0.08);
  display: flex;
  flex-direction: column;
  gap: 18px;
}
.user-profile-form label {
  display: flex;
  flex-direction: column;
  font-size: 1rem;
  color: #2c3e50;
  margin-bottom: 10px;
  font-weight: 500;
  letter-spacing: 0.02em;
  position: relative;
}
.user-profile-form input,
.user-profile-form select {
  margin-top: 4px;
  padding: 8px 12px;
  border-radius: 8px;
  border: 1.5px solid #b5cc7a;
  font-size: 1rem;
  background: #fff;
  transition: border 0.3s, box-shadow 0.3s;
  outline: none;
}
.user-profile-form input:focus,
.user-profile-form select:focus {
  border: 1.5px solid #4a6741;
  box-shadow: 0 0 0 2px #eaf5e1;
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
  transform: scale(1.06);
  box-shadow: 0 6px 24px rgba(74,103,65,0.18), 0 0 12px #8dc26f88;
}
@keyframes cta-breath {
  0% { transform: scale(1); box-shadow: 0 2px 12px rgba(74,103,65,0.10); }
  100% { transform: scale(1.07); box-shadow: 0 6px 24px rgba(74,103,65,0.18), 0 0 16px #8dc26f55; }
}
.cta-button:disabled {
  opacity: 0.5;
  cursor: not-allowed;
  box-shadow: none;
  animation: none;
}
.error-msg.modern-error {
  display: inline-block;
  background: rgba(232, 243, 224, 0.98);
  color: #4a6741;
  font-size: 0.97em;
  margin-top: 6px;
  min-height: 22px;
  font-weight: 500;
  letter-spacing: 0.01em;
  border-radius: 8px;
  box-shadow: 0 2px 8px rgba(74, 103, 65, 0.08);
  padding: 4px 12px 4px 10px;
  position: absolute;
  left: 0;
  bottom: -28px;
  opacity: 0;
  transform: translateY(8px);
  pointer-events: none;
  transition: opacity 0.25s cubic-bezier(.4,1.4,.6,1), transform 0.25s cubic-bezier(.4,1.4,.6,1);
  z-index: 2;
  animation: fadeInModernError 0.4s cubic-bezier(.4,1.4,.6,1);
}
.error-msg.modern-error:empty {
  opacity: 0;
  pointer-events: none;
}
.error-msg.modern-error:not(:empty) {
  opacity: 1;
  pointer-events: auto;
  transform: translateY(0);
}
@keyframes fadeInModernError {
  0% { opacity: 0; transform: translateY(12px); }
  100% { opacity: 1; transform: translateY(0); }
}
.user-profile-form input.error,
.user-profile-form select.error {
  border: 2px solid #e74c3c !important;
  animation: shake 0.4s cubic-bezier(.36,.07,.19,.97) both;
  background: #fff6f6;
}
@keyframes shake {
  10%, 90% { transform: translateX(-2px); }
  20%, 80% { transform: translateX(4px); }
  30%, 50%, 70% { transform: translateX(-8px); }
  40%, 60% { transform: translateX(8px); }
}
.form-title {
  text-align: center;
  font-size: 1.35rem;
  color: #4a6741;
  font-weight: bold;
  margin-bottom: 18px;
  margin-left: 0;
  letter-spacing: 0.01em;
}
</style> 