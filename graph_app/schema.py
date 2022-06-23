import graphene
from graphene_django import DjangoObjectType

from django.contrib.auth import get_user_model
from graphene_django.filter import DjangoFilterConnectionField      # при использовании фильтров

# создаем типы для наших моделей, для этого импортируем модели
from .models import Car, Make, Model
from .types import CarType, MakeType, ModelType, UserType


# создаем класс запросов (можно вынести в отдельный файл)
class Query(graphene.ObjectType):

    # make = graphene.Field(MakeType, id=graphene.Int())
    # makes = graphene.List(MakeType)     # получить всех производителей

    # для использования фильтров меняем вышеуказанные переменные make и makes
    # make = graphene.relay.Node.Field(MakeType, id=graphene.Int()) # показывает ошибку с id
    make = graphene.relay.Node.Field(MakeType)
    makes = DjangoFilterConnectionField(MakeType)


    model = graphene.Field(ModelType, id=graphene.Int())

    car = graphene.Field(CarType, id=graphene.Int())
    cars = graphene.List(CarType)       # получить все описания машин

    # api_client = graphene.Field(UserType)
    # api_clients = graphene.List(UserType)

    # добавляем распознаватели
    def resolve_make(self, info, **kwargs):
        id = kwargs.get('id', None)

        try:
            return Make.objects.get(id=id)
        except Make.DoesNotExist:
            return None

    def resolve_model(self, info, **kwargs):
        id = kwargs.get('id', None)

        try:
            # возвращаем ответ в соответствии с id, полученным из kwargs
            return Model.objects.get(id=id)
        except Model.DoesNotExist:
            return None

    def resolve_car(self, info, **kwargs):
        id = kwargs.get('id', None)

        try:
            return Car.objects.get(id=id)
        except Car.DoesNotExist:
            return None

    def resolve_makes(self, info, **kwargs):
        return Make.objects.all()

    def resolve_cars(self, info, **kwargs):
        return Car.objects.all()

#     def resolve_api_client(self, info):
#         user = info.context.user
#
#         if user.is_anonymous:
#             raise Exception('Authentication Failure: Your must be signed in')
#         return user
#
#     def resolve_api_clients(self, info):
#         user = info.context.user
#
#         if user.is_anonymous:
#             raise Exception('Authentication Failure: Your must be signed in')
#         if not user.is_staff:
#             raise Exception('Authentication Failure: Must be Manager')
#         return get_user_model().objects.all()


# подключаемся к главной схеме
# scheme = graphene.Schema(query=Query)