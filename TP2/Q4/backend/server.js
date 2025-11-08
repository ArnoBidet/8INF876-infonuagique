const express = require("express");
const cors = require("cors");
const { Pool } = require("pg");

const app = express();
const port = 3000;

app.use(cors()); //autoriser toutes les origines

const pool = new Pool({
  user: "postgres",
  host: "postgres-service",
  database: "postgres",
  password: process.env.POSTGRES_PASSWORD,
  port: 5432,
});

app.get("/", (req, res) => {
  res.send("Hello from Node.js backend via Kubernetes!");
});

app.get("/db", async (req, res) => {
  try {
    const result = await pool.query("SELECT NOW() as time");
    res.json(result.rows[0]);
  } catch (err) {
    console.error(err);
    res.status(500).send("Database error");
  }
});

app.listen(port, () => {
  console.log(`Backend running on port ${port}`);
});
