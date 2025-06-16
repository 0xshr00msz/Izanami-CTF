"""
Views for the accounts app.
"""

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm
from .models import PlayerProfile, Achievement, PlayerAchievement

def register(request):
    """Register a new user."""
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create player profile
            PlayerProfile.objects.create(user=user)
            username = form.cleaned_data.get('username')
            messages.success(request, f'Account created for {username}! You can now log in.')
            return redirect('accounts:login')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/register.html', {'form': form})

def login_view(request):
    """Login view with deliberate vulnerabilities for CSRF challenges."""
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('challenges:index')
        else:
            messages.error(request, 'Invalid username or password.')
    return render(request, 'accounts/login.html')

@login_required
def profile(request):
    """User profile view."""
    achievements = PlayerAchievement.objects.filter(player=request.user.profile)
    context = {
        'achievements': achievements,
    }
    return render(request, 'accounts/profile.html', context)

@login_required
def edit_profile(request):
    """Edit user profile."""
    if request.method == 'POST':
        u_form = UserUpdateForm(request.POST, instance=request.user)
        p_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your profile has been updated!')
            return redirect('accounts:profile')
    else:
        u_form = UserUpdateForm(instance=request.user)
        p_form = ProfileUpdateForm(instance=request.user.profile)
    
    context = {
        'u_form': u_form,
        'p_form': p_form,
    }
    return render(request, 'accounts/edit_profile.html', context)

@login_required
def achievements(request):
    """View user achievements."""
    player_achievements = PlayerAchievement.objects.filter(player=request.user.profile)
    all_achievements = Achievement.objects.all()
    
    # Create a list of achievements with earned status
    achievements_list = []
    for achievement in all_achievements:
        earned = player_achievements.filter(achievement=achievement).exists()
        achievements_list.append({
            'achievement': achievement,
            'earned': earned,
            'earned_at': player_achievements.get(achievement=achievement).earned_at if earned else None,
        })
    
    context = {
        'achievements_list': achievements_list,
    }
    return render(request, 'accounts/achievements.html', context)

@csrf_exempt
@login_required
def regenerate_chakra(request):
    """API endpoint to regenerate chakra."""
    if request.method == 'POST':
        profile = request.user.profile
        
        # Regenerate chakra (10 points)
        new_chakra = min(100, profile.chakra_meter + 10)
        profile.chakra_meter = new_chakra
        profile.save()
        
        return JsonResponse({
            'success': True,
            'chakra': profile.chakra_meter
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)
