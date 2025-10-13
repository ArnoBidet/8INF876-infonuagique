<?php
// Include the database connection file
include 'db.php';

/**
 * Retrieve all tasks from the database.
 *
 * @param mysqli $conn The database connection.
 * @return mysqli_result|bool The result set from the query, or false on failure.
 */
function getTasks($conn) {
    // SQL query to select all tasks, ordered by creation time in descending order
    $sql = "SELECT * FROM tasks ORDER BY created_at DESC";
    // Execute the query and return the result
    $result = $conn->query($sql);
    return $result;
}

/**
 * Add a new task to the database.
 *
 * @param mysqli $conn The database connection.
 * @param string $title The title of the task.
 * @return bool True on success, false on failure.
 */
function addTask($conn, $title) {
    // Prepare the SQL statement for inserting a new task
    $stmt = $conn->prepare("INSERT INTO tasks (title) VALUES (?)");
    // Bind the task title to the SQL statement
    $stmt->bind_param("s", $title);
    // Execute the statement and return the result
    return $stmt->execute();
}

/**
 * Delete a task from the database.
 *
 * @param mysqli $conn The database connection.
 * @param int $id The ID of the task to delete.
 * @return bool True on success, false on failure.
 */
function deleteTask($conn, $id) {
    // Prepare the SQL statement for deleting a task
    $stmt = $conn->prepare("DELETE FROM tasks WHERE id = ?");
    // Bind the task ID to the SQL statement
    $stmt->bind_param("i", $id);
    // Execute the statement and return the result
    return $stmt->execute();
}

/**
 * Update a task in the database.
 *
 * @param mysqli $conn The database connection.
 * @param int $id The ID of the task to update.
 * @param string|null $status The new status of the task (optional).
 * @param string|null $title The new title of the task (optional).
 * @return bool True on success, false on failure.
 */
function updateTask($conn, $id, $status = null, $title = null) {
    // Check if the status is provided
    if ($status !== null) {
        // Prepare the SQL statement for updating the task status
        $stmt = $conn->prepare("UPDATE tasks SET status = ? WHERE id = ?");
        // Bind the new status and task ID to the SQL statement
        $stmt->bind_param("si", $status, $id);
    } 
    // Check if the title is provided
    elseif ($title !== null) {
        // Prepare the SQL statement for updating the task title
        $stmt = $conn->prepare("UPDATE tasks SET title = ? WHERE id = ?");
        // Bind the new title and task ID to the SQL statement
        $stmt->bind_param("si", $title, $id);
    }
    // Execute the statement and return the result
    return $stmt->execute();
}
?>
