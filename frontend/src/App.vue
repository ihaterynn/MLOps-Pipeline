<template>
  <div>
    <h1>The Malaysia Boleh Website</h1>
    <HelloWorld />
    <ImageUpload />
    <Timer />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import ImageUpload from './components/ImageUpload.vue'
import Timer from './components/Message.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    ImageUpload,
    Timer
  }
}
</script>

<style>
/* Global styles */
body {
  margin: 0;
  font-family: sans-serif;
}
</style>
