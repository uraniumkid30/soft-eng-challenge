import graphene

from applications.account.schema import UserGrapheneQuery


graphene_querires = [
    UserGrapheneQuery,
]
graphene_mutations = []


class Query(*graphene_querires, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)  # , mutation=Mutation)
