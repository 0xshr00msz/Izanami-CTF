/**
 * WebSocket Challenge - Telepathic Communication
 * This file contains the JavaScript for the WebSocket challenge
 */

$(document).ready(function() {
    // Initialize the WebSocket challenge
    if ($('#websocket-challenge').length) {
        initWebSocketChallenge();
    }
});

function initWebSocketChallenge() {
    let socket = null;
    let currentUsername = 'Anonymous';
    
    // Connect to WebSocket
    function connectWebSocket() {
        const challengeId = $('#websocket-challenge').data('challenge-id');
        const protocol = window.location.protocol === 'https:' ? 'wss://' : 'ws://';
        const wsUrl = `${protocol}${window.location.host}/ws/challenges/${challengeId}/`;
        
        socket = new WebSocket(wsUrl);
        
        socket.onopen = function(e) {
            console.log('WebSocket connection established');
            $('#websocket-status').text('Connected').removeClass('text-danger').addClass('text-success');
            
            // Send initial connection message
            sendSystemMessage(`${currentUsername} has joined the chat`);
        };
        
        socket.onmessage = function(e) {
            const data = JSON.parse(e.data);
            handleWebSocketMessage(data);
        };
        
        socket.onclose = function(e) {
            console.log('WebSocket connection closed');
            $('#websocket-status').text('Disconnected').removeClass('text-success').addClass('text-danger');
            
            // Try to reconnect after 5 seconds
            setTimeout(function() {
                connectWebSocket();
            }, 5000);
        };
        
        socket.onerror = function(e) {
            console.error('WebSocket error:', e);
            $('#websocket-status').text('Error').removeClass('text-success').addClass('text-danger');
        };
    }
    
    // Handle incoming WebSocket messages
    function handleWebSocketMessage(data) {
        if (data.type === 'chat_message') {
            // Deliberately vulnerable - inserting HTML without sanitization
            $('#websocket-messages').append(`
                <div class="message">
                    <strong>${data.username}:</strong> ${data.message}
                </div>
            `);
            
            // Auto-scroll to bottom
            const messagesContainer = document.getElementById('websocket-messages');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
            
            // Check for flag reveal message
            if (data.message.includes('ADMIN_COMMAND:REVEAL_FLAG') && data.username === 'Admin') {
                showFlagMessage('Congratulations! You\'ve successfully exploited the WebSocket vulnerability. Flag: izanami{w3bs0ck3t_vuln3r4b1l1ty}');
            }
        } else if (data.type === 'system_message') {
            $('#websocket-messages').append(`
                <div class="message text-muted">
                    <em>${data.message}</em>
                </div>
            `);
            
            // Auto-scroll to bottom
            const messagesContainer = document.getElementById('websocket-messages');
            messagesContainer.scrollTop = messagesContainer.scrollHeight;
        } else if (data.type === 'challenge_data') {
            console.log('Received challenge data:', data);
        } else if (data.type === 'flag_result') {
            if (data.is_correct) {
                showSuccessMessage(data.message);
            } else {
                showErrorMessage(data.message);
            }
        }
    }
    
    // Send a message through WebSocket
    function sendChatMessage(message, username) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            // Deliberately vulnerable - trusting client-side data
            socket.send(JSON.stringify({
                'type': 'chat_message',
                'message': message,
                'username': username
            }));
        }
    }
    
    // Send a system message
    function sendSystemMessage(message) {
        if (socket && socket.readyState === WebSocket.OPEN) {
            socket.send(JSON.stringify({
                'type': 'system_message',
                'message': message
            }));
        }
    }
    
    // Set up the chat form
    $('#websocket-form').on('submit', function(e) {
        e.preventDefault();
        
        const message = $('#websocket-input').val();
        const username = $('#websocket-username').val() || 'Anonymous';
        
        if (message.trim() === '') return;
        
        // Update current username
        currentUsername = username;
        
        // Send the message
        sendChatMessage(message, username);
        
        // Clear input
        $('#websocket-input').val('');
    });
    
    // Add hint button functionality
    $('#websocket-hint-btn').on('click', function() {
        $('#websocket-hint-content').toggleClass('d-none');
    });
    
    // Add example button functionality
    $('#websocket-example-btn').on('click', function() {
        $('#websocket-username').val('Admin');
        $('#websocket-input').val('ADMIN_COMMAND:REVEAL_FLAG');
    });
    
    // Initialize WebSocket connection
    connectWebSocket();
}

function showSuccessMessage(message) {
    $('#websocket-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showErrorMessage(message) {
    $('#websocket-message').html(
        `<div class="alert alert-danger alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showFlagMessage(message) {
    $('#websocket-flag-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}
