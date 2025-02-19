<template>
  <div>
    <p>Hello from Vue.js!</p>
    <p>Type something to send to the backend:</p>
    <input v-model="inputValue" />
    <button @click="sendToBackend">Send</button>
    <p>{{ responseMessage }}</p>
  </div>
</template>

<script>
export default {
  name: 'HelloWorld',
  data() {
    return {
      inputValue: '',
      responseMessage: ''
    }
  },
  methods: {
    async sendToBackend() {
      try {
        const response = await fetch('http://127.0.0.1:8000/predict', {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input_data: this.inputValue })
        })
        const data = await response.json()
        this.responseMessage = data.prediction
      } catch (error) {
        console.error('Error calling backend:', error)
        this.responseMessage = 'Error calling backend!'
      }
    }
  }
}
</script>
