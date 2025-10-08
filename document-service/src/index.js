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

// Start the server
const PORT = 8081;
app.listen(PORT, () => {
  console.log(`Document Service is running on port ${PORT}`);
});