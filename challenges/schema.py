"""
GraphQL schema for the challenges app.
"""

import graphene
from graphene_django import DjangoObjectType
from django.contrib.auth.models import User
from .models import Challenge, ChallengeCategory, DifficultyLevel, ChallengeSolve

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')

class ChallengeCategoryType(DjangoObjectType):
    class Meta:
        model = ChallengeCategory
        fields = ('id', 'name', 'description', 'icon')

class DifficultyLevelType(DjangoObjectType):
    class Meta:
        model = DifficultyLevel
        fields = ('id', 'name', 'description', 'order')

class ChallengeType(DjangoObjectType):
    class Meta:
        model = Challenge
        fields = ('id', 'title', 'description', 'category', 'difficulty', 'points')

class ChallengeSolveType(DjangoObjectType):
    class Meta:
        model = ChallengeSolve
        fields = ('id', 'user', 'challenge', 'solved_at', 'attempts')

class Query(graphene.ObjectType):
    """GraphQL queries."""
    
    # Deliberately vulnerable GraphQL queries
    all_users = graphene.List(UserType)
    user_by_id = graphene.Field(UserType, id=graphene.Int())
    
    all_challenges = graphene.List(ChallengeType)
    challenge_by_id = graphene.Field(ChallengeType, id=graphene.Int())
    
    all_categories = graphene.List(ChallengeCategoryType)
    all_difficulty_levels = graphene.List(DifficultyLevelType)
    
    # No authentication check - deliberately vulnerable
    def resolve_all_users(self, info):
        return User.objects.all()
    
    def resolve_user_by_id(self, info, id):
        return User.objects.get(pk=id)
    
    def resolve_all_challenges(self, info):
        return Challenge.objects.all()
    
    def resolve_challenge_by_id(self, info, id):
        return Challenge.objects.get(pk=id)
    
    def resolve_all_categories(self, info):
        return ChallengeCategory.objects.all()
    
    def resolve_all_difficulty_levels(self, info):
        return DifficultyLevel.objects.all()

class CreateUser(graphene.Mutation):
    """Create user mutation - deliberately vulnerable."""
    
    class Arguments:
        username = graphene.String(required=True)
        email = graphene.String(required=True)
        password = graphene.String(required=True)
    
    user = graphene.Field(UserType)
    
    def mutate(self, info, username, email, password):
        # No authentication or authorization check - deliberately vulnerable
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        return CreateUser(user=user)

class Mutation(graphene.ObjectType):
    """GraphQL mutations."""
    create_user = CreateUser.Field()
