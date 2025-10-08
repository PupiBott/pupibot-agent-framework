const express = require('express');
const cors = require('cors');

const app = express();

// Middleware
app.use(express.json());
app.use(cors());

// Health check endpoint
app.get('/health', (req, res) => {
  res.json({ status: 'ok', service: 'document-service' });
});

// Generate endpoint
app.post('/generate', (req, res) => {
  const { payload } = req.body;
  if (!payload) {
    return res.status(400).json({ status: 'error', message: 'Payload is required' });
  }

  res.json({
    status: 'ok',
    service: 'document-service',
    document: `Contenido generado a partir de ${payload}`,
  });
});

// Start the server
const PORT = 8081;
app.listen(PORT, () => {
  console.log(`Document Service is running on port ${PORT}`);
});