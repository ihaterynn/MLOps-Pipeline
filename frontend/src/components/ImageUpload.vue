<script>
import { BACKEND_URL } from '../config.js';

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
        const response = await fetch(`${BACKEND_URL}/predict_image`, {
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
