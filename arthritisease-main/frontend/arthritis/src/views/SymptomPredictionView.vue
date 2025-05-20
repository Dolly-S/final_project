<template>
  <div class="symptom-prediction">
    <NavBar />
    <div class="container">
      <div class="back-link">
        <router-link to="/">
          <span class="back-arrow">←</span>
        </router-link>
        <h1>Body Prediction</h1>
      </div>
      <p class="subtitle">Track, Analyze, and Predict Your Body's Progress</p>
      <div class="coming-soon">
        <div class="coming-soon-content">
          <div class="icon">🔮</div>
          <h2>Coming Soon</h2>
          <p>We're working hard to bring you an intelligent symptom prediction system.</p>
          <div class="features">
            <div class="feature">
              <span class="feature-icon">📊</span>
              <span class="feature-text">Data-Driven Insights</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🎯</span>
              <span class="feature-text">Personalized Predictions</span>
            </div>
            <div class="feature">
              <span class="feature-icon">📈</span>
              <span class="feature-text">Progress Tracking</span>
            </div>
            <div class="feature">
              <span class="feature-icon">🔔</span>
              <span class="feature-text">Smart Notifications</span>
            </div>
          </div>
          <p class="stay-tuned">Stay tuned for updates!</p>
        </div>
      </div>
    </div>
    <AppFooter />
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import AppFooter from '@/components/AppFooter.vue'
</script>

<style scoped>
.symptom-prediction {
  width: 100%;
  min-height: 100vh;
  background: linear-gradient(135deg, #f0f7ea 0%, #ffffff 50%, #e8f3e0 100%);
  display: flex;
  flex-direction: column;
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

.coming-soon {
  max-width: 1200px;
  margin-left: auto;
  margin-right: auto;
  background: rgba(255, 255, 255, 0.9);
  border-radius: 24px;
  box-shadow: 0 8px 32px rgba(74, 103, 65, 0.1);
  border: 1px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(10px);
  overflow: hidden;
  transition: transform 0.3s ease, box-shadow 0.3s ease;
}

.coming-soon:hover {
  transform: translateY(-4px);
  box-shadow: 0 12px 40px rgba(74, 103, 65, 0.15);
}

.coming-soon-content {
  padding: 4rem 2rem;
  text-align: center;
}

.icon {
  font-size: 4rem;
  margin-bottom: 1.5rem;
  animation: float 6s ease-in-out infinite;
}

@keyframes float {
  0% { transform: translateY(0px); }
  50% { transform: translateY(-20px); }
  100% { transform: translateY(0px); }
}

h2 {
  font-size: 2rem;
  color: #4a6741;
  margin-bottom: 1rem;
}

.coming-soon p {
  font-size: 1.2rem;
  color: #666;
  max-width: 600px;
  margin: 0 auto 2rem;
  line-height: 1.6;
}

.features {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
  gap: 2rem;
  margin: 3rem 0;
  padding: 0 1rem;
}

.feature {
  display: flex;
  flex-direction: column;
  align-items: center;
  gap: 1rem;
  padding: 1.5rem;
  background: rgba(255, 255, 255, 0.8);
  border-radius: 16px;
  transition: transform 0.3s ease;
}

.feature:hover {
  transform: translateY(-4px);
}

.feature-icon {
  font-size: 2rem;
}

.feature-text {
  font-size: 1.1rem;
  color: #4a6741;
  font-weight: 500;
}

.stay-tuned {
  font-style: italic;
  color: #888;
  margin-top: 2rem;
}

@media (max-width: 768px) {
  .container {
    padding: 1rem;
  }

  h1 {
    font-size: 2rem;
  }

  .coming-soon-content {
    padding: 2rem 1rem;
  }

  .features {
    grid-template-columns: 1fr;
    gap: 1rem;
  }

  .feature {
    padding: 1rem;
  }
}
</style>
