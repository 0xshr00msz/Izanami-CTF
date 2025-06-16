/**
 * Izanami: The Endless Loop - Game Engine
 * Main JavaScript file for game functionality
 */

// Global variables
let chakraRegenInterval;
let genjutsuCounter = 0;

// Initialize game when document is ready
$(document).ready(function() {
    console.log("Izanami game engine initialized");
    
    // Start chakra regeneration
    startChakraRegeneration();
    
    // Setup challenge submission handlers
    setupChallengeHandlers();
    
    // Setup WebSocket connections for relevant challenges
    setupWebSockets();
    
    // Initialize vulnerable client-side features
    initVulnerableFeatures();
});

/**
 * Start chakra regeneration process
 */
function startChakraRegeneration() {
    // Regenerate chakra every 60 seconds
    chakraRegenInterval = setInterval(function() {
        $.ajax({
            url: '/accounts/regenerate_chakra/',
            type: 'POST',
            data: {
                'csrfmiddlewaretoken': getCsrfToken()
            },
            success: function(data) {
                updateChakraMeter(data.chakra);
            }
        });
    }, 60000);
}

/**
 * Update chakra meter display
 */
function updateChakraMeter(chakraValue) {
    const chakraMeter = $('.progress-bar');
    chakraMeter.css('width', chakraValue + '%');
    chakraMeter.attr('aria-valuenow', chakraValue);
    chakraMeter.text(chakraValue + '%');
}

/**
 * Setup challenge submission handlers
 */
function setupChallengeHandlers() {
    // Flag submission
    $('#flag-form').on('submit', function(e) {
        e.preventDefault();
        
        const challengeId = $(this).data('challenge-id');
        const flagInput = $('#flag-input').val();
        
        $.ajax({
            url: `/challenges/${challengeId}/submit/`,
            type: 'POST',
            data: {
                'flag': flagInput,
                'csrfmiddlewaretoken': getCsrfToken()
            },
            success: function(data) {
                if (data.success) {
                    showAlert('success', data.message);
                    incrementSharinganPoints(data.points);
                    
                    // Mark challenge as solved
                    $(`#challenge-${challengeId}`).removeClass('challenge-unsolved').addClass('challenge-solved');
                } else {
                    showAlert('danger', data.message);
                    incrementGenjutsuCounter();
                }
            },
            error: function() {
                showAlert('danger', 'An error occurred while submitting your flag.');
            }
        });
    });
    
    // Hint unlocking
    $('.hint-button').on('click', function() {
        const hintId = $(this).data('hint-id');
        const challengeId = $(this).data('challenge-id');
        
        $.ajax({
            url: `/challenges/${challengeId}/hint/`,
            type: 'POST',
            data: {
                'hint_id': hintId,
                'csrfmiddlewaretoken': getCsrfToken()
            },
            success: function(data) {
                if (data.success) {
                    showAlert('info', data.message);
                    $(`#hint-content-${hintId}`).html(data.hint).removeClass('d-none');
                    updateChakraMeter(data.chakra);
                } else {
                    showAlert('danger', data.message);
                }
            },
            error: function() {
                showAlert('danger', 'An error occurred while unlocking the hint.');
            }
        });
    });
}

/**
 * Setup WebSocket connections for challenges
 */
function setupWebSockets() {
    // Check if we're on a challenge page that needs WebSockets
    const challengeId = $('#challenge-detail').data('challenge-id');
    if (!challengeId) return;
    
    // Check if this challenge has WebSocket functionality
    const hasWebsocket = $('#challenge-detail').data('has-websocket');
    if (!hasWebsocket) return;
    
    // Create WebSocket connection
    const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
    const wsUrl = `${protocol}${window.location.host}/ws/challenges/${challengeId}/`;
    const socket = new WebSocket(wsUrl);
    
    socket.onopen = function(e) {
        console.log('WebSocket connection established');
        $('#websocket-status').text('Connected').removeClass('text-danger').addClass('text-success');
    };
    
    socket.onmessage = function(e) {
        const data = JSON.parse(e.data);
        handleWebSocketMessage(data);
    };
    
    socket.onclose = function(e) {
        console.log('WebSocket connection closed');
        $('#websocket-status').text('Disconnected').removeClass('text-success').addClass('text-danger');
    };
    
    // Send message through WebSocket
    $('#websocket-form').on('submit', function(e) {
        e.preventDefault();
        
        const message = $('#websocket-input').val();
        const username = $('#websocket-username').val() || 'Anonymous';
        
        // Deliberately vulnerable - sending user input without validation
        socket.send(JSON.stringify({
            'type': 'chat_message',
            'message': message,
            'username': username
        }));
        
        $('#websocket-input').val('');
    });
}

/**
 * Handle incoming WebSocket messages
 */
function handleWebSocketMessage(data) {
    if (data.type === 'chat_message') {
        // Deliberately vulnerable - inserting HTML without sanitization
        $('#websocket-messages').append(`
            <div class="message">
                <strong>${data.username}:</strong> ${data.message}
            </div>
        `);
    } else if (data.type === 'challenge_data') {
        console.log('Received challenge data:', data);
    } else if (data.type === 'flag_result') {
        if (data.is_correct) {
            showAlert('success', data.message);
        } else {
            showAlert('danger', data.message);
        }
    }
}

/**
 * Initialize vulnerable client-side features
 */
function initVulnerableFeatures() {
    // Prototype pollution vulnerability
    // This function is deliberately vulnerable to prototype pollution
    function mergeObjects(target, source) {
        for (let key in source) {
            if (source.hasOwnProperty(key)) {
                if (typeof source[key] === 'object' && source[key] !== null) {
                    if (typeof target[key] !== 'object') {
                        target[key] = {};
                    }
                    mergeObjects(target[key], source[key]);
                } else {
                    target[key] = source[key];
                }
            }
        }
        return target;
    }
    
    // Expose the vulnerable function globally
    window.mergeObjects = mergeObjects;
    
    // Parse URL parameters (deliberately vulnerable)
    const urlParams = new URLSearchParams(window.location.search);
    const jsonData = urlParams.get('data');
    
    if (jsonData) {
        try {
            const data = JSON.parse(jsonData);
            // Merge with an empty object (vulnerable to prototype pollution)
            const config = {};
            mergeObjects(config, data);
            
            console.log('Loaded configuration:', config);
        } catch (e) {
            console.error('Failed to parse JSON data:', e);
        }
    }
}

/**
 * Show an alert message
 */
function showAlert(type, message) {
    const alertHtml = `
        <div class="alert alert-${type} alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>
    `;
    
    $('.messages').append(alertHtml);
    
    // Auto-dismiss after 5 seconds
    setTimeout(function() {
        $('.alert').alert('close');
    }, 5000);
}

/**
 * Increment Sharingan points
 */
function incrementSharinganPoints(points) {
    const pointsElement = $('.sharingan-points');
    const currentPoints = parseInt(pointsElement.text());
    const newPoints = currentPoints + points;
    pointsElement.text(newPoints);
}

/**
 * Increment Genjutsu counter
 */
function incrementGenjutsuCounter() {
    genjutsuCounter++;
    $('.genjutsu-counter').text(genjutsuCounter);
}

/**
 * Get CSRF token from cookies
 */
function getCsrfToken() {
    return document.querySelector('[name=csrfmiddlewaretoken]').value;
}
