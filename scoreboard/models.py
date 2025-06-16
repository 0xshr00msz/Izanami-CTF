"""
Models for the scoreboard app.
"""

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from challenges.models import ChallengeSolve

class ScoreboardEntry(models.Model):
    """Scoreboard entry for a user."""
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='scoreboard_entry')
    score = models.IntegerField(default=0)
    last_solve_time = models.DateTimeField(null=True, blank=True)
    rank = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['-score', 'last_solve_time']
        verbose_name_plural = "Scoreboard Entries"
    
    def __str__(self):
        return f"{self.user.username}'s Score: {self.score}"

@receiver(post_save, sender=ChallengeSolve)
def update_scoreboard(sender, instance, created, **kwargs):
    """Update scoreboard when a challenge is solved."""
    if created:
        # Get or create scoreboard entry
        entry, _ = ScoreboardEntry.objects.get_or_create(user=instance.user)
        
        # Update score
        entry.score += instance.challenge.points
        entry.last_solve_time = instance.solved_at
        entry.save()
        
        # Update ranks for all entries
        entries = ScoreboardEntry.objects.all().order_by('-score', 'last_solve_time')
        for i, entry in enumerate(entries, 1):
            entry.rank = i
            entry.save(update_fields=['rank'])
