<?php
// Include the functions file to access the database and utility functions
include 'includes/functions.php';

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve the task title from the POST request
    $title = $_POST['task'];

    // Call the addTask function to add the new task to the database
    if (addTask($conn, $title)) {
        // If the task addition is successful, return a success response in JSON format
        echo json_encode(['status' => 'success']);
    } else {
        // If the task addition fails, return an error response in JSON format
        echo json_encode(['status' => 'error']);
    }
}
?>
