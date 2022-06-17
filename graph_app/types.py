import graphene
from django.contrib.auth import get_user_model

from graphene_django import DjangoObjectType
from .models import Car, Make, Model


# создаем классы наших типов, наследуемых от DjangoObjectType
class MakeType(DjangoObjectType):
    class Meta:
        # указываем модель и поля модели
        model = Make
        fields = ("id", "name")     # можно не указывать, если используются все поля
        # фильтр для поиска не только по id, но и по заданным полям
        # filter_fields = ('name', 'id')
        filter_fields = {'name': ['exact', 'icontains', 'istartswith']}
        interfaces = (graphene.relay.Node,)


class ModelType(DjangoObjectType):
    class Meta:
        model = Model
        fields = ("id", "name")


class CarType(DjangoObjectType):
    class Meta:
        model = Car
        fields = ("id", "license_plate", "make", "model")


class UserType(DjangoObjectType):
    class Meta:
        model = get_user_model()
