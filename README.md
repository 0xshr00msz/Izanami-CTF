# Izanami: The Endless Loop

A web-based CTF game inspired by Itachi's Sharingan Izanami from Naruto Shippuden. This game is designed as an Offensive Hacking CTF with a focus on Web vulnerabilities, featuring puzzle, strategy, logic, and abstract challenges.

## Game Concept

Similar to how Izanami traps opponents in a loop of reality they must acknowledge to escape, this CTF will trap players in a series of web-based challenges that require breaking out of predetermined patterns through offensive web hacking techniques.

## Tech Stack

- **Backend**: Django
- **Frontend**: HTML/CSS + JavaScript with Bootstrap
- **Database**: SQLite (development), PostgreSQL (production)

## Challenge Categories

The game includes a wide range of web security challenges:

1. SQL Injection
2. Cross-Site Scripting (XSS)
3. Cross-Site Request Forgery (CSRF)
4. Server-Side Request Forgery (SSRF)
5. Command Injection
6. Insecure Deserialization
7. File Upload Vulnerabilities
8. API Manipulation
9. WebSocket Vulnerabilities
10. Client-Side Storage Exploitation
11. Race Conditions
12. GraphQL Vulnerabilities
13. Web Cache Poisoning
14. HTTP Request Smuggling
15. Prototype Pollution

## Game Mechanics

- **Sharingan Points**: Earned by solving challenges
- **Chakra Meter**: Limited attempts for certain challenges
- **Scrolls**: Hidden documentation/hints found throughout the game
- **Genjutsu Counter**: Shows how many "loops" the player has been through

## Difficulty Levels

1. **Academy**: Basic web vulnerabilities
2. **Chunin**: More complex exploits
3. **Jōnin**: Chained vulnerabilities
4. **Uchiha**: Advanced techniques combining multiple attack vectors

## Quick Start

1. Clone the repository:
   ```
   git clone https://github.com/0xshr00msz/izanami-ctf.git
   cd izanami-ctf
   ```

2. Create a virtual environment and install dependencies:
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   pip install -r requirements.txt
   ```

3. Run the setup script:
   ```
   ./run.sh
   ```

4. Access the application at http://localhost:8000/

## Default Login

- **Username**: admin
- **Password**: admin123

## Development

To set up the development environment manually:

1. Apply migrations:
   ```
   python manage.py migrate
   ```

2. Load initial data:
   ```
   python manage.py loaddata fixtures/initial_data.json
   ```

3. Set up challenges:
   ```
   python manage.py setup_challenges
   ```

4. Create a superuser:
   ```
   python manage.py create_superuser
   ```

5. Run the development server:
   ```
   python manage.py runserver
   ```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Acknowledgements

- Developed by 0xshr00msz
- Inspired by Naruto Shippuden and the concept of Izanami
- Built for educational purposes to teach web security concepts
