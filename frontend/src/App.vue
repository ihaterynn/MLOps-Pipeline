<template>
  <div>
    <h1>My Simple MLOps Frontend</h1>
    <HelloWorld />
    <ImageUpload />
  </div>
</template>

<script>
import HelloWorld from './components/HelloWorld.vue'
import ImageUpload from './components/ImageUpload.vue'

export default {
  name: 'App',
  components: {
    HelloWorld,
    ImageUpload
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
