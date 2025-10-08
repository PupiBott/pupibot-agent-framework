# Dockerfile for Document Service
FROM node:20

WORKDIR /app

# Install dependencies
COPY package.json ./
RUN npm install --production

# Copy application code
COPY src/ ./src/

# Expose port and run the application
EXPOSE 8081
CMD ["node", "src/index.js"]