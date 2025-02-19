<script>
import { BACKEND_URL } from '../config.js';

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
        const response = await fetch(`${BACKEND_URL}/predict`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ input_data: this.inputValue })
        });
        const data = await response.json();
        this.responseMessage = data.prediction;
      } catch (error) {
        console.error('Error calling backend:', error);
        this.responseMessage = 'Error calling backend!';
      }
    }
  }
}
</script>
