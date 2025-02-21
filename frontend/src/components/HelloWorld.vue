<script setup>
/**
 * Combining old script setup code with new backend call logic.
 */
import { ref } from 'vue'
import { BACKEND_URL } from '../config.js'

// Props from the old template
defineProps({
  msg: String,
})

// The old counter
const count = ref(0)

// New fields for the backend call
const inputValue = ref('')
const responseMessage = ref('')

// New method to call the backend
async function sendToBackend() {
  try {
    const response = await fetch(`${BACKEND_URL}/predict`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ input_data: inputValue.value })
    })
    const data = await response.json()
    responseMessage.value = data.prediction
  } catch (error) {
    console.error('Error calling backend:', error)
    responseMessage.value = 'Error calling backend!'
  }
}
</script>

<template>
  <h1>{{ msg }}</h1>

  <div class="card">
    <!-- Old code: Counter button -->
    <button type="button" @click="count++" class="green-button">
      CLICK ME, Count is: {{ count }}
    </button>
  </div>

  <!-- New code: Input + button to call the backend -->
  <div style="margin-top: 1rem;">
    <p>Type something to call Server to display back:</p>
    <input v-model="inputValue" />
    <button @click="sendToBackend" class="green-button">Send</button>
    <p>{{ responseMessage }}</p>
  </div>
</template>

<style scoped>
/* Green Buttons */
.green-button {
  background-color: #1a8e35; /* Green */
  color: white;
  font-size: 16px;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
  transition: background-color 0.3s;
}

/* Hover Effect */
.green-button:hover {
  background-color: #218838; /* Darker Green */
}
</style>
