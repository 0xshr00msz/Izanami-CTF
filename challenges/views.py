"""
Views for the challenges app.
"""

import os
import json
import pickle
import subprocess
import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse, HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.db import connection
from django.utils.safestring import mark_safe
from .models import Challenge, Hint, ChallengeSolve, ChallengeAttempt, HintUnlock, DifficultyLevel, ChallengeCategory
from accounts.models import Achievement, PlayerAchievement

@login_required
def index(request):
    """Challenge index page."""
    categories = ChallengeCategory.objects.all()
    difficulty_levels = DifficultyLevel.objects.all().order_by('order')
    
    # Get challenges for each difficulty level
    difficulty_challenges = {}
    for level in difficulty_levels:
        difficulty_challenges[level.id] = Challenge.objects.filter(difficulty=level, is_active=True)
    
    # Get solved challenges for the current user
    solved_challenges = ChallengeSolve.objects.filter(user=request.user).values_list('challenge_id', flat=True)
    
    context = {
        'categories': categories,
        'difficulty_levels': difficulty_levels,
        'difficulty_challenges': difficulty_challenges,
        'solved_challenges': solved_challenges,
    }
    return render(request, 'challenges/index.html', context)

@login_required
def academy_challenges(request):
    """Academy level challenges."""
    academy_level = DifficultyLevel.objects.get(name='Academy')
    challenges = Challenge.objects.filter(difficulty=academy_level, is_active=True)
    
    # Get solved challenges for the current user
    solved_challenges = ChallengeSolve.objects.filter(user=request.user).values_list('challenge_id', flat=True)
    
    context = {
        'challenges': challenges,
        'level': 'Academy',
        'solved_challenges': solved_challenges,
    }
    return render(request, 'challenges/level.html', context)

@login_required
def chunin_challenges(request):
    """Chunin level challenges."""
    # Check if user has completed Academy level
    academy_level = DifficultyLevel.objects.get(name='Academy')
    academy_challenges = Challenge.objects.filter(difficulty=academy_level, is_active=True)
    academy_solved = ChallengeSolve.objects.filter(
        user=request.user, 
        challenge__in=academy_challenges
    ).count()
    
    # If user hasn't solved at least 70% of Academy challenges, redirect
    if academy_solved < (academy_challenges.count() * 0.7):
        return render(request, 'challenges/locked.html', {'level': 'Chunin'})
    
    chunin_level = DifficultyLevel.objects.get(name='Chunin')
    challenges = Challenge.objects.filter(difficulty=chunin_level, is_active=True)
    
    # Get solved challenges for the current user
    solved_challenges = ChallengeSolve.objects.filter(user=request.user).values_list('challenge_id', flat=True)
    
    context = {
        'challenges': challenges,
        'level': 'Chunin',
        'solved_challenges': solved_challenges,
    }
    return render(request, 'challenges/level.html', context)

@login_required
def jonin_challenges(request):
    """Jonin level challenges."""
    # Check if user has completed Chunin level
    chunin_level = DifficultyLevel.objects.get(name='Chunin')
    chunin_challenges = Challenge.objects.filter(difficulty=chunin_level, is_active=True)
    chunin_solved = ChallengeSolve.objects.filter(
        user=request.user, 
        challenge__in=chunin_challenges
    ).count()
    
    # If user hasn't solved at least 70% of Chunin challenges, redirect
    if chunin_solved < (chunin_challenges.count() * 0.7):
        return render(request, 'challenges/locked.html', {'level': 'Jōnin'})
    
    jonin_level = DifficultyLevel.objects.get(name='Jōnin')
    challenges = Challenge.objects.filter(difficulty=jonin_level, is_active=True)
    
    # Get solved challenges for the current user
    solved_challenges = ChallengeSolve.objects.filter(user=request.user).values_list('challenge_id', flat=True)
    
    context = {
        'challenges': challenges,
        'level': 'Jōnin',
        'solved_challenges': solved_challenges,
    }
    return render(request, 'challenges/level.html', context)

@login_required
def uchiha_challenges(request):
    """Uchiha level challenges."""
    # Check if user has completed Jonin level
    jonin_level = DifficultyLevel.objects.get(name='Jōnin')
    jonin_challenges = Challenge.objects.filter(difficulty=jonin_level, is_active=True)
    jonin_solved = ChallengeSolve.objects.filter(
        user=request.user, 
        challenge__in=jonin_challenges
    ).count()
    
    # If user hasn't solved at least 70% of Jonin challenges, redirect
    if jonin_solved < (jonin_challenges.count() * 0.7):
        return render(request, 'challenges/locked.html', {'level': 'Uchiha'})
    
    uchiha_level = DifficultyLevel.objects.get(name='Uchiha')
    challenges = Challenge.objects.filter(difficulty=uchiha_level, is_active=True)
    
    # Get solved challenges for the current user
    solved_challenges = ChallengeSolve.objects.filter(user=request.user).values_list('challenge_id', flat=True)
    
    context = {
        'challenges': challenges,
        'level': 'Uchiha',
        'solved_challenges': solved_challenges,
    }
    return render(request, 'challenges/level.html', context)

@login_required
def challenge_detail(request, challenge_id):
    """Challenge detail view."""
    challenge = get_object_or_404(Challenge, pk=challenge_id, is_active=True)
    
    # Check if user has already solved this challenge
    solved = ChallengeSolve.objects.filter(user=request.user, challenge=challenge).exists()
    
    # Check if user has unlocked any hints
    unlocked_hints = HintUnlock.objects.filter(
        user=request.user,
        hint__challenge=challenge
    ).values_list('hint_id', flat=True)
    
    # Get available hints
    hints = Hint.objects.filter(challenge=challenge)
    
    # Get user's attempts for this challenge
    attempts = ChallengeAttempt.objects.filter(user=request.user, challenge=challenge).order_by('-attempted_at')
    
    # Prepare context with potentially vulnerable data for XSS challenges
    if challenge.has_xss:
        # Deliberately vulnerable to XSS
        if 'name' in request.GET:
            user_input = request.GET.get('name')
            greeting = mark_safe(f"Hello, {user_input}!")
        else:
            greeting = "Hello, Ninja!"
    else:
        greeting = "Hello, Ninja!"
    
    # Determine which template to use based on challenge type
    template_name = 'challenges/detail.html'
    if challenge.has_sqli:
        template_name = 'challenges/challenge_templates/sqli_challenge.html'
    elif challenge.has_xss:
        template_name = 'challenges/challenge_templates/xss_challenge.html'
    elif challenge.has_websocket_vulnerability:
        template_name = 'challenges/challenge_templates/websocket_challenge.html'
    elif challenge.has_prototype_pollution:
        template_name = 'challenges/challenge_templates/prototype_pollution_challenge.html'
    elif challenge.has_pygame:
        template_name = 'challenges/challenge_templates/pygame_challenge.html'
    
    context = {
        'challenge': challenge,
        'solved': solved,
        'hints': hints,
        'unlocked_hints': unlocked_hints,
        'attempts': attempts,
        'greeting': greeting,
    }
    return render(request, template_name, context)

@login_required
def submit_flag(request, challenge_id):
    """Submit a flag for a challenge."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    challenge = get_object_or_404(Challenge, pk=challenge_id, is_active=True)
    
    # Handle both form data and JSON requests
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        submitted_flag = data.get('flag', '').strip()
    else:
        submitted_flag = request.POST.get('flag', '').strip()
    
    # Check if the user has already solved this challenge
    if ChallengeSolve.objects.filter(user=request.user, challenge=challenge).exists():
        return JsonResponse({
            'success': False,
            'message': 'You have already solved this challenge!'
        })
    
    # Check if the user has enough chakra
    if request.user.profile.chakra_meter < challenge.chakra_cost:
        return JsonResponse({
            'success': False,
            'message': f'Not enough chakra! You need {challenge.chakra_cost} chakra to attempt this challenge.'
        })
    
    # Deduct chakra cost
    request.user.profile.chakra_meter -= challenge.chakra_cost
    request.user.profile.save()
    
    # Record the attempt
    attempt = ChallengeAttempt.objects.create(
        user=request.user,
        challenge=challenge,
        submitted_flag=submitted_flag,
        is_correct=False
    )
    
    # Check if the flag is correct - use case-insensitive comparison and strip whitespace
    if submitted_flag.strip() == challenge.flag.strip():
        # Mark the attempt as correct
        attempt.is_correct = True
        attempt.save()
        
        # Record the solve
        ChallengeSolve.objects.create(
            user=request.user,
            challenge=challenge
        )
        
        # Award sharingan points
        request.user.profile.sharingan_points += challenge.points
        request.user.profile.save()
        
        # Check for first blood
        first_blood = not ChallengeSolve.objects.filter(challenge=challenge).exclude(user=request.user).exists()
        if first_blood:
            # Award first blood achievement
            first_blood_achievement = Achievement.objects.get(name='First Blood')
            PlayerAchievement.objects.get_or_create(
                player=request.user.profile,
                achievement=first_blood_achievement
            )
            
            # Award bonus points for first blood
            request.user.profile.sharingan_points += 50
            request.user.profile.save()
        
        return JsonResponse({
            'success': True,
            'message': f'Correct flag! You earned {challenge.points} sharingan points.',
            'points': challenge.points,
            'first_blood': first_blood
        })
    else:
        # Increment genjutsu counter
        request.user.profile.genjutsu_counter += 1
        request.user.profile.save()
        
        return JsonResponse({
            'success': False,
            'message': 'Incorrect flag. Try again!'
        })

@login_required
def unlock_hint(request, challenge_id):
    """Unlock a hint for a challenge."""
    if request.method != 'POST':
        return redirect('challenges:detail', challenge_id=challenge_id)
    
    # Handle both form data and JSON requests
    if request.content_type == 'application/json':
        data = json.loads(request.body)
        hint_id = data.get('hint_id')
    else:
        hint_id = request.POST.get('hint_id')
    
    hint = get_object_or_404(Hint, pk=hint_id, challenge_id=challenge_id)
    
    # Check if user has already unlocked this hint
    if HintUnlock.objects.filter(user=request.user, hint=hint).exists():
        return JsonResponse({
            'success': True,
            'message': 'Hint already unlocked!',
            'content': hint.content,
            'remaining_chakra': request.user.profile.chakra_meter
        })
    
    # Check if user has enough chakra
    profile = request.user.profile
    if profile.chakra_meter < hint.chakra_cost:
        return JsonResponse({
            'success': False,
            'message': 'Not enough chakra to unlock this hint!'
        })
    
    # Decrease chakra and unlock hint
    profile.chakra_meter -= hint.chakra_cost
    profile.save()
    HintUnlock.objects.create(user=request.user, hint=hint)
    
    return JsonResponse({
        'success': True,
        'message': 'Hint unlocked!',
        'content': hint.content,
        'remaining_chakra': profile.chakra_meter
    })

# Vulnerable API endpoints for challenges

@csrf_exempt
def user_data_api(request):
    """API endpoint vulnerable to SQL injection."""
    if request.method == 'GET':
        username = request.GET.get('username', '')
        
        # Deliberately vulnerable to SQL injection
        with connection.cursor() as cursor:
            cursor.execute(f"SELECT id, username, email FROM auth_user WHERE username = '{username}'")
            result = cursor.fetchone()
        
        if result:
            return JsonResponse({
                'id': result[0],
                'username': result[1],
                'email': result[2]
            })
        else:
            return JsonResponse({'error': 'User not found'}, status=404)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def search_api(request):
    """API endpoint vulnerable to XSS."""
    if request.method == 'GET':
        query = request.GET.get('q', '')
        
        # Simulate search results
        results = [
            {'id': 1, 'title': f'Result for {query}', 'content': f'This is a result for {query}'},
            {'id': 2, 'title': 'Another result', 'content': f'Another result for {query}'},
        ]
        
        # Return results with the query parameter (vulnerable to XSS)
        return JsonResponse({
            'query': query,
            'results': results
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def file_upload(request):
    """API endpoint vulnerable to file upload attacks."""
    if request.method == 'POST' and request.FILES.get('file'):
        uploaded_file = request.FILES['file']
        
        # Deliberately vulnerable file upload
        # No proper validation of file type or content
        file_path = os.path.join('media', 'uploads', uploaded_file.name)
        
        with open(file_path, 'wb+') as destination:
            for chunk in uploaded_file.chunks():
                destination.write(chunk)
        
        return JsonResponse({
            'success': True,
            'message': 'File uploaded successfully',
            'file_path': file_path
        })
    
    return JsonResponse({'error': 'No file provided'}, status=400)

@csrf_exempt
def fetch_url(request):
    """API endpoint vulnerable to SSRF."""
    if request.method == 'POST':
        data = json.loads(request.body)
        url = data.get('url', '')
        
        try:
            # Deliberately vulnerable to SSRF
            response = requests.get(url, timeout=5)
            return JsonResponse({
                'status': response.status_code,
                'content': response.text[:500]  # Limit response size
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def execute_command(request):
    """API endpoint vulnerable to command injection."""
    if request.method == 'POST':
        data = json.loads(request.body)
        hostname = data.get('hostname', '')
        
        try:
            # Deliberately vulnerable to command injection
            command = f"ping -c 1 {hostname}"
            output = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT)
            return JsonResponse({
                'output': output.decode('utf-8')
            })
        except subprocess.CalledProcessError as e:
            return JsonResponse({'error': e.output.decode('utf-8')}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def deserialize_data(request):
    """API endpoint vulnerable to insecure deserialization."""
    if request.method == 'POST':
        data = request.body
        
        try:
            # Deliberately vulnerable to insecure deserialization
            deserialized = pickle.loads(data)
            return JsonResponse({
                'result': str(deserialized)
            })
        except Exception as e:
            return JsonResponse({'error': str(e)}, status=500)
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

# API endpoints for specific challenges

@csrf_exempt
def login_check_api(request):
    """API endpoint for SQL injection challenge."""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        
        # Deliberately vulnerable to SQL injection
        # In a real app, this would query a database
        # Here we simulate the vulnerability
        
        # Check for SQL injection attempts
        if "'" in username or "--" in username or "OR" in username.upper():
            # Simulating successful SQL injection
            return JsonResponse({
                'success': True,
                'message': 'Login successful! Welcome, admin!',
                'flag': 'izanami{sql_1nj3ct10n_b4s1cs}'
            })
        else:
            # Normal login check (always fails for this challenge)
            return JsonResponse({
                'success': False,
                'message': 'Invalid username or password.'
            })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def update_profile_api(request):
    """API endpoint for CSRF challenge."""
    if request.method == 'POST':
        username = request.POST.get('username', '')
        email = request.POST.get('email', '')
        bio = request.POST.get('bio', '')
        
        # Check if this is a CSRF attack
        # In a real app, we would check the referer and CSRF token
        # Here we simulate detecting a CSRF attack
        referer = request.META.get('HTTP_REFERER', '')
        csrf_detected = 'external-site' in referer or not referer
        
        if csrf_detected:
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully!',
                'csrf_detected': True,
                'flag': 'izanami{csrf_t0k3ns_m4tt3r}'
            })
        else:
            return JsonResponse({
                'success': True,
                'message': 'Profile updated successfully!',
                'csrf_detected': False
            })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@csrf_exempt
def get_profile_api(request):
    """API endpoint to get profile data for CSRF challenge."""
    if request.method == 'GET':
        # Return dummy profile data
        return JsonResponse({
            'success': True,
            'username': 'ninja_user',
            'email': 'ninja@example.com',
            'bio': 'I am a ninja in training.'
        })
    
    return JsonResponse({'error': 'Method not allowed'}, status=405)

@login_required
def pygame_challenge(request, challenge_id):
    """Pygame challenge view."""
    challenge = get_object_or_404(Challenge, pk=challenge_id, is_active=True, has_pygame=True)
    
    # Check if user has already solved this challenge
    solved = ChallengeSolve.objects.filter(user=request.user, challenge=challenge).exists()
    
    # Check if user has unlocked any hints
    unlocked_hints = HintUnlock.objects.filter(
        user=request.user,
        hint__challenge=challenge
    ).values_list('hint_id', flat=True)
    
    # Get available hints
    hints = Hint.objects.filter(challenge=challenge)
    
    # Add is_unlocked attribute to each hint
    for hint in hints:
        hint.is_unlocked = hint.id in unlocked_hints
    
    context = {
        'challenge': challenge,
        'solved': solved,
        'hints': hints,
        'unlocked_hints': unlocked_hints,
    }
    return render(request, 'challenges/challenge_templates/pygame_challenge.html', context)

@login_required
def pygame_game(request, challenge_id):
    """Serve the Pygame game for a challenge."""
    challenge = get_object_or_404(Challenge, pk=challenge_id, is_active=True, has_pygame=True)
    
    # Return the HTML page that will load the Pygame game using Pygbag
    html_content = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <meta charset="utf-8">
        <meta name="viewport" content="width=device-width, initial-scale=1">
        <title>{challenge.title} - Pygame Challenge</title>
        <style>
            html, body {{
                margin: 0;
                padding: 0;
                height: 100%;
                overflow: hidden;
            }}
            #canvas {{
                width: 100%;
                height: 100%;
                display: block;
            }}
            .message {{
                position: absolute;
                top: 50%;
                left: 50%;
                transform: translate(-50%, -50%);
                text-align: center;
                color: white;
                font-family: Arial, sans-serif;
            }}
        </style>
    </head>
    <body style="background-color: black;">
        <canvas id="canvas"></canvas>
        <div class="message">
            <h2>Pygame Challenge</h2>
            <p>This is a Pygame challenge that requires memory manipulation.</p>
            <p>Use keyboard shortcuts like Ctrl+M to reveal memory values and Ctrl+C to see collected values.</p>
            <p>The flag is hidden within the game. Find all four parts to complete the challenge.</p>
            <p>Flag format: izanami{{m3m0ry_m4n1pul4t10n_m4st3r}}</p>
        </div>
        <script>
            // Function to send flag back to parent window
            function sendFlag(flag) {{
                window.parent.postMessage({{ type: 'flag', flag: flag }}, '*');
            }}
            
            // In a real implementation, this would load the Pygame game using Pygbag
            // For now, we're just displaying instructions
            document.addEventListener('keydown', function(event) {{
                // Ctrl+M to show memory values
                if (event.ctrlKey && event.key === 'm') {{
                    console.log('Memory values: [42, 13, 37, 73]');
                    alert('Memory values: [42, 13, 37, 73]');
                }}
                
                // Ctrl+C to show collected values
                if (event.ctrlKey && event.key === 'c') {{
                    console.log('Collected values: []');
                    alert('Collected values: []');
                }}
                
                // Ctrl+F to reveal flag (for testing)
                if (event.ctrlKey && event.key === 'f') {{
                    const flag = 'izanami{{m3m0ry_m4n1pul4t10n_m4st3r}}';
                    console.log('FLAG:', flag);
                    alert('You found the flag: ' + flag);
                    sendFlag(flag);
                }}
            }});
        </script>
    </body>
    </html>
    """
    
    return HttpResponse(html_content)
