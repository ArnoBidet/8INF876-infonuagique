
# 📝 PHP To-Do List Web Application
A simple and efficient To-Do List web application built using PHP, HTML, CSS, JavaScript, Bootstrap, and MySQL. This application allows users to add, edit, delete, and update tasks with a user-friendly interface.

## 🌟 Features
- Add new tasks 🆕
- Edit existing tasks ✏️
- Mark tasks as completed ✔️
- Delete tasks ❌
- Responsive design using Bootstrap 📱💻

## 🛠️ Technologies Used
- **Frontend**: HTML, CSS, Bootstrap, JavaScript, jQuery
- **Backend**: PHP, MySQL
- **AJAX**: For seamless updates

## 📝 Setup Instructions

Follow these steps to set up the project locally:

### 1. Clone the Repository
```bash
git clone https://github.com/obadaKraishan/ToDoListPHP.git
cd to-do-list
```

### 2. Set Up the Database
1. Start your local server using XAMPP, WAMP, or MAMP.
2. Open phpMyAdmin and create a new database named `todo_list`.
3. Import the SQL file to set up the `tasks` table:
   ```sql
   CREATE DATABASE todo_list;
   USE todo_list;

   CREATE TABLE tasks (
       id INT AUTO_INCREMENT PRIMARY KEY,
       title VARCHAR(255) NOT NULL,
       status ENUM('pending', 'completed') DEFAULT 'pending',
       created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
   );
   ```

### 3. Configure the Database Connection
Edit `includes/db.php` with your database connection details:
```php
<?php
$servername = "localhost";
$username = "root";
$password = "";
$dbname = "todo_list";

$conn = new mysqli($servername, $username, $password, $dbname);

if ($conn->connect_error) {
    die("Connection failed: " . $conn->connect_error);
}
?>
```

### 4. Run the Application
Open a web browser and navigate to `http://localhost/to-do-list`.

## 🎨 Customization
### 1. Update Styles
Modify the styles in `assets/css/styles.css` to match your design preferences.

### 2. Update JavaScript
Enhance the JavaScript functionality in `assets/js/scripts.js` to customize the interactivity.

### 3. Update Content
Modify the HTML content in `index.php` to personalize the text and tasks.

## 📄 License
This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Contributors
- [Obada Kraishan](https://github.com/obadaKraishan)
