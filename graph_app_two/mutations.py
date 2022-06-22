import graphene
from django.contrib.auth import get_user_model
# from graphql_jwt.shortcuts import create_refresh_token, get_token

from graph_app.types import MakeType, UserType
from graph_app.models import Make


class MakeInput(graphene.InputObjectType):
    # поля, которые пользователь будет вводить (здесь – name)
    id = graphene.ID()
    name = graphene.String()


# создание мутации
class CreateMake(graphene.Mutation):
    class Arguments:
        # записываются аргументы, которые нужны для разрешения мутации
        input = MakeInput(required=True)

    # поля вывода мутации, когда она разрешена
    ok = graphene.Boolean()
    make = graphene.Field(MakeType)

    # обязательный метод, который будет применен после вызова мутации.
    # Этот метод — всего лишь специальный преобразователь, в котором мы можем изменять данные.
    # Он принимает те же аргументы, что и стандартный запрос Resolver Parameters.
    # @classmethod
    def mutate(self, info, input=None):
        ok = True
        # создаем объект
        make_instance = Make.objects.create(name=input)
        # возвращаем этот же объект класса CreateMake
        return CreateMake(ok=ok, make=make_instance)


# мутация для изменения объекта (копируем CreateMake и вносим изменения)
class UpdateMake(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)    # добавляем поле id (нужно знать изменяемый элемент)
        input = MakeInput(required=True)

    ok = graphene.Boolean()
    make = graphene.Field(MakeType)

    @classmethod
    def mutate(cls, root, info, id, input=None):  # добавляем поле id
        ok = False                          # меняем по умолчанию на False
        try:                                # добавляем на случай, если не получим id
            make_instance = Make.objects.get(pk=id)  # получаем объект по id
        except Make.DoesNotExist:
            return cls(ok=ok, make=None)

        ok = True
        make_instance.name = input.name     # меняем значение поля на input.name
        make_instance.save()                # сохраняем новое значение
        return cls(ok=ok, make=make_instance)


# мутация для изменения объекта (копируем CreateMake и вносим изменения)
class DeleteMake(graphene.Mutation):
    class Arguments:
        id = graphene.Int(required=True)

    ok = graphene.Boolean()

    @classmethod
    def mutate(cls, root, info, id):
        try:
            make_instance = Make.objects.get(pk=id)
            make_instance.delete()
            return cls(ok=True)
        except Make.DoesNotExist:
            return cls(ok=True)


# class CreateUser(graphene.Mutation):
#     user = graphene.Field(UserType)
#     token = graphene.String()
#     refresh_token = graphene.String()
#
#     class Arguments:
#         password = graphene.String(required=True)
#         email = graphene.String(required=True)
#
#     def mutate(self, info, password, email):
#         user = get_user_model()(
#             email=email,
#         )
#         user.set_password(password)
#         user.save()

        # token = get_token(user)
        # refresh_token = create_refresh_token(user)

        # return CreateUser(user=user, token=token, refresh_token=refresh_token)


class Mutation(graphene.ObjectType):
    # подключаем название, указываем мутации
    create_make = CreateMake.Field()
    update_make = UpdateMake.Field()
    delete_make = DeleteMake.Field()
    # create_user = CreateUser.Field()
