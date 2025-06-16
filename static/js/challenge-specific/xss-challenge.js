/**
 * XSS Challenge - Greeting Card
 * This file contains the JavaScript for the XSS challenge
 */

$(document).ready(function() {
    // Initialize the XSS challenge
    if ($('#xss-challenge').length) {
        initXSSChallenge();
    }
});

function initXSSChallenge() {
    // Get the name parameter from the URL
    const urlParams = new URLSearchParams(window.location.search);
    const name = urlParams.get('name');
    
    // Deliberately vulnerable code - directly inserting user input into the DOM
    if (name) {
        // Vulnerable code - directly inserting user input without sanitization
        $('#greeting-message').html('Hello, ' + name + '!');
        
        // Show the input that was used (for educational purposes)
        $('#xss-input-display').html(
            `<div class="alert alert-secondary">
                <strong>Input Used:</strong>
                <code>${escapeHtml(name)}</code>
            </div>`
        );
    } else {
        $('#greeting-message').text('Hello, Ninja!');
    }
    
    // Set up the greeting form
    $('#xss-greeting-form').on('submit', function(e) {
        e.preventDefault();
        
        const nameInput = $('#name-input').val();
        
        // Redirect to the same page with the name parameter
        window.location.href = window.location.pathname + '?name=' + encodeURIComponent(nameInput);
    });
    
    // Add hint button functionality
    $('#xss-hint-btn').on('click', function() {
        $('#xss-hint-content').toggleClass('d-none');
    });
    
    // Add example button functionality
    $('#xss-example-btn').on('click', function() {
        $('#name-input').val("<script>alert('XSS')</script>");
    });
    
    // Secret function that reveals the flag when called
    window.revealFlag = function() {
        $('#xss-message').html(
            `<div class="alert alert-success alert-dismissible fade show">
                Congratulations! You've successfully executed JavaScript. Flag: izanami{cr0ss_s1t3_scr1pt1ng_101}
                <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
            </div>`
        );
    };
    
    // Cookie with fake sensitive data (for the challenge)
    document.cookie = "fake_sensitive_data=this_is_not_the_real_flag; path=/";
}

function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
