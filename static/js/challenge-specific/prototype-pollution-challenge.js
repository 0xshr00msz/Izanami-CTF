/**
 * Prototype Pollution Challenge - Bloodline Limit
 * This file contains the JavaScript for the Prototype Pollution challenge
 */

$(document).ready(function() {
    // Initialize the Prototype Pollution challenge
    if ($('#prototype-pollution-challenge').length) {
        initPrototypePollutionChallenge();
    }
});

function initPrototypePollutionChallenge() {
    // Deliberately vulnerable merge function
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
    
    // Global configuration object
    window.config = {
        theme: 'dark',
        username: 'guest',
        isAdmin: false,
        features: {
            advancedSearch: false,
            fileUpload: false,
            adminPanel: false
        }
    };
    
    // Function to check if user is admin
    function checkAdminAccess() {
        if (window.config.isAdmin === true) {
            $('#admin-panel').removeClass('d-none');
            showFlagMessage('Congratulations! You\'ve successfully exploited the prototype pollution vulnerability. Flag: izanami{pr0t0typ3_p0llut10n_m4st3r}');
        } else {
            $('#admin-panel').addClass('d-none');
        }
    }
    
    // Function to update the UI based on config
    function updateUI() {
        $('#config-display').html(
            `<pre class="bg-dark text-light p-3 rounded"><code>${JSON.stringify(window.config, null, 2)}</code></pre>`
        );
        
        // Check admin access
        checkAdminAccess();
    }
    
    // Set up the configuration form
    $('#config-form').on('submit', function(e) {
        e.preventDefault();
        
        try {
            const configInput = $('#config-input').val();
            const userConfig = JSON.parse(configInput);
            
            // Deliberately vulnerable merge
            mergeObjects(window.config, userConfig);
            
            showSuccessMessage('Configuration updated successfully!');
            updateUI();
        } catch (error) {
            showErrorMessage('Invalid JSON: ' + error.message);
        }
    });
    
    // Parse URL parameters (deliberately vulnerable)
    const urlParams = new URLSearchParams(window.location.search);
    const jsonData = urlParams.get('config');
    
    if (jsonData) {
        try {
            const data = JSON.parse(decodeURIComponent(jsonData));
            // Merge with config object (vulnerable to prototype pollution)
            mergeObjects(window.config, data);
            showSuccessMessage('Configuration loaded from URL parameters!');
        } catch (e) {
            console.error('Failed to parse JSON data:', e);
        }
    }
    
    // Add hint button functionality
    $('#prototype-hint-btn').on('click', function() {
        $('#prototype-hint-content').toggleClass('d-none');
    });
    
    // Add example button functionality
    $('#prototype-example-btn').on('click', function() {
        $('#config-input').val('{"__proto__": {"isAdmin": true}}');
    });
    
    // Initialize UI
    updateUI();
}

function showSuccessMessage(message) {
    $('#prototype-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showErrorMessage(message) {
    $('#prototype-message').html(
        `<div class="alert alert-danger alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}

function showFlagMessage(message) {
    $('#prototype-flag-message').html(
        `<div class="alert alert-success alert-dismissible fade show">
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert" aria-label="Close"></button>
        </div>`
    );
}
