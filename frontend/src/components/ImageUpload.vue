<template>
  <div class="image-upload">
    <h2>Upload a Nasi Lemak or Roti Canai Image for Prediction</h2>
    <input type="file" @change="onFileChange" accept="image/*" />
    
    <!-- Green Predict Button -->
    <button @click="uploadImage" class="predict-button">Predict</button>

    <div v-if="previewUrl">
      <h3>Preview:</h3>
      <img :src="previewUrl" alt="Image Preview" style="max-width: 300px;" />
    </div>

    <div v-if="prediction !== null" class="prediction-container">
      <h3 class="prediction-text">Prediction: {{ prediction }}</h3>
    </div>
  </div>
</template>

<script>
import { BACKEND_URL } from '../config.js'

export default {
  name: "ImageUpload",
  data() {
    return {
      selectedFile: null,
      previewUrl: null,
      prediction: null
    }
  },
  methods: {
    onFileChange(event) {
      const file = event.target.files[0];
      if (file) {
        this.selectedFile = file;
        this.previewUrl = URL.createObjectURL(file);
      }
    },
    async uploadImage() {
      if (!this.selectedFile) return;

      const formData = new FormData();
      formData.append("file", this.selectedFile);

      try {
          console.log("📤 Sending image to:", `${BACKEND_URL}/predict_image`);

          const response = await fetch(`${BACKEND_URL}/predict_image`, {
              method: "POST",
              body: formData
          });

          console.log("✅ Response received:", response);

          // Check if response is JSON
          const data = await response.json();
          console.log("🔹 Parsed JSON:", data);

          // Ensure "prediction" key exists
          if (data.prediction) {
              this.prediction = data.prediction;
              console.log("🎯 Prediction:", this.prediction);
          } else {
              this.prediction = "Error: No prediction received!";
              console.warn("⚠️ Warning: No prediction in response.");
          }
      } catch (error) {
          console.error("❌ Error uploading image:", error);
          this.prediction = "Error: Server did not respond!";
      }
    }
  }
}
</script>

<style scoped>
.image-upload {
  margin: 20px;
  text-align: center;
  font-family: Arial, sans-serif;
}

/* Green Predict Button */
.predict-button {
  background-color: #1a8e35; /* Green */
  color: white;
  font-size: 16px;
  padding: 10px 15px;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

/* Hover Effect */
.predict-button:hover {
  background-color: #1c7c31; /* Darker Green */
}

/* Larger Prediction Text */
.prediction-container {
  margin-top: 20px;
}

.prediction-text {
  font-size: 24px; /* Bigger font */
  font-weight: bold;
  color: #18dbf0;
}
</style>