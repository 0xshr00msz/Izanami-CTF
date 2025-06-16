"""
Views for the core app, including Izanami Loop feature.
"""

import json
import random
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from django.db.models import Count, Avg
from django.db import models

from .models import (
    GameSettings, Announcement, MemoryFragment, IzanamiLoop,
    CollectedFragment, RealityLayer, UserRealityLayer, LoopPattern
)
from challenges.models import Challenge, ChallengeSolve

@login_required
def index(request):
    """Home page view."""
    # Get game settings
    try:
        settings = GameSettings.objects.first()
        if not settings:
            # Create default settings if none exist
            settings = GameSettings.objects.create(
                game_name="Izanami: The Endless Loop",
                game_description="A web-based CTF game inspired by Itachi's Sharingan Izanami.",
                is_active=True,
                registration_open=True,
                start_time=timezone.now(),
                end_time=timezone.now() + timezone.timedelta(days=90)
            )
    except:
        # If there's an error, create a dummy settings object
        settings = type('obj', (object,), {
            'game_name': "Izanami: The Endless Loop",
            'game_description': "A web-based CTF game inspired by Itachi's Sharingan Izanami."
        })
    
    # Get announcements
    try:
        announcements = Announcement.objects.filter(is_visible=True)[:5]
    except:
        announcements = []
    
    # Check if the tables exist before trying to get Izanami Loop status
    try:
        # Get user's Izanami Loop status
        izanami_loop, created = IzanamiLoop.objects.get_or_create(user=request.user)
        
        # Apply distortion to announcements if user is in the loop
        if not created and izanami_loop.distortion_level > 0:
            for announcement in announcements:
                announcement.title = izanami_loop.get_distortion_text(announcement.title)
                announcement.content = izanami_loop.get_distortion_text(announcement.content)
        
        # Get user's reality layer
        try:
            first_layer = RealityLayer.objects.first()
            if not first_layer:
                # Create a default reality layer if none exists
                first_layer = RealityLayer.objects.create(
                    name="First Illusion",
                    description="The first layer of the Izanami genjutsu. In this reality, things appear normal, but subtle distortions begin to manifest.",
                    level=1,
                    escape_condition="Find the hidden pattern in the Academy challenges and submit the escape flag.",
                    escape_flag="izanami{f1rst_l4y3r_br0k3n}"
                )
            
            user_layer, created = UserRealityLayer.objects.get_or_create(
                user=request.user,
                defaults={'layer': first_layer}
            )
            
            context = {
                'settings': settings,
                'announcements': announcements,
                'izanami_loop': izanami_loop,
                'reality_layer': user_layer.layer,
                'is_trapped': izanami_loop.is_trapped(),
            }
        except Exception as e:
            # If there's an error with reality layers
            context = {
                'settings': settings,
                'announcements': announcements,
                'izanami_loop': izanami_loop,
                'error': str(e)
            }
    except Exception as e:
        # If there's an error (e.g., tables don't exist), just use basic context
        context = {
            'settings': settings,
            'announcements': announcements,
            'error': str(e)
        }
    
    return render(request, 'core/index.html', context)

@login_required
def izanami_status(request):
    """View for showing the user's Izanami Loop status."""
    try:
        # Get user's Izanami Loop status
        izanami_loop, created = IzanamiLoop.objects.get_or_create(user=request.user)
        
        # Get collected fragments
        collected_fragments = CollectedFragment.objects.filter(user=request.user).select_related('fragment')
        
        # Get recognized patterns
        recognized_pattern_ids = izanami_loop.get_recognized_patterns()
        recognized_patterns = LoopPattern.objects.filter(id__in=recognized_pattern_ids)
        
        # Make sure we have at least one reality layer
        first_layer = RealityLayer.objects.first()
        if not first_layer:
            # Create a default reality layer if none exists
            first_layer = RealityLayer.objects.create(
                name="First Illusion",
                description="The first layer of the Izanami genjutsu. In this reality, things appear normal, but subtle distortions begin to manifest.",
                level=1,
                escape_condition="Find the hidden pattern in the Academy challenges and submit the escape flag.",
                escape_flag="izanami{f1rst_l4y3r_br0k3n}"
            )
        
        # Get user's reality layer
        user_layer, created = UserRealityLayer.objects.get_or_create(
            user=request.user,
            defaults={'layer': first_layer}
        )
        
        context = {
            'izanami_loop': izanami_loop,
            'collected_fragments': collected_fragments,
            'recognized_patterns': recognized_patterns,
            'reality_layer': user_layer.layer,
            'is_trapped': izanami_loop.is_trapped(),
            'remaining_patterns': 5 - len(recognized_pattern_ids),
            'remaining_iterations': max(0, 3 - izanami_loop.loop_iterations),
        }
    except Exception as e:
        # If there's an error, provide a basic context with the error
        context = {
            'error': str(e)
        }
    
    return render(request, 'core/izanami_status.html', context)

@login_required
def collect_fragment(request, fragment_id):
    """Collect a memory fragment."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        fragment = get_object_or_404(MemoryFragment, pk=fragment_id)
        
        # Check if already collected
        if CollectedFragment.objects.filter(user=request.user, fragment=fragment).exists():
            return JsonResponse({
                'success': False,
                'message': 'You have already collected this memory fragment.'
            })
        
        # Record the collection
        CollectedFragment.objects.create(user=request.user, fragment=fragment)
        
        # If this is a real fragment, check if it helps recognize a pattern
        if fragment.is_real:
            # Check if user has collected enough real fragments to recognize a pattern
            real_fragments_count = CollectedFragment.objects.filter(
                user=request.user, 
                fragment__is_real=True
            ).count()
            
            # Every 3 real fragments, we might recognize a pattern
            if real_fragments_count % 3 == 0:
                # Get user's Izanami Loop
                izanami_loop = IzanamiLoop.objects.get(user=request.user)
                
                # Get patterns not yet recognized
                recognized_patterns = izanami_loop.get_recognized_patterns()
                unrecognized_patterns = LoopPattern.objects.exclude(id__in=recognized_patterns)
                
                if unrecognized_patterns.exists():
                    # Recognize a new pattern
                    new_pattern = unrecognized_patterns.first()
                    izanami_loop.add_recognized_pattern(new_pattern.id)
                    
                    return JsonResponse({
                        'success': True,
                        'message': f'You collected the memory fragment: {fragment.name}',
                        'pattern_recognized': True,
                        'pattern_name': new_pattern.name,
                        'pattern_clue': new_pattern.clue
                    })
        
        return JsonResponse({
            'success': True,
            'message': f'You collected the memory fragment: {fragment.name}'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error collecting fragment: {str(e)}'
        }, status=500)

@login_required
def recognize_pattern(request):
    """Submit a flag to recognize a pattern."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        submitted_flag = request.POST.get('flag', '').strip()
        
        # Find the pattern with this recognition flag
        try:
            pattern = LoopPattern.objects.get(recognition_flag=submitted_flag)
        except LoopPattern.DoesNotExist:
            return JsonResponse({
                'success': False,
                'message': 'Invalid pattern recognition flag.'
            })
        
        # Get user's Izanami Loop
        izanami_loop = IzanamiLoop.objects.get(user=request.user)
        
        # Check if already recognized
        recognized_patterns = izanami_loop.get_recognized_patterns()
        if pattern.id in recognized_patterns:
            return JsonResponse({
                'success': False,
                'message': 'You have already recognized this pattern.'
            })
        
        # Add the recognized pattern
        izanami_loop.add_recognized_pattern(pattern.id)
        
        # Check if user has recognized enough patterns to progress
        if len(izanami_loop.get_recognized_patterns()) >= 5:
            # Progress to the next loop
            izanami_loop.progress_loop()
            
            return JsonResponse({
                'success': True,
                'message': f'Pattern recognized: {pattern.name}. You have progressed to loop {izanami_loop.current_loop}!',
                'loop_progressed': True,
                'current_loop': izanami_loop.current_loop
            })
        
        return JsonResponse({
            'success': True,
            'message': f'Pattern recognized: {pattern.name}. Recognize {5 - len(izanami_loop.get_recognized_patterns())} more patterns to progress.'
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error recognizing pattern: {str(e)}'
        }, status=500)

@login_required
def escape_reality(request):
    """Submit a flag to escape the current reality layer."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        submitted_flag = request.POST.get('flag', '').strip()
        
        # Get user's current reality layer
        user_layer = get_object_or_404(UserRealityLayer, user=request.user)
        current_layer = user_layer.layer
        
        # Check if the flag matches the escape flag for this layer
        if submitted_flag != current_layer.escape_flag:
            return JsonResponse({
                'success': False,
                'message': 'Invalid escape flag for this reality layer.'
            })
        
        # Find the next reality layer
        try:
            next_layer = RealityLayer.objects.get(level=current_layer.level + 1)
            user_layer.layer = next_layer
            user_layer.entered_at = timezone.now()
            user_layer.save()
            
            return JsonResponse({
                'success': True,
                'message': f'You have escaped {current_layer.name} and entered {next_layer.name}!',
                'new_layer': next_layer.name
            })
        except RealityLayer.DoesNotExist:
            # User has escaped all layers
            izanami_loop = IzanamiLoop.objects.get(user=request.user)
            izanami_loop.loop_iterations = 3  # Set to minimum required to escape
            izanami_loop.recognized_patterns = json.dumps([p.id for p in LoopPattern.objects.all()[:5]])
            izanami_loop.save()
            
            return JsonResponse({
                'success': True,
                'message': 'Congratulations! You have escaped all reality layers and broken free from the Izanami Loop!',
                'escaped': True
            })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error escaping reality: {str(e)}'
        }, status=500)

@login_required
def accept_reality(request):
    """Final step to break free from the Izanami Loop."""
    if request.method != 'POST':
        return JsonResponse({'error': 'Method not allowed'}, status=405)
    
    try:
        submitted_flag = request.POST.get('flag', '').strip()
        
        # The acceptance flag is a combination of all pattern recognition flags
        all_patterns = LoopPattern.objects.all()
        
        if all_patterns.count() < 5:
            # Create default patterns if they don't exist
            if all_patterns.count() == 0:
                LoopPattern.objects.create(
                    name="Repeating Challenges",
                    description="Challenges that appear to be different but follow the same underlying pattern.",
                    clue="Look for challenges with similar solutions but different presentations.",
                    recognition_flag="izanami{r3p34t1ng_p4tt3rn}"
                )
                LoopPattern.objects.create(
                    name="False Flags",
                    description="Some flags appear to be correct but lead deeper into the loop.",
                    clue="Not all flags that work are the true flags. Look for inconsistencies in the reward system.",
                    recognition_flag="izanami{f4ls3_fl4gs_d3c3pt10n}"
                )
                LoopPattern.objects.create(
                    name="Memory Distortion",
                    description="Your memories of previous challenges are being distorted.",
                    clue="Compare challenge descriptions over time to spot subtle changes.",
                    recognition_flag="izanami{m3m0ry_d1st0rt10n}"
                )
                LoopPattern.objects.create(
                    name="Reality Layers",
                    description="The Izanami Loop consists of multiple layers of reality.",
                    clue="Each time you think you've escaped, you're just entering a deeper layer.",
                    recognition_flag="izanami{l4y3r3d_r34l1ty}"
                )
                LoopPattern.objects.create(
                    name="Self Acceptance",
                    description="The only way to break free from the Izanami Loop is to accept your true self.",
                    clue="Collect all real memory fragments to piece together your true identity.",
                    recognition_flag="izanami{tru3_s3lf_4cc3pt4nc3}"
                )
                all_patterns = LoopPattern.objects.all()
        
        try:
            acceptance_flag = "izanami{" + "_".join([p.recognition_flag.split("{")[1].split("}")[0] for p in all_patterns[:5]]) + "}"
        except:
            # Fallback acceptance flag
            acceptance_flag = "izanami{tru3_s3lf_4cc3pt4nc3}"
        
        if submitted_flag != acceptance_flag:
            return JsonResponse({
                'success': False,
                'message': 'Invalid acceptance flag. You must truly understand the nature of the loop to escape.'
            })
        
        # User has accepted reality and escaped the loop
        izanami_loop = IzanamiLoop.objects.get(user=request.user)
        izanami_loop.loop_iterations = 3  # Set to minimum required to escape
        izanami_loop.recognized_patterns = json.dumps([p.id for p in all_patterns[:5]])
        izanami_loop.save()
        
        # Award special achievement
        try:
            from accounts.models import Achievement, PlayerAchievement
            achievement, created = Achievement.objects.get_or_create(
                name="Reality Breaker",
                defaults={
                    'description': "Break free from the Izanami Loop by accepting your true self",
                    'icon': "fa-eye-slash"
                }
            )
            PlayerAchievement.objects.get_or_create(player=request.user.profile, achievement=achievement)
        except:
            # Skip achievement if there's an error
            pass
        
        return JsonResponse({
            'success': True,
            'message': 'Congratulations! You have accepted reality and broken free from the Izanami Loop!',
            'escaped': True
        })
    except Exception as e:
        return JsonResponse({
            'success': False,
            'message': f'Error accepting reality: {str(e)}'
        }, status=500)

@login_required
def distorted_challenge(request, challenge_id):
    """Show a distorted version of a challenge based on Izanami Loop level."""
    try:
        challenge = get_object_or_404(Challenge, pk=challenge_id)
        
        # Get user's Izanami Loop
        izanami_loop, created = IzanamiLoop.objects.get_or_create(user=request.user)
        
        # Apply distortion to challenge
        distorted_title = izanami_loop.get_distortion_text(challenge.title)
        distorted_description = izanami_loop.get_distortion_text(challenge.description)
        
        # Check if this challenge has a memory fragment
        has_fragment = MemoryFragment.objects.filter(challenge=challenge).exists()
        
        # Check if user has already collected the fragment
        fragment_collected = False
        fragment_id = None
        if has_fragment:
            fragment = MemoryFragment.objects.get(challenge=challenge)
            fragment_id = fragment.id
            fragment_collected = CollectedFragment.objects.filter(user=request.user, fragment=fragment).exists()
        
        context = {
            'challenge': challenge,
            'distorted_title': distorted_title,
            'distorted_description': distorted_description,
            'izanami_loop': izanami_loop,
            'has_fragment': has_fragment,
            'fragment_collected': fragment_collected,
            'fragment_id': fragment_id,
        }
    except Exception as e:
        context = {
            'error': str(e)
        }
    
    return render(request, 'core/distorted_challenge.html', context)

@login_required
def loop_analytics(request):
    """Admin view for Izanami Loop analytics."""
    if not request.user.is_staff:
        return redirect('core:index')
    
    try:
        # Get loop statistics
        total_users = IzanamiLoop.objects.count()
        escaped_users = IzanamiLoop.objects.filter(loop_iterations__gte=3).count()
        avg_iterations = IzanamiLoop.objects.aggregate(avg_iterations=Avg('loop_iterations'))['avg_iterations'] or 0
        
        # Get pattern recognition statistics
        pattern_stats = []
        for pattern in LoopPattern.objects.all():
            recognized_count = IzanamiLoop.objects.filter(recognized_patterns__contains=str(pattern.id)).count()
            pattern_stats.append({
                'pattern': pattern,
                'recognized_count': recognized_count,
                'recognition_rate': (recognized_count / total_users * 100) if total_users > 0 else 0
            })
        
        # Get fragment collection statistics
        fragment_stats = []
        for fragment in MemoryFragment.objects.all():
            collected_count = CollectedFragment.objects.filter(fragment=fragment).count()
            fragment_stats.append({
                'fragment': fragment,
                'collected_count': collected_count,
                'collection_rate': (collected_count / total_users * 100) if total_users > 0 else 0
            })
        
        context = {
            'total_users': total_users,
            'escaped_users': escaped_users,
            'escape_rate': (escaped_users / total_users * 100) if total_users > 0 else 0,
            'avg_iterations': round(avg_iterations, 2),
            'pattern_stats': pattern_stats,
            'fragment_stats': fragment_stats,
        }
    except Exception as e:
        context = {
            'error': str(e)
        }
    
    return render(request, 'core/loop_analytics.html', context)
