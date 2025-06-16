/**
 * Flag submission handler for all challenge types
 */

$(document).ready(function() {
    // Flag submission handler
    $('#flag-form').on('submit', function(e) {
        e.preventDefault();
        
        const challengeId = $(this).data('challenge-id');
        const flagInput = $('#flag-input').val();
        
        // Check if the challenge is already solved
        const isSolved = $(this).data('solved');
        if (isSolved === true) {
            $('#flag-message').html(
                `<div class="alert alert-warning alert-dismissible fade show">
                    You have already solved this challenge!
                    <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                </div>`
            );
            return;
        }
        
        $.ajax({
            url: `/challenges/${challengeId}/submit/`,
            type: 'POST',
            data: {
                'flag': flagInput,
                'csrfmiddlewaretoken': $('input[name=csrfmiddlewaretoken]').val()
            },
            success: function(data) {
                if (data.success) {
                    $('#flag-message').html(
                        `<div class="alert alert-success alert-dismissible fade show">
                            ${data.message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`
                    );
                    
                    // Mark the challenge as solved
                    $('#flag-form').data('solved', true);
                    
                    // Add solved badge to the challenge header
                    if ($('.challenge-header .badge.bg-success').length === 0) {
                        $('.challenge-header .category-badge').after(
                            '<span class="badge bg-success ms-2">Solved</span>'
                        );
                    }
                    
                    // Disable the form
                    setTimeout(function() {
                        $('#flag-input').attr('disabled', true);
                        $('#flag-form button[type="submit"]').attr('disabled', true);
                        $('#flag-form button[type="submit"]').text('Challenge Solved');
                    }, 2000);
                } else {
                    $('#flag-message').html(
                        `<div class="alert alert-danger alert-dismissible fade show">
                            ${data.message}
                            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                        </div>`
                    );
                }
            },
            error: function() {
                $('#flag-message').html(
                    `<div class="alert alert-danger alert-dismissible fade show">
                        An error occurred while submitting your flag.
                        <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
                    </div>`
                );
            }
        });
    });
});
