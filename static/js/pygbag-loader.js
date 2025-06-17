/**
 * Pygbag loader for Pygame challenges
 * This script loads a Pygame game using Pygbag (WebAssembly)
 */

// Global variables
let pygbagScript = null;
let pygbagWorker = null;
let canvas = null;
let ctx = null;
let gameRunning = false;

/**
 * Load a Pygame game using Pygbag
 * @param {string} pythonScriptPath - Path to the Python script
 */
function loadPygame(pythonScriptPath) {
    // Get the canvas element
    canvas = document.getElementById('canvas');
    ctx = canvas.getContext('2d');
    
    // Set canvas dimensions
    resizeCanvas();
    window.addEventListener('resize', resizeCanvas);
    
    // Show loading message
    drawLoadingMessage('Loading Pygame...');
    
    // Load Pygbag script
    loadPygbagScript()
        .then(() => {
            // Initialize Pygbag with the Python script
            initPygbag(pythonScriptPath);
        })
        .catch(error => {
            console.error('Error loading Pygbag:', error);
            drawErrorMessage('Failed to load Pygame. Please try again.');
        });
}

/**
 * Load the Pygbag script
 * @returns {Promise} - Promise that resolves when the script is loaded
 */
function loadPygbagScript() {
    return new Promise((resolve, reject) => {
        // Check if Pygbag script is already loaded
        if (window.pygbag) {
            resolve();
            return;
        }
        
        // Create script element
        pygbagScript = document.createElement('script');
        pygbagScript.src = '/static/js/pygbag.js';
        pygbagScript.async = true;
        
        // Set up event handlers
        pygbagScript.onload = () => {
            console.log('Pygbag script loaded');
            resolve();
        };
        
        pygbagScript.onerror = () => {
            reject(new Error('Failed to load Pygbag script'));
        };
        
        // Add script to document
        document.head.appendChild(pygbagScript);
    });
}

/**
 * Initialize Pygbag with the Python script
 * @param {string} pythonScriptPath - Path to the Python script
 */
function initPygbag(pythonScriptPath) {
    try {
        // Create a new Pygbag instance
        pygbagWorker = new window.pygbag.PygbagWorker({
            canvas: canvas,
            pythonScript: pythonScriptPath,
            onStdout: handleStdout,
            onStderr: handleStderr,
            onGameReady: handleGameReady,
            onGameExit: handleGameExit,
            onError: handleError
        });
        
        // Start the game
        pygbagWorker.start();
    } catch (error) {
        console.error('Error initializing Pygbag:', error);
        drawErrorMessage('Failed to initialize Pygame. Please try again.');
    }
}

/**
 * Handle stdout messages from the Pygame game
 * @param {string} message - The stdout message
 */
function handleStdout(message) {
    console.log('Pygame stdout:', message);
    
    // Check if the message contains a flag
    if (message.includes('FLAG:')) {
        const flag = message.split('FLAG:')[1].trim();
        sendFlagToParent(flag);
    }
}

/**
 * Handle stderr messages from the Pygame game
 * @param {string} message - The stderr message
 */
function handleStderr(message) {
    console.error('Pygame stderr:', message);
}

/**
 * Handle game ready event
 */
function handleGameReady() {
    console.log('Pygame game is ready');
    gameRunning = true;
}

/**
 * Handle game exit event
 * @param {number} exitCode - The exit code
 */
function handleGameExit(exitCode) {
    console.log('Pygame game exited with code:', exitCode);
    gameRunning = false;
    
    // Show exit message
    drawExitMessage(`Game exited with code: ${exitCode}`);
}

/**
 * Handle error event
 * @param {Error} error - The error object
 */
function handleError(error) {
    console.error('Pygame error:', error);
    gameRunning = false;
    
    // Show error message
    drawErrorMessage('An error occurred in the game. Please try again.');
}

/**
 * Send a flag to the parent window
 * @param {string} flag - The flag to send
 */
function sendFlagToParent(flag) {
    if (window.parent && window.parent !== window) {
        window.parent.postMessage({ type: 'flag', flag: flag }, '*');
    }
}

/**
 * Resize the canvas to fit the window
 */
function resizeCanvas() {
    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;
    
    // Redraw loading message if game is not running
    if (!gameRunning) {
        drawLoadingMessage('Loading Pygame...');
    }
}

/**
 * Draw a loading message on the canvas
 * @param {string} message - The message to display
 */
function drawLoadingMessage(message) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ff0000';
    ctx.font = '24px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
    
    // Draw a loading spinner
    drawLoadingSpinner();
}

/**
 * Draw an error message on the canvas
 * @param {string} message - The error message to display
 */
function drawErrorMessage(message) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ff0000';
    ctx.font = '24px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
    
    // Draw a retry button
    drawRetryButton();
}

/**
 * Draw an exit message on the canvas
 * @param {string} message - The exit message to display
 */
function drawExitMessage(message) {
    ctx.fillStyle = '#000000';
    ctx.fillRect(0, 0, canvas.width, canvas.height);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = '24px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText(message, canvas.width / 2, canvas.height / 2);
    
    // Draw a restart button
    drawRestartButton();
}

/**
 * Draw a loading spinner on the canvas
 */
function drawLoadingSpinner() {
    const centerX = canvas.width / 2;
    const centerY = canvas.height / 2 + 50;
    const radius = 20;
    const startAngle = 0;
    const endAngle = Math.PI * 2;
    
    // Draw spinner background
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, startAngle, endAngle);
    ctx.strokeStyle = '#333333';
    ctx.lineWidth = 5;
    ctx.stroke();
    
    // Draw spinner foreground
    const now = new Date().getTime() / 1000;
    const spinnerAngle = (now % 2) * Math.PI;
    
    ctx.beginPath();
    ctx.arc(centerX, centerY, radius, spinnerAngle, spinnerAngle + Math.PI);
    ctx.strokeStyle = '#ff0000';
    ctx.lineWidth = 5;
    ctx.stroke();
    
    // Continue animation
    if (!gameRunning) {
        requestAnimationFrame(() => drawLoadingSpinner());
    }
}

/**
 * Draw a retry button on the canvas
 */
function drawRetryButton() {
    const buttonX = canvas.width / 2;
    const buttonY = canvas.height / 2 + 50;
    const buttonWidth = 100;
    const buttonHeight = 40;
    
    ctx.fillStyle = '#ff0000';
    ctx.fillRect(buttonX - buttonWidth / 2, buttonY - buttonHeight / 2, buttonWidth, buttonHeight);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = '16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Retry', buttonX, buttonY);
    
    // Add click event listener
    canvas.addEventListener('click', handleRetryClick);
}

/**
 * Draw a restart button on the canvas
 */
function drawRestartButton() {
    const buttonX = canvas.width / 2;
    const buttonY = canvas.height / 2 + 50;
    const buttonWidth = 100;
    const buttonHeight = 40;
    
    ctx.fillStyle = '#008000';
    ctx.fillRect(buttonX - buttonWidth / 2, buttonY - buttonHeight / 2, buttonWidth, buttonHeight);
    
    ctx.fillStyle = '#ffffff';
    ctx.font = '16px Arial';
    ctx.textAlign = 'center';
    ctx.textBaseline = 'middle';
    ctx.fillText('Restart', buttonX, buttonY);
    
    // Add click event listener
    canvas.addEventListener('click', handleRestartClick);
}

/**
 * Handle retry button click
 * @param {MouseEvent} event - The click event
 */
function handleRetryClick(event) {
    const buttonX = canvas.width / 2;
    const buttonY = canvas.height / 2 + 50;
    const buttonWidth = 100;
    const buttonHeight = 40;
    
    const x = event.clientX;
    const y = event.clientY;
    
    if (x >= buttonX - buttonWidth / 2 && x <= buttonX + buttonWidth / 2 &&
        y >= buttonY - buttonHeight / 2 && y <= buttonY + buttonHeight / 2) {
        // Remove click event listener
        canvas.removeEventListener('click', handleRetryClick);
        
        // Reload the page
        window.location.reload();
    }
}

/**
 * Handle restart button click
 * @param {MouseEvent} event - The click event
 */
function handleRestartClick(event) {
    const buttonX = canvas.width / 2;
    const buttonY = canvas.height / 2 + 50;
    const buttonWidth = 100;
    const buttonHeight = 40;
    
    const x = event.clientX;
    const y = event.clientY;
    
    if (x >= buttonX - buttonWidth / 2 && x <= buttonX + buttonWidth / 2 &&
        y >= buttonY - buttonHeight / 2 && y <= buttonY + buttonHeight / 2) {
        // Remove click event listener
        canvas.removeEventListener('click', handleRestartClick);
        
        // Reload the page
        window.location.reload();
    }
}
