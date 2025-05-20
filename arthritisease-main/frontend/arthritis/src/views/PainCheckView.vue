<template>
  <div class="pain-check">
    <NavBar />
    <div class="container">
      <div v-if="editProfile || !userStore.user_profile" class="user-profile-form animate-fade-in">
        <h2>{{ userStore.user_profile ? 'Edit Your Profile' : 'Complete Your Profile' }}</h2>
        <form @submit.prevent="submitProfile">
          <label>Age:
            <input v-model.number="profile.age" type="number" min="1" max="120" required placeholder="Enter your age" @input="validateAge" @blur="onBlur('age')" :class="{ error: errors.age }" />
            <span v-if="errors.age" class="error-msg modern-error">{{ errors.age }}</span>
          </label>
          <label>Gender:
            <select v-model="profile.gender" required @change="validateGender" @blur="onBlur('gender')" :class="{ error: errors.gender }">
              <option value="" disabled>Select gender</option>
              <option value="male">Male</option>
              <option value="female">Female</option>
            </select>
            <span v-if="errors.gender" class="error-msg modern-error">{{ errors.gender }}</span>
          </label>
          <label>Height (cm):
            <input v-model.number="profile.height" type="number" min="50" max="250" required placeholder="e.g. 170" @input="validateHeight" @blur="onBlur('height')" :class="{ error: errors.height }" />
            <span v-if="errors.height" class="error-msg modern-error">{{ errors.height }}</span>
          </label>
          <label>Weight (kg):
            <input v-model.number="profile.weight" type="number" min="20" max="300" required placeholder="e.g. 65" @input="validateWeight" @blur="onBlur('weight')" :class="{ error: errors.weight }" />
            <span v-if="errors.weight" class="error-msg modern-error">{{ errors.weight }}</span>
          </label>
          <label>Silhouette:
            <select v-model="profile.silhouette" required @change="validateSilhouette" @blur="onBlur('silhouette')" :class="{ error: errors.silhouette }">
              <option value="" disabled>Select silhouette</option>
              <option value="apple">Apple</option>
              <option value="pear">Pear</option>
              <option value="rectangle">Rectangle</option>
              <option value="hourglass">Hourglass</option>
              <option value="inverted">Inverted Triangle</option>
            </select>
            <span v-if="errors.silhouette" class="error-msg modern-error">{{ errors.silhouette }}</span>
          </label>
          <label>Somatotype:
            <select v-model="profile.somatotype" required @change="validateSomatotype" @blur="onBlur('somatotype')" :class="{ error: errors.somatotype }">
              <option value="" disabled>Select somatotype</option>
              <option value="ectomorph">Ectomorph (slim)</option>
              <option value="mesomorph">Mesomorph (athletic)</option>
              <option value="endomorph">Endomorph (round)</option>
            </select>
            <span v-if="errors.somatotype" class="error-msg modern-error">{{ errors.somatotype }}</span>
          </label>
          <button type="submit" class="cta-button" :disabled="!isFormValid">
            {{ userStore.user_profile ? 'Save Profile' : 'Save and Start Pain Check' }} <span class="cta-arrow">→</span>
          </button>
          <button type="button" class="clear-form-btn" @click="clearForm">Clear Form</button>
          <button v-if="userStore.user_profile" type="button" class="cancel-edit-btn" @click="cancelEdit">Cancel</button>
        </form>
      </div>
      <div v-else>
        <div class="back-link">
          <router-link to="#" @click.prevent="handleBack">
            <span class="back-arrow">←</span>
          </router-link>
          <h1>Pain Assessment</h1>
        </div>
        <p class="subtitle">Track and monitor your arthritis symptoms</p>
        <button class="edit-profile-btn" @click="editProfile = true">Edit Profile</button>
        <PainCheckForm />
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import PainCheckForm from '@/components/PainCheckForm.vue'
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
const triedSubmit = ref(false)
const shakeFields = ref({})
const editProfile = ref(false)
function validateAge() {
  if (!profile.value.age || isNaN(profile.value.age)) {
    errors.value.age = triedSubmit.value ? 'Age is required.' : ''
  } else if (profile.value.age < 1 || profile.value.age > 120) {
    errors.value.age = 'Age must be between 1 and 120.'
  } else {
    errors.value.age = ''
  }
}
function validateGender() {
  errors.value.gender = profile.value.gender ? '' : (triedSubmit.value ? 'Gender is required.' : '')
}
function validateHeight() {
  if (!profile.value.height || isNaN(profile.value.height)) {
    errors.value.height = triedSubmit.value ? 'Height is required.' : ''
  } else if (profile.value.height < 50 || profile.value.height > 250) {
    errors.value.height = 'Height must be between 50 and 250 cm.'
  } else {
    errors.value.height = ''
  }
}
function validateWeight() {
  if (!profile.value.weight || isNaN(profile.value.weight)) {
    errors.value.weight = triedSubmit.value ? 'Weight is required.' : ''
  } else if (profile.value.weight < 20 || profile.value.weight > 300) {
    errors.value.weight = 'Weight must be between 20 and 300 kg.'
  } else {
    errors.value.weight = ''
  }
}
function validateSilhouette() {
  errors.value.silhouette = profile.value.silhouette ? '' : (triedSubmit.value ? 'Silhouette is required.' : '')
}
function validateSomatotype() {
  errors.value.somatotype = profile.value.somatotype ? '' : (triedSubmit.value ? 'Somatotype is required.' : '')
}
const isFormValid = computed(() => {
  validateAge();
  validateGender();
  validateHeight();
  validateWeight();
  validateSilhouette();
  validateSomatotype();
  return (
    !errors.value.age &&
    !errors.value.gender &&
    !errors.value.height &&
    !errors.value.weight &&
    !errors.value.silhouette &&
    !errors.value.somatotype &&
    profile.value.age &&
    profile.value.gender &&
    profile.value.height &&
    profile.value.weight &&
    profile.value.silhouette &&
    profile.value.somatotype
  )
})
function submitProfile() {
  triedSubmit.value = true
  validateAge();
  validateGender();
  validateHeight();
  validateWeight();
  validateSilhouette();
  validateSomatotype();
  if (!isFormValid.value) return
  userStore.setUserProfile(profile.value)
  userStore.setExercisePlan(null)
  editProfile.value = false
}
function clearForm() {
  profile.value = {
    age: '',
    gender: '',
    height: '',
    weight: '',
    silhouette: '',
    somatotype: ''
  }
  errors.value = {
    age: '',
    gender: '',
    height: '',
    weight: '',
    silhouette: '',
    somatotype: ''
  }
  triedSubmit.value = false
}
function onBlur(field) {
  switch (field) {
    case 'age': validateAge(); break;
    case 'gender': validateGender(); break;
    case 'height': validateHeight(); break;
    case 'weight': validateWeight(); break;
    case 'silhouette': validateSilhouette(); break;
    case 'somatotype': validateSomatotype(); break;
  }
  if (errors.value[field]) {
    shakeFields.value[field] = true
    setTimeout(() => { shakeFields.value[field] = false }, 500)
  }
}
function handleBack() {
  if (userStore.user_profile) {
    router.push('/')
  } else {
    clearForm()
    // 保持在当前页面，表单已清空
  }
}
function cancelEdit() {
  // 恢复为userStore中的profile
  Object.assign(profile.value, userStore.user_profile)
  errors.value = {
    age: '', gender: '', height: '', weight: '', silhouette: '', somatotype: ''
  }
  triedSubmit.value = false
  editProfile.value = false
}
onMounted(() => {
  if (!userStore.user_profile) {
    router.replace('/user-profile')
  }
})
</script>

<style scoped>
.pain-check {
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
.user-profile-form h2 {
  text-align: center;
  color: #4a6741;
  margin-bottom: 18px;
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
.clear-form-btn {
  margin-top: 10px;
  padding: 8px 16px;
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
.clear-form-btn:hover {
  background: #4a6741;
  color: #fff;
  transform: scale(1.04);
  box-shadow: 0 4px 16px rgba(74,103,65,0.10);
}
.modern-error {
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
.subtitle {
  color: #666;
  margin-top: 0.5rem;
  margin-bottom: 2rem;
  font-size: 1.1rem;
  text-align: left;
}
.edit-profile-btn {
  margin-bottom: 18px;
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
.cancel-edit-btn {
  margin-top: 10px;
  padding: 8px 16px;
  background: #fff;
  color: #e74c3c;
  border: 2px solid #e74c3c;
  border-radius: 20px;
  font-weight: bold;
  font-size: 1rem;
  cursor: pointer;
  transition: background 0.3s, color 0.3s, box-shadow 0.3s, transform 0.2s;
  box-shadow: 0 1px 6px rgba(231,76,60,0.06);
  letter-spacing: 1px;
  display: inline-block;
}
.cancel-edit-btn:hover {
  background: #e74c3c;
  color: #fff;
  transform: scale(1.04);
  box-shadow: 0 4px 16px rgba(231,76,60,0.10);
}
</style>
