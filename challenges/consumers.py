"""
WebSocket consumers for the challenges app.
"""

import json
from channels.generic.websocket import AsyncWebsocketConsumer
from channels.db import database_sync_to_async
from django.contrib.auth.models import User
from .models import Challenge

class ChallengeConsumer(AsyncWebsocketConsumer):
    """WebSocket consumer for challenge interactions."""
    
    async def connect(self):
        """Handle WebSocket connection."""
        self.challenge_id = self.scope['url_route']['kwargs']['challenge_id']
        self.challenge_group_name = f'challenge_{self.challenge_id}'
        
        # Join challenge group
        await self.channel_layer.group_add(
            self.challenge_group_name,
            self.channel_name
        )
        
        # Accept the connection (deliberately vulnerable - no proper authentication)
        await self.accept()
        
        # Send challenge data
        challenge = await self.get_challenge(self.challenge_id)
        if challenge:
            await self.send(text_data=json.dumps({
                'type': 'challenge_data',
                'title': challenge['title'],
                'description': challenge['description'],
            }))
    
    async def disconnect(self, close_code):
        """Handle WebSocket disconnection."""
        # Leave challenge group
        await self.channel_layer.group_discard(
            self.challenge_group_name,
            self.channel_name
        )
    
    async def receive(self, text_data):
        """Handle received messages."""
        data = json.loads(text_data)
        message_type = data.get('type', '')
        
        if message_type == 'submit_flag':
            # Process flag submission
            flag = data.get('flag', '')
            username = data.get('username', '')  # Deliberately vulnerable - trusting client data
            
            # Verify flag (deliberately vulnerable - no proper authentication)
            is_correct = await self.verify_flag(self.challenge_id, flag)
            
            # Send response
            await self.send(text_data=json.dumps({
                'type': 'flag_result',
                'is_correct': is_correct,
                'message': 'Correct flag!' if is_correct else 'Incorrect flag!',
            }))
        
        elif message_type == 'chat_message':
            # Broadcast chat message to group (deliberately vulnerable - no sanitization)
            message = data.get('message', '')
            username = data.get('username', 'Anonymous')
            
            await self.channel_layer.group_send(
                self.challenge_group_name,
                {
                    'type': 'chat_message',
                    'message': message,
                    'username': username,
                }
            )
    
    async def chat_message(self, event):
        """Send chat message to WebSocket."""
        message = event['message']
        username = event['username']
        
        # Send message to WebSocket (deliberately vulnerable - no sanitization)
        await self.send(text_data=json.dumps({
            'type': 'chat_message',
            'message': message,
            'username': username,
        }))
    
    @database_sync_to_async
    def get_challenge(self, challenge_id):
        """Get challenge data."""
        try:
            challenge = Challenge.objects.get(pk=challenge_id)
            return {
                'title': challenge.title,
                'description': challenge.description,
                'flag': challenge.flag,  # Deliberately vulnerable - sending flag to client
            }
        except Challenge.DoesNotExist:
            return None
    
    @database_sync_to_async
    def verify_flag(self, challenge_id, flag):
        """Verify if a flag is correct."""
        try:
            challenge = Challenge.objects.get(pk=challenge_id)
            return challenge.flag == flag
        except Challenge.DoesNotExist:
            return False
