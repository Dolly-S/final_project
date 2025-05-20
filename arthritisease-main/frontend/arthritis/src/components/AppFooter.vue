<template>
  <footer class="footer">
    <div class="footer-wave">
      <svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 1440 120">
        <path
          fill="#e8efd1"
          fill-opacity="1"
          d="M0,64L60,64C120,64,240,64,360,58.7C480,53,600,43,720,48C840,53,960,75,1080,80C1200,85,1320,75,1380,69.3L1440,64L1440,120L1380,120C1320,120,1200,120,1080,120C960,120,840,120,720,120C600,120,480,120,360,120C240,120,120,120,60,120L0,120Z"
        ></path>
      </svg>
    </div>

    <div class="footer-content">
      <div class="footer-section brand-section">
        <div class="footer-brand">
          <span class="brand-name">ArthritEase</span>
          <span class="brand-dot"></span>
        </div>
        <p class="footer-description">
          Helping arthritis patients better manage health with personalized exercise suggestions and weather alerts.
        </p>
      </div>

      <div class="footer-section">
        <h3>Quick Links</h3>
        <nav class="footer-links">
          <router-link to="/humidity">
            <span class="link-icon">→</span>Humidity
          </router-link>
          <router-link to="/sport-suggestion/mild">
            <span class="link-icon">→</span>Sport Suggestion
          </router-link>
          <router-link to="/symptom-prediction">
            <span class="link-icon">→</span>Body Prediction
          </router-link>
          <router-link to="/community">
            <span class="link-icon">→</span>Community
          </router-link>
        </nav>
      </div>
    </div>

    <div class="footer-bottom">
      <p>&copy; 2025 ArthritEase. All rights reserved.</p>
    </div>
  </footer>
</template>

<script setup>
// No additional logic needed
</script>

<style scoped>
.footer {
  position: relative;
  background: linear-gradient(to bottom, #e8efd1, #d8e9b2);
  padding: 35px 20px 10px;
  width: 100%;
  color: #4a6741;
  overflow: hidden;
}

.footer-wave {
  position: absolute;
  top: -80px;
  left: 0;
  width: 100%;
  overflow: hidden;
  line-height: 0;
  z-index: 1;
  transform: scale(1.2, 0.7);
}

.footer-content {
  position: relative;
  z-index: 2;
  display: grid;
  grid-template-columns: 2fr 1fr 1fr;
  gap: 20px;
  max-width: 1200px;
  margin: 0 auto;
  padding-bottom: 15px;
  border-bottom: 1px solid rgba(74, 103, 65, 0.15);
}

.footer-section {
  padding: 0 5px;
}

.brand-section {
  position: relative;
}

.footer-section h3 {
  font-size: 1rem;
  margin-bottom: 12px;
  color: #4a6741;
  font-weight: 600;
  position: relative;
  display: inline-block;
}

.footer-section h3::after {
  content: '';
  position: absolute;
  left: 0;
  bottom: -3px;
  width: 30px;
  height: 2px;
  background-color: #8bb978;
  transition: width 0.3s ease;
}

.footer-section:hover h3::after {
  width: 45px;
}

.footer-brand {
  display: flex;
  align-items: center;
  margin-bottom: 8px;
}

.brand-name {
  font-size: 1.5rem;
  font-weight: bold;
  color: #4a6741;
  background: linear-gradient(45deg, #4a6741, #8bb978);
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}

.brand-dot {
  width: 6px;
  height: 6px;
  background-color: #8bb978;
  border-radius: 50%;
  margin-left: 4px;
  display: inline-block;
}

.footer-description {
  font-size: 0.85rem;
  line-height: 1.4;
  color: #5a7751;
  max-width: 90%;
}

.footer-links {
  display: flex;
  flex-direction: column;
  gap: 8px;
}

.footer-links a {
  color: #5a7751;
  text-decoration: none;
  transition: all 0.3s ease;
  font-size: 0.85rem;
  display: flex;
  align-items: center;
  padding: 3px 0;
}

.link-icon {
  opacity: 0;
  margin-right: 6px;
  font-size: 0.7rem;
  transform: translateX(-10px);
  transition: all 0.3s ease;
}

.footer-links a:hover {
  color: #4a6741;
  transform: translateX(3px);
}

.footer-links a:hover .link-icon {
  opacity: 1;
  transform: translateX(0);
}

.footer-bottom {
  position: relative;
  z-index: 2;
  max-width: 1200px;
  margin: 10px auto 0;
  padding-top: 10px;
  display: flex;
  justify-content: space-between;
  align-items: center;
  color: #5a7751;
  font-size: 0.75rem;
}

.footer-bottom-links {
  display: flex;
  gap: 15px;
  align-items: center;
}

.footer-bottom-links a {
  color: #5a7751;
  text-decoration: none;
  transition: color 0.3s ease;
  position: relative;
}

.footer-bottom-links a::after {
  content: '';
  position: absolute;
  width: 0;
  height: 1px;
  bottom: -2px;
  left: 0;
  background-color: #4a6741;
  transition: width 0.3s ease;
}

.footer-bottom-links a:hover {
  color: #4a6741;
}

.footer-bottom-links a:hover::after {
  width: 100%;
}

.separator {
  width: 3px;
  height: 3px;
  background-color: #8bb978;
  border-radius: 50%;
  display: inline-block;
}

@media (max-width: 768px) {
  .footer {
    padding-top: 30px;
    padding-bottom: 8px;
  }
  
  .footer-wave {
    display: none;
  }
  
  .footer-content {
    grid-template-columns: 1fr;
    text-align: center;
    gap: 20px;
    padding-bottom: 10px;
  }

  .footer-section {
    display: flex;
    flex-direction: column;
    align-items: center;
    padding: 0;
  }
  
  .footer-section h3::after {
    left: 50%;
    transform: translateX(-50%);
  }
  
  .footer-description {
    max-width: 100%;
  }
  
  .footer-links a {
    justify-content: center;
  }
  
  .link-icon {
    opacity: 1;
    transform: translateX(0);
  }

  .footer-bottom {
    flex-direction: column;
    gap: 10px;
    text-align: center;
  }
}
</style>
