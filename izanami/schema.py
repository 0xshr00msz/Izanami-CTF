"""
GraphQL schema for izanami project.
"""

import graphene
from challenges.schema import Query as ChallengesQuery
from challenges.schema import Mutation as ChallengesMutation

class Query(ChallengesQuery, graphene.ObjectType):
    pass

class Mutation(ChallengesMutation, graphene.ObjectType):
    pass

schema = graphene.Schema(query=Query, mutation=Mutation)
