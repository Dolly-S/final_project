<template>
  <div class="community-page">
    <NavBar />
    <div class="container">
      <h1>社区讨论</h1>
      <CommunityTopic />
    </div>
  </div>
</template>

<script setup>
import NavBar from '@/components/NavBar.vue'
import CommunityTopic from '@/components/CommunityTopic.vue'
</script>

<style scoped>
.community-page {
  width: 100%;
  min-height: 100vh;
  background-color: #f5f5f5;
}

.container {
  max-width: 1200px;
  margin: 0 auto;
  padding: 20px 15px;
}

h1 {
  margin-bottom: 30px;
  color: #333;
  font-size: 2rem;
  text-align: center;
}
</style>
