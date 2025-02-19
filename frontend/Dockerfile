# Use a lightweight Node.js image
FROM node:18

# Set working directory
WORKDIR /app

# Copy package.json and package-lock.json
COPY package*.json ./

# Install dependencies
RUN npm install

# Copy rest of the frontend files
COPY . .

# Expose port for Vite
EXPOSE 5173

# Start frontend
CMD ["npm", "run", "dev"]
