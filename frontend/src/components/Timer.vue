<template>
    <div class="timer-box">
      <p>{{ message }}</p>
    </div>
  </template>
  
  <script setup>
  import { ref, onMounted, onUnmounted } from 'vue'
  import { BACKEND_URL } from '../config.js'
  
  const message = ref("Waiting for a random message...")
  
  async function fetchRandomMessage() {
    try {
      const response = await fetch(`${BACKEND_URL}/random_message`, {
        method: "POST"
      });
      const data = await response.json();
      if (data.message) {
        message.value = data.message;
      }
    } catch (error) {
      console.error("Error fetching random message:", error);
      message.value = "Error fetching message!";
    }
  }
  
  let intervalId;
  onMounted(() => {
    fetchRandomMessage(); 
    intervalId = setInterval(fetchRandomMessage, 6000);
  });
  
  onUnmounted(() => {
    clearInterval(intervalId);
  });
  </script>
  
  <style scoped>
  .timer-box {
    border: 1px solid #ccc;
    padding: 1rem;
    margin: 1rem 0;
    border-radius: 4px;
    background-color: #f9f9f9;
    text-align: center;
    font-size: 1.2rem;
    font-family: monospace;
    color: black;
  }
  </style>
  