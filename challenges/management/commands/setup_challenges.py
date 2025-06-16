"""
Management command to set up challenge categories and difficulty levels.
"""

from django.core.management.base import BaseCommand
from challenges.models import DifficultyLevel, ChallengeCategory, Challenge, Hint
from accounts.models import Achievement

class Command(BaseCommand):
    help = 'Sets up challenge categories and difficulty levels'

    def handle(self, *args, **options):
        self.stdout.write('Setting up difficulty levels...')
        self._setup_difficulty_levels()
        
        self.stdout.write('Setting up challenge categories...')
        self._setup_challenge_categories()
        
        self.stdout.write('Setting up achievements...')
        self._setup_achievements()
        
        self.stdout.write(self.style.SUCCESS('Successfully set up challenges data'))
    
    def _setup_difficulty_levels(self):
        """Set up difficulty levels."""
        difficulty_levels = [
            {
                'name': 'Academy',
                'description': 'Beginner-level challenges designed to introduce you to basic web vulnerabilities.',
                'order': 1
            },
            {
                'name': 'Chunin',
                'description': 'Intermediate challenges that require a deeper understanding of web security concepts.',
                'order': 2
            },
            {
                'name': 'Jōnin',
                'description': 'Advanced challenges that often require chaining multiple vulnerabilities together.',
                'order': 3
            },
            {
                'name': 'Uchiha',
                'description': 'Expert-level challenges that require mastery of multiple attack vectors and creative thinking.',
                'order': 4
            }
        ]
        
        for level_data in difficulty_levels:
            level, created = DifficultyLevel.objects.get_or_create(
                name=level_data['name'],
                defaults={
                    'description': level_data['description'],
                    'order': level_data['order']
                }
            )
            
            if created:
                self.stdout.write(f'Created difficulty level: {level.name}')
            else:
                self.stdout.write(f'Difficulty level already exists: {level.name}')
    
    def _setup_challenge_categories(self):
        """Set up challenge categories."""
        categories = [
            {
                'name': 'SQL Injection',
                'description': 'Challenges focused on exploiting SQL injection vulnerabilities to extract data or bypass authentication.',
                'icon': 'fa-database'
            },
            {
                'name': 'XSS',
                'description': 'Cross-Site Scripting challenges that test your ability to inject and execute malicious JavaScript.',
                'icon': 'fa-code'
            },
            {
                'name': 'CSRF',
                'description': 'Cross-Site Request Forgery challenges that involve tricking users into performing unwanted actions.',
                'icon': 'fa-random'
            },
            {
                'name': 'File Upload',
                'description': 'Challenges that involve exploiting file upload vulnerabilities to achieve code execution.',
                'icon': 'fa-file-upload'
            },
            {
                'name': 'SSRF',
                'description': 'Server-Side Request Forgery challenges that involve making the server request internal resources.',
                'icon': 'fa-server'
            },
            {
                'name': 'Command Injection',
                'description': 'Challenges that involve injecting OS commands into vulnerable applications.',
                'icon': 'fa-terminal'
            },
            {
                'name': 'Deserialization',
                'description': 'Challenges focused on exploiting insecure deserialization to achieve code execution.',
                'icon': 'fa-box-open'
            },
            {
                'name': 'WebSocket',
                'description': 'Challenges that involve exploiting vulnerabilities in WebSocket connections.',
                'icon': 'fa-plug'
            },
            {
                'name': 'API',
                'description': 'Challenges focused on finding and exploiting vulnerabilities in web APIs.',
                'icon': 'fa-project-diagram'
            },
            {
                'name': 'GraphQL',
                'description': 'Challenges that involve exploiting vulnerabilities in GraphQL implementations.',
                'icon': 'fa-sitemap'
            },
            {
                'name': 'Race Condition',
                'description': 'Challenges that involve exploiting timing vulnerabilities in web applications.',
                'icon': 'fa-clock'
            },
            {
                'name': 'Prototype Pollution',
                'description': 'Challenges focused on exploiting JavaScript prototype pollution vulnerabilities.',
                'icon': 'fa-code-branch'
            }
        ]
        
        for category_data in categories:
            category, created = ChallengeCategory.objects.get_or_create(
                name=category_data['name'],
                defaults={
                    'description': category_data['description'],
                    'icon': category_data['icon']
                }
            )
            
            if created:
                self.stdout.write(f'Created category: {category.name}')
            else:
                self.stdout.write(f'Category already exists: {category.name}')
    
    def _setup_achievements(self):
        """Set up achievements."""
        achievements = [
            {
                'name': 'Academy Graduate',
                'description': 'Complete all Academy level challenges',
                'icon': 'fa-graduation-cap'
            },
            {
                'name': 'Chunin Exam Survivor',
                'description': 'Complete all Chunin level challenges',
                'icon': 'fa-user-ninja'
            },
            {
                'name': 'Jōnin Elite',
                'description': 'Complete all Jōnin level challenges',
                'icon': 'fa-user-shield'
            },
            {
                'name': 'Uchiha Prodigy',
                'description': 'Complete all Uchiha level challenges',
                'icon': 'fa-eye'
            },
            {
                'name': 'SQL Master',
                'description': 'Complete all SQL Injection challenges',
                'icon': 'fa-database'
            },
            {
                'name': 'Script Kiddie',
                'description': 'Complete all XSS challenges',
                'icon': 'fa-code'
            },
            {
                'name': 'First Blood',
                'description': 'Be the first to solve any challenge',
                'icon': 'fa-tint'
            },
            {
                'name': 'Perfect Loop',
                'description': 'Solve a challenge without using any hints',
                'icon': 'fa-sync-alt'
            }
        ]
        
        for achievement_data in achievements:
            achievement, created = Achievement.objects.get_or_create(
                name=achievement_data['name'],
                defaults={
                    'description': achievement_data['description'],
                    'icon': achievement_data['icon']
                }
            )
            
            if created:
                self.stdout.write(f'Created achievement: {achievement.name}')
            else:
                self.stdout.write(f'Achievement already exists: {achievement.name}')
