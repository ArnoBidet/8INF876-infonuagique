// server.js
const http = require('http'); // Import Node.js core http module
const url = require('url'); // Import URL module to parse URLs

const hostname = '0.0.0.0'; // Localhost
const port = 3000; // Port to listen on

// Create a server instance
const server = http.createServer((req, res) => {
  // Parse the URL
  const parsedUrl = url.parse(req.url, true);
  const path = parsedUrl.pathname;
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
    
    req.on('end', () => {
        const data = JSON.parse(body);
        const { weight, height } = data;
        
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
        
        res.statusCode = 200;
        res.end(JSON.stringify({
          weight,
          height,
          imc: Math.round(imc * 100) / 100,
          category
        }));
    });
  } 
});

// Start the server and listen for incoming requests
server.listen(port, hostname, () => {
  
  console.log(`Server running at http://${hostname}:${port}/`);
});