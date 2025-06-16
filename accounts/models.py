"""
Models for the accounts app.
"""

from django.db import models
from django.contrib.auth.models import User

class PlayerProfile(models.Model):
    """Extended user profile for players."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    sharingan_points = models.IntegerField(default=0)
    chakra_meter = models.IntegerField(default=100)
    current_level = models.CharField(
        max_length=20, 
        choices=[
            ('academy', 'Academy'),
            ('chunin', 'Chunin'),
            ('jonin', 'Jōnin'),
            ('uchiha', 'Uchiha'),
        ],
        default='academy'
    )
    genjutsu_counter = models.IntegerField(default=0)  # Number of loops the player has been through
    last_active = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return f"{self.user.username}'s Profile"
    
    def increase_sharingan_points(self, points):
        """Increase player's Sharingan points."""
        self.sharingan_points += points
        self.save()
    
    def decrease_chakra(self, amount):
        """Decrease player's chakra meter."""
        self.chakra_meter = max(0, self.chakra_meter - amount)
        self.save()
    
    def refill_chakra(self):
        """Refill player's chakra meter."""
        self.chakra_meter = 100
        self.save()
    
    def increment_genjutsu_counter(self):
        """Increment the genjutsu counter (loop counter)."""
        self.genjutsu_counter += 1
        self.save()

class Achievement(models.Model):
    """Player achievements."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    icon = models.CharField(max_length=50)  # CSS class for the icon
    
    def __str__(self):
        return self.name

class PlayerAchievement(models.Model):
    """Achievements earned by players."""
    player = models.ForeignKey(PlayerProfile, on_delete=models.CASCADE, related_name='achievements')
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)
    earned_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('player', 'achievement')
    
    def __str__(self):
        return f"{self.player.user.username} - {self.achievement.name}"
