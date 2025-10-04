-- Database initialization script
-- This script creates the database and IMC table

CREATE DATABASE IF NOT EXISTS imc_db;
USE imc_db;

-- Create IMC table
CREATE TABLE IF NOT EXISTS imc (
    id INT AUTO_INCREMENT PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    height INT NOT NULL,
    weight INT NOT NULL,
    imc DECIMAL(5,2) NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Insert some sample data (optional)
INSERT INTO imc (username, height, weight, imc) VALUES 
('john_doe', 175, 70, 22.86),
('jane_smith', 165, 60, 22.04),
('alice_brown', 170, 65, 22.49);