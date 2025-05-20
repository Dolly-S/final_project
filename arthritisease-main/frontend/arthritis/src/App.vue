<template>
  <div id="app">
    <router-view></router-view>
    <SaraAssistant />
  </div>
</template>

<script setup>
import SaraAssistant from '@/components/SaraAssistant.vue'
</script>

<style>
* {
  box-sizing: border-box;
  margin: 0;
  padding: 0;
}

html,
body {         
  width: 100%;
  min-height: 100vh;
  margin: 0;
  padding: 0;
  overflow-x: hidden;
  font-family: 'Arial', sans-serif;
  line-height: 1.6;
  color: #333;
}

#app {
  width: 100%;
  min-height: 100vh;
  font-family: Arial, sans-serif;
  -webkit-font-smoothing: antialiased;
  -moz-osx-font-smoothing: grayscale;
  position: relative;
}

img {
  max-width: 100%;
}

a {
  color: inherit;
  text-decoration: none;
}
</style>
