import graphene
from graphene import relay
from models import Question as QuestionModel
from graphene_pynamodb import PynamoObjectType, PynamoConnectionField


class Question(PynamoObjectType):
    class Meta:
        model = QuestionModel
        interfaces = (graphene.Node,)


class Query(graphene.ObjectType):
    questions = graphene.List(Question, description='A typical question')

    def resolve_questions(self, args, context, info):
        return list(QuestionModel.scan())

schema = graphene.Schema(query=Query, types=[Question])
