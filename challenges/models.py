"""
Models for the challenges app.
"""

from django.db import models
from django.contrib.auth.models import User

class ChallengeCategory(models.Model):
    """Challenge categories."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # CSS class for the icon
    
    class Meta:
        verbose_name_plural = "Challenge Categories"
    
    def __str__(self):
        return self.name

class DifficultyLevel(models.Model):
    """Difficulty levels for challenges."""
    name = models.CharField(max_length=50)
    description = models.TextField()
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order']
    
    def __str__(self):
        return self.name

class Challenge(models.Model):
    """Challenge model."""
    title = models.CharField(max_length=200)
    description = models.TextField()
    category = models.ForeignKey(ChallengeCategory, on_delete=models.CASCADE, related_name='challenges')
    difficulty = models.ForeignKey(DifficultyLevel, on_delete=models.CASCADE, related_name='challenges')
    points = models.IntegerField(default=100)
    flag = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    # Challenge-specific fields
    requires_authentication = models.BooleanField(default=True)
    chakra_cost = models.IntegerField(default=10)  # Chakra points required to attempt
    hint_available = models.BooleanField(default=True)
    
    # Fields for specific vulnerability types
    has_xss = models.BooleanField(default=False)
    has_sqli = models.BooleanField(default=False)
    has_csrf = models.BooleanField(default=False)
    has_file_upload = models.BooleanField(default=False)
    has_ssrf = models.BooleanField(default=False)
    has_command_injection = models.BooleanField(default=False)
    has_insecure_deserialization = models.BooleanField(default=False)
    has_websocket_vulnerability = models.BooleanField(default=False)
    has_api_vulnerability = models.BooleanField(default=False)
    has_graphql_vulnerability = models.BooleanField(default=False)
    has_race_condition = models.BooleanField(default=False)
    has_prototype_pollution = models.BooleanField(default=False)
    
    def __str__(self):
        return self.title

class Hint(models.Model):
    """Hints for challenges."""
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='hints')
    content = models.TextField()
    chakra_cost = models.IntegerField(default=5)  # Chakra points required to view hint
    
    def __str__(self):
        return f"Hint for {self.challenge.title}"

class ChallengeSolve(models.Model):
    """Record of challenge solves by users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='solves')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='solves')
    solved_at = models.DateTimeField(auto_now_add=True)
    attempts = models.IntegerField(default=1)
    
    class Meta:
        unique_together = ('user', 'challenge')
    
    def __str__(self):
        return f"{self.user.username} solved {self.challenge.title}"

class ChallengeAttempt(models.Model):
    """Record of challenge attempts by users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='attempts')
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE, related_name='attempts')
    submitted_flag = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)
    attempted_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} attempted {self.challenge.title}"

class HintUnlock(models.Model):
    """Record of hints unlocked by users."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='unlocked_hints')
    hint = models.ForeignKey(Hint, on_delete=models.CASCADE, related_name='unlocks')
    unlocked_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'hint')
    
    def __str__(self):
        return f"{self.user.username} unlocked hint for {self.hint.challenge.title}"
