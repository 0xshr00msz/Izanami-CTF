"""
Views for the scoreboard app.
"""

from django.shortcuts import render
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import ScoreboardEntry

@login_required
def scoreboard(request):
    """Scoreboard view."""
    entries = ScoreboardEntry.objects.all().order_by('rank')[:100]
    
    # Get current user's rank
    try:
        user_entry = ScoreboardEntry.objects.get(user=request.user)
        user_rank = user_entry.rank
    except ScoreboardEntry.DoesNotExist:
        user_rank = None
    
    context = {
        'entries': entries,
        'user_rank': user_rank,
    }
    return render(request, 'scoreboard/scoreboard.html', context)

def scoreboard_data(request):
    """API endpoint for scoreboard data."""
    entries = ScoreboardEntry.objects.all().order_by('rank')[:100]
    
    data = []
    for entry in entries:
        data.append({
            'rank': entry.rank,
            'username': entry.user.username,
            'score': entry.score,
            'last_solve': entry.last_solve_time.isoformat() if entry.last_solve_time else None,
        })
    
    return JsonResponse({'data': data})
