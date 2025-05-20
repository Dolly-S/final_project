<template>
  <div class="cta-section">
    <div class="cta-container">
      <div class="image-carousel">
        <div
          class="carousel-track"
          :style="{ transform: `translateX(-${currentImageIndex * 100}%)` }"
        >
          <div v-for="(image, index) in exerciseImages" :key="index" class="carousel-slide">
            <img :src="image" :alt="imageAlts[index]" class="carousel-image" />
          </div>
        </div>
      </div>

      <div class="cta-content">
        <h2>How to do we have a suitable exercise?</h2>
        <p>Check with the pain level firstly, and then see the suitable sports for you.</p>
        <router-link to="/pain-check" class="check-now-btn">Check Now!</router-link>
      </div>

      <div class="carousel-indicators">
        <button
          v-for="(_, index) in exerciseImages"
          :key="index"
          class="indicator-dot"
          :class="{ active: currentImageIndex === index }"
          @click="setActiveImage(index)"
        ></button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import bikingImg from '@/assets/cycling.jpg'
import swimmingImg from '@/assets/water-aerobics.jpg'
import waterExerciseImg from '@/assets/aquatic-therapy.jpg'

// Array of exercise images
const exerciseImages = [bikingImg, swimmingImg, waterExerciseImg]

// Image alt texts
const imageAlts = [
  'Elderly person biking outdoors',
  'Elderly person swimming in a pool',
  'Elderly person enjoying water exercise',
]

// Track the current image
const currentImageIndex = ref(0)
let carouselInterval = null

// Function to advance the carousel
const advanceCarousel = () => {
  currentImageIndex.value = (currentImageIndex.value + 1) % exerciseImages.length
}

// Function to set a specific image as active
const setActiveImage = (index) => {
  currentImageIndex.value = index
  // Reset the interval when manually changing slides
  if (carouselInterval) {
    clearInterval(carouselInterval)
    carouselInterval = setInterval(advanceCarousel, 4000)
  }
}

// Set up and clean up the interval
onMounted(() => {
  // Change image every 5 seconds
  carouselInterval = setInterval(advanceCarousel, 4000)
})

onBeforeUnmount(() => {
  // Clear the interval when component is destroyed
  if (carouselInterval) {
    clearInterval(carouselInterval)
  }
})
</script>

<style scoped>
.cta-section {
  width: 100%;
  margin: 50px 0;
}

.cta-container {
  position: relative;
  max-width: 1200px;
  height: 400px;
  margin: 0 auto;
  overflow: hidden;
  border-radius: 12px;
  box-shadow: 0 4px 20px rgba(0, 0, 0, 0.08);
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
}

.cta-container:hover {
  transform: translateY(-5px);
  box-shadow: 0 15px 30px rgba(0, 0, 0, 0.12);
}

.image-carousel {
  width: 100%;
  height: 100%;
  position: relative;
  overflow: hidden;
}

.carousel-track {
  display: flex;
  width: 100%;
  height: 100%;
  transition: transform 0.8s ease-in-out;
}

.carousel-slide {
  min-width: 100%;
  height: 100%;
  flex-shrink: 0;
  position: relative;
  overflow: hidden;
}

.carousel-image {
  width: 100%;
  height: 100%;
  object-fit: cover;
  transition: transform 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  transform-origin: center center;
}

.cta-container:hover .carousel-image {
  transform: scale(1.05);
}

.cta-content {
  position: absolute;
  top: 0;
  left: 0;
  width: 100%;
  height: 100%;
  display: flex;
  flex-direction: column;
  justify-content: center;
  padding-left: 50px;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.4) 0%,
    rgba(0, 0, 0, 0.2) 30%,
    rgba(0, 0, 0, 0) 60%
  );
  color: white;
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
}

.cta-container:hover .cta-content {
  opacity: 1;
  background: linear-gradient(
    to right,
    rgba(0, 0, 0, 0.7) 0%,
    rgba(0, 0, 0, 0.4) 30%,
    rgba(0, 0, 0, 0) 60%
  );
}

.cta-content h2 {
  position: relative;
  font-size: 2.2rem;
  margin-bottom: 15px;
  line-height: 1.3;
  letter-spacing: -0.5px;
  text-shadow: 2px 2px 4px rgba(0, 0, 0, 0.3);
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  max-width: 400px;
  font-weight: 600;
}

.cta-content p {
  font-size: 1.05rem;
  line-height: 1.6;
  letter-spacing: 0.2px;
  text-shadow: 1px 1px 2px rgba(0, 0, 0, 0.2);
  transform: translateY(20px);
  transition: all 0.6s cubic-bezier(0.4, 0, 0.2, 1);
  opacity: 0;
  max-width: 360px;
  font-weight: 400;
  color: rgba(255, 255, 255, 0.95);
}

.cta-container:hover .cta-content h2,
.cta-container:hover .cta-content p,
.cta-container:hover .check-now-btn {
  transform: translateY(0);
  opacity: 1;
}

.check-now-btn {
  position: relative;
  left: 120px;
  display: inline-flex;
  align-items: center;
  background-color: rgba(74, 103, 65, 0.9);
  color: white;
  padding: 10px 24px;
  border-radius: 25px;
  text-decoration: none;
  font-weight: 500;
  font-size: 1.05rem;
  letter-spacing: 0.3px;
  transition: all 0.4s ease;
  border: 2px solid rgba(255, 255, 255, 0.2);
  backdrop-filter: blur(5px);
  width: fit-content;
  transform: translateY(20px);
  opacity: 0;
  box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
  margin: 8px 0 12px;
}

.cta-container:hover .check-now-btn {
  transform: translateY(0);
  opacity: 1;
}

.check-now-btn::after {
  content: "→";
  margin-left: 6px;
  font-size: 1.1em;
  transition: transform 0.3s ease;
}

.check-now-btn:hover {
  background-color: rgba(74, 103, 65, 1);
  border-color: rgba(255, 255, 255, 0.4);
  transform: translateY(-2px) !important;
  box-shadow: 0 6px 20px rgba(0, 0, 0, 0.3);
}

.check-now-btn:hover::after {
  transform: translateX(5px);
}

.carousel-indicators {
  position: absolute;
  bottom: 20px;
  left: 0;
  right: 0;
  display: flex;
  justify-content: center;
  gap: 10px;
  z-index: 2;
}

.indicator-dot {
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background-color: rgba(255, 255, 255, 0.5);
  border: none;
  cursor: pointer;
  transition: all 0.3s ease;
  padding: 0;
}

.indicator-dot:hover,
.indicator-dot.active {
  background-color: white;
}

@media (max-width: 768px) {
  .cta-container {
    height: 350px;
  }

  .cta-content {
    padding-left: 25px;
    padding-right: 20px;
  }

  .cta-content h2 {
    font-size: 1.8rem;
    margin-bottom: 12px;
    line-height: 1.25;
    max-width: 300px;
  }

  .check-now-btn {
    left: 90px;
    padding: 8px 20px;
    font-size: 1rem;
    margin: 6px 0 10px;
  }

  .cta-content p {
    font-size: 1rem;
    line-height: 1.5;
    max-width: 280px;
  }
}

@media (max-width: 480px) {
  .cta-container {
    height: 300px;
  }

  .cta-content {
    width: 100%;
    padding: 25px;
    background: linear-gradient(
      to bottom,
      rgba(0, 0, 0, 0.7) 0%,
      rgba(0, 0, 0, 0.5) 100%
    );
  }

  .cta-content h2 {
    font-size: 1.5rem;
  }

  .cta-content p {
    font-size: 0.95rem;
    margin-bottom: 20px;
  }

  .check-now-btn {
    left: 60px;
  }
}
</style>
