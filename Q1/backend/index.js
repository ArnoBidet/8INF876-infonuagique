// server.js
const http = require('http'); // Import Node.js core http module
const mysql = require('mysql2/promise'); // Import MySQL driver

const hostname = '0.0.0.0'; // Localhost
const port = 3000; // Port to listen on

// Database connection configuration

function getEnvVar(name) {
  const value = process.env[name];
  if (!value) {
    throw new Error(`Environment variable ${name} is required but not set`);
  }
  return value;
}

const dbConfig = {
  host: getEnvVar('MYSQL_HOST'),
  user: getEnvVar('MYSQL_USER'),
  password: getEnvVar('MYSQL_PASSWORD'),
  database: getEnvVar('MYSQL_DATABASE'),
  waitForConnections: true,
  connectionLimit: 10,
  queueLimit: 0
};

console.log(dbConfig);
// Create connection pool
const pool = mysql.createPool(dbConfig);

// Function to wait for database connection
async function waitForDatabase() {
  let attempts = 0;
  const maxAttempts = 30;

  while (attempts < maxAttempts) {
    try {
      await pool.execute('SELECT 1');
      console.log('Database connected successfully');
      return;
    } catch (error) {
      attempts++;
      console.log(`Database connection attempt ${attempts}/${maxAttempts} failed. Retrying in 2 seconds...`);
      await new Promise(resolve => setTimeout(resolve, 2000));
    }
  }

  throw new Error('Could not connect to database after maximum attempts');
}

// Create a server instance
const server = http.createServer(async (req, res) => {
  const requestUrl = new URL(req.url, `http://${req.headers.host}`);
  const path = requestUrl.pathname;
  const method = req.method;

  // Set common headers
  res.setHeader('Content-Type', 'application/json');
  res.setHeader('Access-Control-Allow-Origin', '*');
  res.setHeader('Access-Control-Allow-Methods', 'GET, POST, OPTIONS');
  res.setHeader('Access-Control-Allow-Headers', 'Content-Type');

  if (path === '/imc' && method === 'POST') {
    // POST /imc route
    let body = '';

    req.on('data', chunk => {
      body += chunk.toString();
    });

    req.on('end', async () => {
      try {
        const data = JSON.parse(body);
        const { weight, height, username } = data;

        const imc = weight / (height * height);
        let category = '';

        if (imc < 18.5) {
          category = "Insuffisance pondérale (maigreur)";
        } else if (imc < 25) {
          category = "Corpulence normale";
        } else if (imc < 30) {
          category = "Surpoids";
        } else if (imc < 35) {
          category = "Obésité modérée";
        } else if (imc < 40) {
          category = "Obésité sévère";
        } else {
          category = "Obésité morbide";
        }

        const imcRounded = Math.round(imc * 100) / 100;

        // Save to database
        const [result] = await pool.execute(
          'INSERT INTO imc (username, height, weight, imc) VALUES (?, ?, ?, ?)',
          [username || 'anonymous', height, weight, imcRounded]
        );

        res.statusCode = 200;
        res.end(JSON.stringify({
          id: result.insertId,
          weight,
          height,
          imc: imcRounded,
          category,
          username: username || 'anonymous'
        }));
      } catch (error) {
        console.error('Database error:', error);
        res.statusCode = 500;
        res.end(JSON.stringify({ error: 'Internal server error' }));
      }
    });
  } else if (path === '/imc' && method === 'GET') {
    // GET /imc route - retrieve all IMC records
    try {
      const [rows] = await pool.execute('SELECT * FROM imc ORDER BY id DESC');
      res.statusCode = 200;
      res.end(JSON.stringify(rows));
    } catch (error) {
      console.error('Database error:', error);
      res.statusCode = 500;
      res.end(JSON.stringify({ error: 'Internal server error' }));
    }
  } else if (method === 'OPTIONS') {
    // Handle preflight requests
    res.statusCode = 200;
    res.end();
  } else {
    // 404 Not Found
    res.statusCode = 404;
    res.end(JSON.stringify({ error: 'Not found' }));
  }
});

// Start the server and listen for incoming requests
async function startServer() {
  try {
    await waitForDatabase();
    server.listen(port, hostname, () => {
      console.log(`Server running at http://${hostname}:${port}/`);
    });
  } catch (error) {
    console.error('Failed to start server:', error);
    process.exit(1);
  }
}

startServer();