<?php
// Include the functions file to access the database and utility functions
include 'includes/functions.php';

// Check if the request method is POST
if ($_SERVER['REQUEST_METHOD'] == 'POST') {
    // Retrieve the task ID from the POST request
    $id = $_POST['id'];
    
    // Check if the status is set in the POST request, if not, set it to null
    $status = isset($_POST['status']) ? $_POST['status'] : null;
    
    // Check if the title is set in the POST request, if not, set it to null
    $title = isset($_POST['title']) ? $_POST['title'] : null;

    // Call the updateTask function to update the task in the database
    if (updateTask($conn, $id, $status, $title)) {
        // If the update is successful, return a success response in JSON format
        echo json_encode(['status' => 'success']);
    } else {
        // If the update fails, return an error response in JSON format
        echo json_encode(['status' => 'error']);
    }
}
?>
