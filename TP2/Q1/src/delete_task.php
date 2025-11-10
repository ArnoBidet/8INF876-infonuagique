<?php
// Include the functions file to access the database and utility functions
include 'includes/functions.php';

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve the task ID from the POST request
    $id = $_POST['id'];

    // Call the deleteTask function to delete the task from the database
    if (deleteTask($conn, $id)) {
        // If the deletion is successful, return a success response in JSON format
        echo json_encode(['status' => 'success']);
    } else {
        // If the deletion fails, return an error response in JSON format
        echo json_encode(['status' => 'error']);
    }
}
?>
