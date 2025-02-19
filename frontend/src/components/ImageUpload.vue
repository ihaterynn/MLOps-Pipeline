<template>
    <div class="image-upload">
      <h2>Upload an Image for Prediction</h2>
      <input type="file" @change="onFileChange" accept="image/*" />
      <button @click="uploadImage" :disabled="!selectedFile">Predict</button>
      <div v-if="previewUrl">
        <h3>Preview:</h3>
        <img :src="previewUrl" alt="Image Preview" style="max-width: 300px;" />
      </div>
      <div v-if="prediction !== null">
        <h3>Prediction: {{ prediction }}</h3>
      </div>
    </div>
  </template>
  
  <script>
  export default {
    name: "ImageUpload",
    data() {
      return {
        selectedFile: null,
        previewUrl: null,
        prediction: null
      };
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
          const response = await fetch("http://127.0.0.1:8000/predict_image", {
            method: "POST",
            body: formData
          });
          const data = await response.json();
          this.prediction = data.prediction;
        } catch (error) {
          console.error("Error uploading image:", error);
        }
      }
    }
  };
  </script>
  
  <style scoped>
  .image-upload {
    margin: 20px;
  }
  </style>
  