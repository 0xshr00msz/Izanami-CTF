# Izanami: The Endless Loop

![Izanami CTF Logo](static/images/izanami-logo.png)

A web-based Capture The Flag (CTF) game inspired by Itachi's Sharingan Izanami from Naruto Shippuden. This game is designed as an Offensive Hacking CTF with a focus on Web vulnerabilities, featuring puzzle, strategy, logic, and abstract challenges.

## Table of Contents

- [Game Concept](#game-concept)
- [Features](#features)
- [Challenge Categories](#challenge-categories)
- [Game Mechanics](#game-mechanics)
- [Difficulty Levels](#difficulty-levels)
- [Tech Stack](#tech-stack)
- [Installation](#installation)
- [Project Structure](#project-structure)
- [Development](#development)
- [Challenge Creation](#challenge-creation)
- [API Documentation](#api-documentation)
- [WebSocket Integration](#websocket-integration)
- [Security Considerations](#security-considerations)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Game Concept

Similar to how Izanami traps opponents in a loop of reality they must acknowledge to escape, this CTF will trap players in a series of web-based challenges that require breaking out of predetermined patterns through offensive web hacking techniques.

In Naruto Shippuden, Izanami is a powerful genjutsu technique that traps the target in an infinite loop of events. The only way to break free is for the target to accept their true self and circumstances. Similarly, in this CTF game, players must identify vulnerabilities, understand the underlying patterns, and find their own unique solution paths to escape the loop.

Each challenge represents a "memory" the player is trapped in, and to escape the Izanami, players must "acknowledge their true selves" by finding their own unique solution path.

## Features

- **Progressive Difficulty System**: Players advance through ninja ranks (Academy, Chunin, Jōnin, Uchiha)
- **Chakra-Based Attempt System**: Limited attempts for challenges with regeneration over time
- **Sharingan Points**: Scoring system for tracking player progress
- **Genjutsu Counter**: Tracks failed attempts as "loops" in the Izanami
- **Hint System**: Unlockable hints that cost chakra points
- **Achievement System**: Rewards for completing specific challenges or milestones
- **Real-time Scoreboard**: Track your progress against other players
- **WebSocket Challenges**: Real-time interactive challenges
- **User Profiles**: Track your progress, achievements, and statistics

## Challenge Categories

The game includes a wide range of web security challenges:

1. **SQL Injection**: Exploit database queries to extract unauthorized data
2. **Cross-Site Scripting (XSS)**: Inject and execute malicious client-side scripts
3. **Cross-Site Request Forgery (CSRF)**: Trick users into performing unwanted actions
4. **Server-Side Request Forgery (SSRF)**: Make the server request internal resources
5. **Command Injection**: Execute unauthorized commands on the server
6. **Insecure Deserialization**: Exploit vulnerable deserialization processes
7. **File Upload Vulnerabilities**: Bypass file upload restrictions
8. **API Manipulation**: Exploit vulnerabilities in web APIs
9. **WebSocket Vulnerabilities**: Attack real-time communication channels
10. **Client-Side Storage Exploitation**: Manipulate browser storage mechanisms
11. **Race Conditions**: Exploit timing vulnerabilities
12. **GraphQL Vulnerabilities**: Attack GraphQL implementations
13. **Web Cache Poisoning**: Manipulate cached content
14. **HTTP Request Smuggling**: Exploit request handling inconsistencies
15. **Prototype Pollution**: Manipulate JavaScript object prototypes

## Game Mechanics

### Sharingan Points
Points earned by solving challenges. The more difficult the challenge, the more points you earn. These points determine your ranking on the scoreboard.

### Chakra Meter
Each player has a chakra meter that limits the number of attempts they can make on challenges. Different challenges require different amounts of chakra to attempt. Chakra regenerates over time (10 points per hour) and can also be earned by solving certain challenges.

### Scrolls
Hidden documentation and hints that can be found throughout the game. Some scrolls provide general knowledge, while others offer specific hints for challenges.

### Genjutsu Counter
Shows how many "loops" or failed attempts a player has made. This counter increases with each incorrect flag submission, representing the player being caught in the Izanami genjutsu.

### Hint System
Players can unlock hints for challenges by spending chakra points. Hints provide progressively more detailed information about how to solve a challenge.

## Difficulty Levels

1. **Academy**: Basic web vulnerabilities designed for beginners. These challenges introduce fundamental concepts and techniques.

2. **Chunin**: Intermediate challenges that require a deeper understanding of web security. Players must solve at least 70% of Academy challenges to unlock this level.

3. **Jōnin**: Advanced challenges that often require chaining multiple vulnerabilities together. Players must solve at least 70% of Chunin challenges to unlock this level.

4. **Uchiha**: Expert-level challenges that combine multiple attack vectors and require creative thinking. Players must solve at least 70% of Jōnin challenges to unlock this level.

## Tech Stack

### Backend
- Django Framework
- Django REST Framework
- Django Channels (WebSockets)
- Graphene Django (GraphQL)

### Frontend
- HTML/CSS
- JavaScript
- Bootstrap 5
- Font Awesome
- Chart.js

### Database
- SQLite (development)
- PostgreSQL (production)

## Installation

### Prerequisites
- Python 3.8+
- pip
- virtualenv

### Quick Start

1. Clone the repository:
   ```bash
   git clone https://github.com/0xshr00msz/izanami-ctf.git
   cd izanami-ctf
   ```

2. Create a virtual environment and install dependencies:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the setup script:
   ```bash
   ./run.sh
   ```

4. Access the application at http://localhost:8000/

### Default Login

- **Username**: admin
- **Password**: admin123

## Project Structure

```
izanami_ctf/
├── accounts/              # User authentication and profiles
├── challenges/            # Challenge models and views
│   ├── management/        # Management commands
│   ├── migrations/        # Database migrations
│   ├── templates/         # Challenge templates
│   │   └── challenge_templates/  # Specific challenge type templates
│   ├── templatetags/      # Custom template tags
│   ├── models.py          # Challenge data models
│   ├── urls.py            # URL routing
│   └── views.py           # View controllers
├── core/                  # Core application functionality
├── fixtures/              # Initial data fixtures
├── izanami/               # Project settings
├── media/                 # User-uploaded content
├── scoreboard/            # Scoreboard functionality
├── static/                # Static files
│   ├── css/               # Stylesheets
│   ├── images/            # Images
│   ├── js/                # JavaScript files
│   │   └── challenge-specific/  # Challenge-specific scripts
├── templates/             # Global templates
├── manage.py              # Django management script
├── requirements.txt       # Python dependencies
└── run.sh                 # Setup and run script
```

## Development

### Setting Up the Development Environment Manually

1. Apply migrations:
   ```bash
   python manage.py migrate
   ```

2. Load initial data:
   ```bash
   python manage.py loaddata fixtures/initial_data.json
   ```

3. Set up challenges:
   ```bash
   python manage.py setup_challenges
   ```

4. Create a superuser:
   ```bash
   python manage.py create_superuser
   ```

5. Run the development server:
   ```bash
   python manage.py runserver
   ```

### Database Models

#### Challenge Model
The main model for challenges with the following key fields:
- `title`: Challenge name
- `description`: Challenge description
- `category`: Category (SQL Injection, XSS, etc.)
- `difficulty`: Difficulty level (Academy, Chunin, etc.)
- `points`: Points awarded for solving
- `flag`: The correct flag string
- `chakra_cost`: Chakra points required to attempt
- Various boolean fields for challenge types (has_xss, has_sqli, etc.)

#### Other Key Models
- `DifficultyLevel`: Defines difficulty levels
- `ChallengeCategory`: Defines challenge categories
- `Hint`: Hints for challenges
- `ChallengeSolve`: Records when users solve challenges
- `ChallengeAttempt`: Records all attempts at challenges
- `PlayerProfile`: Extended user profile with game stats

### Custom Management Commands

- `setup_challenges`: Sets up challenge categories and difficulty levels
- `create_superuser`: Creates an admin user with default credentials

## Challenge Creation

To create a new challenge:

1. Add the challenge to the `fixtures/initial_data.json` file or create it through the admin interface
2. Create any necessary templates in `challenges/templates/challenge_templates/`
3. Add any challenge-specific JavaScript in `static/js/challenge-specific/`
4. If needed, create API endpoints in `challenges/views.py`

### Challenge Template Structure

Each challenge type has a specific template structure:

```html
{% extends 'base.html' %}

{% block title %}Challenge Title{% endblock %}

{% block content %}
<!-- Challenge-specific content -->

<!-- Flag submission form -->
<div class="flag-submission">
    <h5><i class="fas fa-flag text-danger"></i> Submit Flag</h5>
    {% if not solved %}
    <form id="flag-form" data-challenge-id="{{ challenge.id }}" data-solved="{{ solved|yesno:'true,false' }}">
        {% csrf_token %}
        <div class="input-group">
            <input type="text" id="flag-input" class="form-control" placeholder="Enter flag here...">
            <button class="btn btn-danger" type="submit">Submit</button>
        </div>
    </form>
    {% else %}
    <div class="alert alert-success">
        <i class="fas fa-check-circle me-2"></i> You have already solved this challenge!
    </div>
    {% endif %}
    <div id="flag-message" class="mt-3"></div>
</div>
{% endblock %}
```

## API Documentation

### Challenge API Endpoints

- `GET /challenges/`: List all challenges
- `GET /challenges/<id>/`: Get challenge details
- `POST /challenges/<id>/submit/`: Submit a flag
- `POST /challenges/<id>/hint/`: Unlock a hint

### User API Endpoints

- `POST /accounts/regenerate_chakra/`: Regenerate chakra points
- `GET /accounts/progress/`: Get user progress data

### Vulnerable API Endpoints (for challenges)

- `GET /challenges/api/user_data/`: SQL Injection vulnerable endpoint
- `GET /challenges/api/search/`: XSS vulnerable endpoint
- `POST /challenges/api/file_upload/`: File upload vulnerable endpoint
- `POST /challenges/api/fetch_url/`: SSRF vulnerable endpoint
- `POST /challenges/api/execute_command/`: Command injection vulnerable endpoint
- `POST /challenges/api/deserialize/`: Insecure deserialization vulnerable endpoint

## WebSocket Integration

The application uses Django Channels to provide WebSocket functionality for real-time challenges. WebSocket consumers are defined in `challenges/consumers.py`.

### WebSocket Challenge Example

```python
class ChallengeChatConsumer(AsyncWebsocketConsumer):
    async def connect(self):
        self.challenge_id = self.scope['url_route']['kwargs']['challenge_id']
        self.room_group_name = f'challenge_{self.challenge_id}'

        # Join room group
        await self.channel_layer.group_add(
            self.room_group_name,
            self.channel_name
        )

        await self.accept()

    async def disconnect(self, close_code):
        # Leave room group
        await self.channel_layer.group_discard(
            self.room_group_name,
            self.channel_name
        )

    # Receive message from WebSocket
    async def receive(self, text_data):
        text_data_json = json.loads(text_data)
        message_type = text_data_json.get('type', 'chat_message')
        
        # Handle different message types
        if message_type == 'chat_message':
            username = text_data_json.get('username', 'Anonymous')
            message = text_data_json.get('message', '')
            
            # Send message to room group
            await self.channel_layer.group_send(
                self.room_group_name,
                {
                    'type': 'chat_message',
                    'username': username,
                    'message': message
                }
            )
```

## Security Considerations

This application deliberately contains security vulnerabilities for educational purposes. These vulnerabilities are isolated to specific challenge endpoints and should not affect the core functionality of the application.

**Warning**: Do not deploy this application in a production environment without thoroughly reviewing and securing all endpoints.

### Deliberate Vulnerabilities

- SQL Injection in user data API
- XSS in search API and challenge descriptions
- CSRF in profile update forms
- Command Injection in network tools
- Insecure Deserialization in data processing
- File Upload vulnerabilities in file upload endpoints
- WebSocket vulnerabilities in chat features
- Prototype Pollution in JavaScript code

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Developed by [0xshr00msz](https://github.com/0xshr00msz)
- Created with assistance from Amazon Q
- Inspired by Naruto Shippuden and the concept of Izanami
- Built for educational purposes to teach web security concepts
