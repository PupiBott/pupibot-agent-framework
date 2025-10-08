# Dockerfile for Image Generator
FROM node:20-alpine

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --production

# Copy application code
COPY src/ ./src/

# Expose port and run the application
EXPOSE 8082
CMD ["npm", "start"]