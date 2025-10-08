const express = require('express');
const cors = require('cors');

const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'image-generator' });
});

// Generate endpoint
app.post('/generate', (req, res) => {
  const { payload } = req.body;
  if (!payload) {
    return res.status(400).json({ status: 'error', message: 'Payload is required' });
  }

  res.json({
    status: 'ok',
    service: 'image-generator',
    image_url: `http://fake.local/${payload}.png`,
  });
});

// Start the server
const PORT = 8082;
app.listen(PORT, () => {
  console.log(`Image Generator Service is running on port ${PORT}`);
});