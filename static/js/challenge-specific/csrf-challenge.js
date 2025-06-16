/**
 * CSRF Challenge - Profile Update
 * This file contains the JavaScript for the CSRF challenge
 */

$(document).ready(function() {
    // Initialize the CSRF challenge
    if ($('#csrf-challenge').length) {
        initCSRFChallenge();
    }
});

function initCSRFChallenge() {
    // Set up the profile update form (deliberately vulnerable - no CSRF token)
    $('#csrf-profile-form').on('submit', function(e) {
        e.preventDefault();
        
        const username = $('#username-input').val();
        const email = $('#email-input').val();
        const bio = $('#bio-input').val();
        
        // Deliberately vulnerable AJAX request - no CSRF token validation
        $.ajax({
            url: '/challenges/api/update_profile/',
            type: 'POST',
            data: {
                username: username,
                email: email,
                bio: bio
            },
            success: function(response) {
                if (response.success) {
                    showSuccessMessage('Profile updated successfully!');
                    
                    // Check if this was the CSRF attack
                    if (response.csrf_detected) {
                        showFlagMessage('Congratulations! You\'ve successfully exploited the CSRF vulnerability. Flag: ' + response.flag);
                    }
                } else {
                    showErrorMessage('Failed to update profile. Try again!');
                }
            },
            error: function() {
                showErrorMessage('An error occurred. Please try again.');
            }
        });
    });
    
    // Add hint button functionality
    $('#csrf-hint-btn').on('click', function() {
        $('#csrf-hint-content').toggleClass('d-none');
    });
    
    // Add example button functionality
    $('#csrf-example-btn').on('click', function() {
        $('#csrf-example-content').toggleClass('d-none');
    });
    
    // Load current profile data
    loadProfileData();
}

function loadProfileData() {
    // Load the current profile data
    $.ajax({
        url: '/challenges/api/get_profile/',
        type: 'GET',
        success: function(response) {
            if (response.success) {
                $('#username-input').val(response.username);
                $('#email-input').val(response.email);
                $('#bio-input').val(response.bio);
            }
        }
    });
}

function showSuccessMessage(message) {
    $('#csrf-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showErrorMessage(message) {
    $('#csrf-message').html(
        `<div class="alert alert-danger alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showFlagMessage(message) {
    $('#csrf-flag-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}
