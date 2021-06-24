
from rest_framework.serializers import IntegerField, CharField, Serializer, \
    ModelSerializer, HyperlinkedIdentityField, SerializerMethodField
from notes.models import Note
from accounts.models import User
from rest_framework.renderers import JSONRenderer
from django.contrib.auth import get_user_model



class NoteSimpleSerializer(Serializer):

    id = IntegerField(read_only=True)
    title = CharField(required=True, max_length=255)
    text = CharField(required=False, allow_blank=True) # allow_blank - тоже самое что и blank в моделе или форме
    #                                                     означает, что поле может быть пустым

    def create(self, validated_data):
        return Note.objects.create(**validated_data)

    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.text = validated_data.get('text', instance.text)
        instance.save()
        return instance





class UserSerializer(ModelSerializer):

    # url = HyperlinkedIdentityField(view_name='users')





    class Meta:
        # get_user_model - такая функция, которая позволяет получить instance юзера
        # она нужна, когда мы ссылаемся на кастомную модель юзера
        # Дальше в queryset сериалайзера мы используем model
        # get_user_model позволяет получить класс объекта экземпляра юзера (узнать его тип данных)
        # Получить модель экземпляром которой является юзер
        # собственно для этого эта функция и нужна
        # Все это нужно при использовании кастомного юзера
        model = get_user_model() # получаем доступ к модели юзера
        queryset = model.objects.all()
        fields = 'id', 'email', 'password', 'name', 'admin', #'url',
        extra_kwargs = {'password': {'write_only': True,},}


    def create(self, validated_data):
        password = validated_data.pop('password', '') # еще один способ захэшировать пароль first string
        user = self.Meta.model(**validated_data)
        user.set_password(password)                 # еще один способ захэшировать пароль second string
        # метод set_password модели User делает примерно так:
        # self.password = make_password(password)
        # но как выше строчкой, скорее всего нельзя
        user.save()
        return user


    def update(self, instance, validated_data):
        instance.set_password(validated_data.pop('password', ''))
        return super().update(instance, validated_data)



class ThinUserSerializers(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='accounts-detail')

    class Meta:

        model = User
        fields = 'email', 'is_active', 'url',




class NoteSerializer(ModelSerializer):

    author = SerializerMethodField(read_only=True)

    def get_author(self, obj):
        return str(obj.author.pk) #obj.author.email

    # get_author работает здесь в связке с SerializerMethodField.
    # синтаксис следующий get_<name_field_in_db>, т.е. к get_добавдяем имя, которое мы хотим использовать как поле
    # благодаря SerializerMethodField мы делаем это поле только для чтения.
    # А благодаря get_author - выбираем то выводить в json файле в поле author
    # Но в данном случае они работают только в связке, по одному не могут (почему - не знаю)
    # Запомни эту связку - очень полезная штука.

    class Meta:
        model = Note
        fields =  'id', 'title', 'text', 'created', 'updated', 'author', #'__all__'



class ThinNoteSerializer(ModelSerializer):

    url = HyperlinkedIdentityField(view_name='notes-detail') # view_name - это pathname
    class Meta:
        model = Note
        fields = 'id', 'title', 'url',






# HyperlinkedIdentityField - позволяет сделать запись url. Для этого нужно в этот класс
# передать pathname. В именованный аргумент view_name (почему view_name не знаю)
# и дальше добавить эту переменную в тапл fields в метаклассе.
# Но чтобы все работало, нужно будет в наш сериалайзер, при создании объекта,
# передать context, где ключ и значение должны быть request.
# Вспомни, что при определении метода get_absolute_url никаких request в контекст нигде передавать не надо
# django сам найдет этот request. Но в DRF в serializer надо, и это посути костыль.
# HyperlinkedIdentityField - поле для определения гиперссылки.


# пользователи при доступе к API стучатся в django по какому-то определенному url.
# доступ к API может запрашивать браузер, мобильное приложение, другой сайт (возможно через парсинг).
# Важно, в ответ вместо html страницы ожидается json или xml файл. Сооветсвенно с какими-то данными,
# из бд, обработанными в обработчике.
# Если такой файл не обнаруживается, ожидается не просто html страница 404,
# а status 404 (я так понимаю в http ответе, но это не точно)
# разрешенные методы http запроса, и вообще сам по себе http запрос - краеугольный камень API
# Самая главная фишка обработчика для api - обработчик должен вернуть json или xml файл.
# И чтобы json или xml получить - создается прослойка как serializer
# (см. схемы цикла mvc паттерна, и api на телефоне фото)
# Сериалайзер позволяет преобразовывать данные из json в объекты python,
# чтобы их можно было записывать в бд (через orm)
# И в обратную сторону - те данные, что приходят из бд, сериалайзер приобразовывает из объектов python или django
# в данные с форматом json, отдает в котроллер, и данные идут дальше тому приложению, которое их запрашивало.
# Помни, котнтроллер работает опираясь не только на адрес, но и на метод по котрому пришли данные.
# И вроде как по такому принципу строится работа web api, написанная не только на django, но и на flask,
# и даже приложениях, написанных на других языках.
# !!! В общем повтори урок 10, он очень полезен !!!

# Общение клиента с api происходит через http методы, и http заголовки

# Важно помнить, что пользователь не только, при использовании api, получает данные в формате json,
# но и отправляет их с post запросом тожет в формате json. И изменяет кстати тоже.
# Работа с сериализаторами очень похожа на работу с формами