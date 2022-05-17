import graphene

from applications.account.schema import UserGrapheneQuery
from applications.ship.schema import ShipGrapheneQuery, MotherShipGrapheneQuery


graphene_querires = [
    UserGrapheneQuery,
    ShipGrapheneQuery,
    MotherShipGrapheneQuery,
]
graphene_mutations = []


class Query(*graphene_querires, graphene.ObjectType):
    pass


class Mutation(graphene.ObjectType):
    pass


schema = graphene.Schema(query=Query)
