<template>
  <div class="navbar">
    <div class="navbar-container">
      <div class="brand-container">
        <router-link to="/" class="brand">
          <div class="brand-text">ArthritEase</div>
        </router-link>
        <div
          v-if="isHomePage"
          class="brand-underline"
          :style="{ backgroundImage: `url(${brushStrokeImg})` }"
        ></div>
      </div>
      <div class="nav-links">
        <div class="nav-item">
          <router-link to="/humidity" class="nav-button">Humidity</router-link>
          <div
            v-if="currentRoute === '/humidity'"
            class="link-underline"
            :style="{ backgroundImage: `url(${brushStrokeImg})` }"
          ></div>
        </div>
        <div class="nav-item">
          <router-link to="/sport-suggestion/mild" class="nav-button">Sport Suggestion</router-link>
          <div
            v-if="currentRoute === '/pain-check'"
            class="link-underline"
            :style="{ backgroundImage: `url(${brushStrokeImg})` }"
          ></div>
        </div>
        <div class="nav-item">
          <router-link to="/body-prediction" class="nav-button">Body Prediction</router-link>
          <div
            v-if="currentRoute === '/body-prediction'"
            class="link-underline"
            :style="{ backgroundImage: `url(${brushStrokeImg})` }"
          ></div>
        </div>
        <div class="nav-item">
          <router-link to="/community" class="nav-button">Community</router-link>
          <div
            v-if="currentRoute === '/community'"
            class="link-underline"
            :style="{ backgroundImage: `url(${brushStrokeImg})` }"
          ></div>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed } from 'vue'
import { useRoute } from 'vue-router'
import brushStrokeImg from '@/assets/brush-stroke.png'

const route = useRoute()
const currentRoute = computed(() => route.path)
const isHomePage = computed(() => route.path === '/' || route.path === '/home')
</script>

<style scoped>
.navbar {
  width: 100%;
  background-color: #ffffff;
  padding: 15px 0;
  margin: 0;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  position: sticky;
  top: 0;
  z-index: 1000;
  transition: all 0.3s ease;
}

.navbar:hover {
  box-shadow: 0 4px 8px rgba(74, 103, 65, 0.2);
}

.navbar-container {
  display: flex;
  align-items: center;
  max-width: 1200px;
  width: 100%;
  margin: 0 auto;
  padding: 0 20px;
}

.brand-container {
  position: relative;
  margin-right: 80px;
}

.brand {
  text-decoration: none;
}

.brand-text {
  color: #4a6741;
  font-weight: bold;
  font-size: 1.8rem;
  font-family: 'Times New Roman', serif;
  transition: all 0.3s ease;
  position: relative;
  display: inline-block;
}

.brand-text:hover {
  transform: scale(1.05);
  color: #3a5331;
  text-shadow: 2px 2px 4px rgba(74, 103, 65, 0.2);
}

.brand-underline {
  position: absolute;
  bottom: -5px;
  left: 0;
  width: 100%;
  height: 15px;
  background-size: 100% 100%;
  background-repeat: no-repeat;
}

.nav-links {
  display: flex;
  gap: 20px;
}

.nav-item {
  position: relative;
  perspective: 1000px;
}

/* New button-like navigation styling */
.nav-button {
  display: block;
  text-decoration: none;
  color: #000;
  font-size: 1.1rem;
  padding: 8px 15px;
  font-weight: 500;
  transition: all 0.3s ease;
  border-radius: 4px;
  background-color: transparent;
  position: relative;
  overflow: hidden;
}

.nav-button::before {
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
  transition: 0.5s;
}

.nav-button:hover::before {
  left: 100%;
}

.nav-button:hover {
  background-color: rgba(74, 103, 65, 0.1);
  color: #4a6741;
  transform: translateY(-2px);
  box-shadow: 0 2px 4px rgba(74, 103, 65, 0.1);
}

/* Active/current route styling */
.router-link-active.nav-button {
  color: #4a6741;
  font-weight: bold;
  background-color: rgba(74, 103, 65, 0.05);
  box-shadow: 0 2px 4px rgba(74, 103, 65, 0.1);
}

.link-underline {
  position: absolute;
  bottom: -8px;
  left: 50%;
  transform: translateX(-50%);
  width: 120%;
  height: 12px;
  background-size: 100% 100%;
  background-repeat: no-repeat;
  transition: all 0.3s ease;
}

.nav-item:hover .link-underline {
  transform: translateX(-50%) scale(1.1);
}

@media (max-width: 768px) {
  .navbar-container {
    flex-direction: column;
    align-items: flex-start;
  }

  .brand-container {
    margin-bottom: 20px;
    margin-right: 0;
  }

  .nav-links {
    width: 100%;
    justify-content: space-between;
    gap: 10px;
  }

  .nav-button {
    text-align: center;
    padding: 8px 10px;
    font-size: 1rem;
  }

  .link-underline {
    width: 100%;
  }
}
</style>
