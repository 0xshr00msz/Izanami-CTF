/**
 * SQL Injection Challenge - Login Bypass
 * This file contains the JavaScript for the SQL Injection challenge
 */

$(document).ready(function() {
    // Initialize the SQL injection challenge
    if ($('#sqli-challenge').length) {
        initSQLiChallenge();
    }
});

function initSQLiChallenge() {
    // Set up the login form with vulnerable SQL query
    $('#sqli-login-form').on('submit', function(e) {
        e.preventDefault();
        
        const username = $('#username-input').val();
        const password = $('#password-input').val();
        
        // Deliberately vulnerable SQL query simulation
        $.ajax({
            url: '/challenges/api/login_check/',
            type: 'POST',
            data: {
                username: username,
                password: password,
                csrfmiddlewaretoken: getCsrfToken()
            },
            success: function(response) {
                if (response.success) {
                    showSuccessMessage('Login successful! Flag: ' + response.flag);
                    
                    // Show the SQL query that was executed (for educational purposes)
                    $('#sql-query-display').html(
                        `<div class="alert alert-info">
                            <strong>SQL Query:</strong>
                            <code>SELECT * FROM users WHERE username = '${escapeHtml(username)}' AND password = '${escapeHtml(password)}'</code>
                        </div>`
                    );
                } else {
                    showErrorMessage('Login failed. Try again!');
                    
                    // Show the SQL query that was executed (for educational purposes)
                    $('#sql-query-display').html(
                        `<div class="alert alert-secondary">
                            <strong>SQL Query:</strong>
                            <code>SELECT * FROM users WHERE username = '${escapeHtml(username)}' AND password = '${escapeHtml(password)}'</code>
                        </div>`
                    );
                }
            },
            error: function() {
                showErrorMessage('An error occurred. Please try again.');
            }
        });
    });
    
    // Add hint button functionality
    $('#sqli-hint-btn').on('click', function() {
        $('#sqli-hint-content').toggleClass('d-none');
    });
    
    // Add example button functionality
    $('#sqli-example-btn').on('click', function() {
        $('#username-input').val("admin' --");
        $('#password-input').val("anything");
    });
}

function showSuccessMessage(message) {
    $('#sqli-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showErrorMessage(message) {
    $('#sqli-message').html(
        `<div class="alert alert-danger alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
