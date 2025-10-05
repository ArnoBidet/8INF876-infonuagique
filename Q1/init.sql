-- Database initialization script
-- This script creates the database and IMC table
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

-- Insert some sample data only if table is empty
INSERT IGNORE INTO imc (id, username, height, weight, imc) VALUES 
(1, 'john_doe', 175, 70, 22.86),
(2, 'jane_smith', 165, 60, 22.04),
('alice_brown', 170, 65, 22.49);