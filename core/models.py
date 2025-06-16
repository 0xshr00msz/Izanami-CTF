"""
Models for the core app, including Izanami Loop feature.
"""

from django.db import models
from django.contrib.auth.models import User
import json
import random
from django.utils import timezone

class GameSettings(models.Model):
    """Global game settings."""
    game_name = models.CharField(max_length=200, default="Izanami: The Endless Loop")
    game_description = models.TextField(default="A web-based CTF game inspired by Itachi's Sharingan Izanami.")
    is_active = models.BooleanField(default=True)
    registration_open = models.BooleanField(default=True)
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    
    class Meta:
        verbose_name_plural = "Game Settings"
    
    def __str__(self):
        return self.game_name

class Announcement(models.Model):
    """Game announcements."""
    title = models.CharField(max_length=200)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_visible = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['-created_at']
    
    def __str__(self):
        return self.title

class RealityLayer(models.Model):
    """Represents different layers of reality in the Izanami Loop."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    level = models.IntegerField(default=1)
    escape_condition = models.TextField()  # Description of how to escape this layer
    escape_flag = models.CharField(max_length=255)  # Flag to escape this layer
    
    def __str__(self):
        return f"Reality Layer {self.level}: {self.name}"

class LoopPattern(models.Model):
    """Patterns that users need to recognize to escape the Izanami Loop."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    clue = models.TextField()  # Clue to help users recognize the pattern
    recognition_flag = models.CharField(max_length=255)  # Flag to submit when recognizing this pattern
    
    def __str__(self):
        return self.name

# Use string reference for Challenge to avoid circular import
class MemoryFragment(models.Model):
    """Memory fragments that players can collect to escape the Izanami Loop."""
    name = models.CharField(max_length=100)
    description = models.TextField()
    content = models.TextField()
    is_real = models.BooleanField(default=True)  # False for deceptive fragments
    challenge = models.ForeignKey('challenges.Challenge', on_delete=models.CASCADE, 
                                 related_name='memory_fragments', null=True, blank=True)
    image_url = models.CharField(max_length=255, blank=True, null=True)
    
    def __str__(self):
        return f"{self.name} ({'Real' if self.is_real else 'Deceptive'})"

class IzanamiLoop(models.Model):
    """Model for tracking player progress through the Izanami Loop."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='izanami_loop')
    current_loop = models.IntegerField(default=1)
    loop_start_time = models.DateTimeField(auto_now_add=True)
    loop_iterations = models.IntegerField(default=0)
    recognized_patterns = models.TextField(default="[]")  # JSON list of recognized patterns
    distortion_level = models.IntegerField(default=0)  # Affects UI/challenge distortions
    last_loop_time = models.DateTimeField(auto_now_add=True)
    
    def get_recognized_patterns(self):
        """Get the list of recognized patterns."""
        try:
            return json.loads(self.recognized_patterns)
        except:
            return []
    
    def add_recognized_pattern(self, pattern_id):
        """Add a recognized pattern."""
        patterns = self.get_recognized_patterns()
        if pattern_id not in patterns:
            patterns.append(pattern_id)
            self.recognized_patterns = json.dumps(patterns)
            self.save()
    
    def is_trapped(self):
        """Determine if user is still trapped in the loop."""
        patterns = self.get_recognized_patterns()
        return self.loop_iterations < 3 or len(patterns) < 5
    
    def progress_loop(self):
        """Progress the user through the loop."""
        self.loop_iterations += 1
        self.last_loop_time = timezone.now()
        if self.loop_iterations % 3 == 0:
            self.current_loop += 1
            self.distortion_level += 1
        self.save()
    
    def get_distortion_text(self, text):
        """Apply distortion to text based on distortion level."""
        if self.distortion_level <= 0:
            return text
            
        distortions = [
            lambda t: t,  # No distortion
            lambda t: t[::-1],  # Reverse text
            lambda t: ''.join(random.choice([c.upper(), c.lower()]) for c in t),  # Random case
            lambda t: ''.join(c if random.random() > 0.1 else '_' for c in t),  # Random blanks
            lambda t: t + " (or is it?)",  # Add doubt
            lambda t: "Maybe " + t,  # Add uncertainty
        ]
        
        # Apply multiple distortions based on level
        result = text
        for i in range(min(self.distortion_level, len(distortions))):
            if random.random() < 0.3:  # 30% chance to apply each distortion
                result = distortions[i](result)
                
        return result
    
    def __str__(self):
        return f"{self.user.username}'s Izanami Loop (Level {self.current_loop})"

class UserRealityLayer(models.Model):
    """Tracks which reality layer a user is currently in."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='reality_layer')
    layer = models.ForeignKey(RealityLayer, on_delete=models.CASCADE)
    entered_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return f"{self.user.username} in {self.layer.name}"

class CollectedFragment(models.Model):
    """Tracks which memory fragments a user has collected."""
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='collected_fragments')
    fragment = models.ForeignKey(MemoryFragment, on_delete=models.CASCADE)
    collected_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'fragment')
    
    def __str__(self):
        return f"{self.user.username} collected {self.fragment.name}"
