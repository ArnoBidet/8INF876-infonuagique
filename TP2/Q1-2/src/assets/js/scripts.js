// When the document is fully loaded and ready
$(document).ready(function() {
    // Attach a submit event handler to the form with ID 'addTaskForm'
    $('#addTaskForm').on('submit', function(e) {
        e.preventDefault(); // Prevent the default form submission behavior

        // Send an AJAX POST request to add_task.php
        $.ajax({
            url: 'add_task.php', // URL of the PHP file to handle the request
            method: 'POST', // HTTP method for the request
            data: $(this).serialize(), // Serialize the form data
            success: function(response) { // Callback function to handle success
                let res = JSON.parse(response); // Parse the JSON response
                if (res.status == 'success') {
                    location.reload(); // Reload the page if the task was added successfully
                } else {
                    alert('Failed to add task'); // Show an error message if the task addition failed
                }
            }
        });
    });
});

// Function to delete a task
function deleteTask(id) {
    // Send an AJAX POST request to delete_task.php
    $.ajax({
        url: 'delete_task.php', // URL of the PHP file to handle the request
        method: 'POST', // HTTP method for the request
        data: { id: id }, // Data to be sent to the server (task ID)
        success: function(response) { // Callback function to handle success
            let res = JSON.parse(response); // Parse the JSON response
            if (res.status == 'success') {
                location.reload(); // Reload the page if the task was deleted successfully
            } else {
                alert('Failed to delete task'); // Show an error message if the task deletion failed
            }
        }
    });
}

// Function to update a task's status
function updateTask(id, status) {
    // Send an AJAX POST request to update_task.php
    $.ajax({
        url: 'update_task.php', // URL of the PHP file to handle the request
        method: 'POST', // HTTP method for the request
        data: { id: id, status: status }, // Data to be sent to the server (task ID and new status)
        success: function(response) { // Callback function to handle success
            let res = JSON.parse(response); // Parse the JSON response
            if (res.status == 'success') {
                // Find the complete button for the task
                let button = $('#task-' + id + ' .btn-complete');
                if (status == 'completed') {
                    button.text('Completed'); // Update button text to 'Completed'
                    button.removeClass('btn-success').addClass('btn-secondary'); // Change button class for styling
                } else {
                    button.text('Complete'); // Update button text to 'Complete'
                    button.removeClass('btn-secondary').addClass('btn-success'); // Change button class for styling
                }
            } else {
                alert('Failed to update task'); // Show an error message if the task update failed
            }
        }
    });
}

// Function to edit a task's title
function editTask(id) {
    // Get the current title of the task
    let taskTitle = $('#task-' + id + ' .task-title').text();
    // Prompt the user to enter a new title
    let newTitle = prompt('Edit Task:', taskTitle);
    if (newTitle && newTitle.trim() !== '') {
        // Send an AJAX POST request to update_task.php
        $.ajax({
            url: 'update_task.php', // URL of the PHP file to handle the request
            method: 'POST', // HTTP method for the request
            data: { id: id, title: newTitle }, // Data to be sent to the server (task ID and new title)
            success: function(response) { // Callback function to handle success
                let res = JSON.parse(response); // Parse the JSON response
                if (res.status == 'success') {
                    $('#task-' + id + ' .task-title').text(newTitle); // Update the task title in the DOM
                } else {
                    alert('Failed to update task'); // Show an error message if the task update failed
                }
            }
        });
    }
}
