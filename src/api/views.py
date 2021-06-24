# from rest_framework.urls import urlpatterns
from django.shortcuts import render
from django.http import Http404
from django.views.generic import View
from django.contrib.auth import get_user_model
from rest_framework.generics import get_object_or_404, GenericAPIView, ListAPIView, CreateAPIView,\
    ListCreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.response import Response
from rest_framework.renderers import JSONRenderer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.mixins import ListModelMixin, CreateModelMixin, \
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin
from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import BasicAuthentication
from notes.models import Note
from accounts.models import User
from .serializers import NoteSerializer, ThinNoteSerializer, UserSerializer, ThinUserSerializers
from api.permissions import IsAuthorOrReadOnly
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404 as g_o_o_404, render



import requests


# обработчики функции
# ----------------------------------------------------------------------------------------
# декораторы для функций контроллеров предназначенных для api
# строго обязательны
# а именнованный аргумент format (None по умоланию) нужен для отображения через базовую страницу
# для api (скорее всего это связано напрямую с format_suffix_patterns из urls)

@api_view(['GET', 'POST',])
def notes_list(request, format=None):
    if request.method == 'GET':
        notes = Note.objects.all()
        serializer = NoteSerializer(notes, many=True)


        # ------------
        print('\n\n',
              *dir(request),
              '\n\n',sep='\n')
        # ------------

        return Response(serializer.data, status=status.HTTP_200_OK)
    # кстати, насчет работы Response и Serializer. Проверь в shell, какой тип данных вернет
    # serializer.data. Это будет OrderedDict (поправка, ReturnList, состоящий из объектов OrderedDict).
    # Таким образом функция Response не только рэндерит
    # инфу на отдельную страницу, но и приобразует данные в json (последнее неточно, преобразовывать может что-то другое)
    # Посмотри как выглядит начинка Response. Там есть именнованный аргумент template_name.
    # Отсюда следует, что мы можем рендерить наш json файл и на свою страницу.

    elif request.method == 'POST':
        data = request.data
        serializer = NoteSerializer(data=data)  # при post запросе (да и при put)
        # когда мы кладем в сериалайзер ин-фу, мы должны передавать ее в именованный аргумент data
        # иначе он передастася в аргумент instance
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return Response({'error': 'not allowed method'})

# Обрати внимание, статусы отправляются через Response. Сами статусы импортируются из rest_framework
# Общение происходит через статусы и методы http в api.




@api_view(['GET', 'PUT', 'DELETE',])
def note_detail(request, pk, format=None):

    # note = get_object_or_404(Note, pk=pk)
    # функция get_object_or_404 заменяет конструкцию ниже
    try:
        note = Note.objects.get(pk=pk)
    # except Note.objects.all().model.DoesNotExist:
    #     raise Http404('Note does not exist')
    except Note.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)
    # обрати внимание, что можно передавать в Response просто статус ответа (http статус).



    if request.method == 'GET':
        serializer = NoteSerializer(note)
        data = serializer.data

        return Response(data, status=status.HTTP_200_OK)

    elif request.method == 'PUT':
        # -- не мой вариант
        serializer = NoteSerializer(note, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'success': f'{note.title} was updated successfully'}, status=status.HTTP_201_CREATED)
        return Response(status=status.HTTP_400_BAD_REQUEST)

        # -- мой вариант |/
        # note.title = request.data.get('title', note.title)
        # note.text = request.data.get('text', note.text)
        # note.save()
        # return Response({'success': f'{note.title} was updated successfully'}, status=status.HTTP_200_OK)

    elif request.method == 'DELETE':
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
# --------------------------------------------------------------------------------------------


class NotesListView(APIView):

    def get(self, request, format=None):
        notes = Note.objects.all()
        context = {'request': request,}
        # Зачем мы создаем здесь переменную context с request в словаре?
        # И передаем ее в сериалайзер?
        # По сути это костыль. В обычном django у request есть какой-то свой контекст (по всей видимости)
        # И доступен этот контекст в любом месте где бы мы не работали.
        # Но в rest-framework чтобы достучаться к request внутри сериалайзера
        # (поправка, внутри модели сериалайзера)
        # этот request нужно передать внутри переменной context.
        # И это все делается для того, чтобы можно было отображать url в записях к записям, ша.
        # Обрати внимание, что нам необходимо передавать так request, после того,
        # как мы использовали функцию HyperlinkedIdentityField, куда в аргумент name_view
        # передали name path. До этого нам наш request передавать не нужно было.
        # С помощью этой функции drf формирует url к нашей записи в json. Для этого и нужен там request.
        # чем-то отдаленно напоминает get_absolute_url
        serializer = ThinNoteSerializer(notes, many=True, context=context)


        print(f'\n\n'
              f'{serializer.data}'
            f'\n\n')


        # # как сделать, чтобы в json записи конкретного объекта был указан url
        # # можно это сделать, как сделал я:
        # # а можно см. в serializers.py
        # for note in serializer.data:
        #     id = note['id']
        #     note['url'] = 'http://127.0.0.1:8000/api/notes/' + str(id) + '/'
        # # а можно см. в serializers.py

        return Response(serializer.data)

    def post(self, request, format=None):
        note = request.data
        serializer = NoteSerializer(data=note)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response({'Success': f'{serializer.data["title"]} was successfully added'}, status=status.HTTP_200_OK)
        return Response('WhataFuck - MazaFuck', status=status.HTTP_400_BAD_REQUEST)





class NoteDetailView(APIView):


    def get(self, request, pk, format=None):
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(note)
        return Response(serializer.data)


    def put(self, request, pk, format=None):
        note = get_object_or_404(Note, pk=pk)
        serializer = NoteSerializer(instance=note, data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data)
        return Response(status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, pk, format=None):
        note = get_object_or_404(Note, pk=pk)
        note.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


# -------------------------------------------------------------------------------------
# Обработчики с помощью миксинов

class NotesListViewMixin(ListModelMixin, CreateModelMixin, GenericAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        self.serializer_class = ThinNoteSerializer
        return self.list(request, *args, **kwargs)

    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)




class NoteDetailViewMixin(RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    def get(self, request, *args, **kwargs):
        return self.retrieve(request, *args, **kwargs)

    def put(self, request, *args, **kwargs):
        return self.update(request, *args, **kwargs)

    def delete(self, request, *args, **kwargs):
        return self.destroy(request, *args, **kwargs)


# ------------------------------------------------------------------------------------------------
# Наиболее краткие обработчики заимствующиеся от generic, с полным функционалом CRUD, ша

class NotesListAPIView(ListCreateAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer

    # # мой вар-т. Но так мы переопределяем весь get
    # def get(self, request, *args, **kwargs):
    #     self.serializer_class = ThinNoteSerializer
    #     return super().get(request, *args, **kwargs)

    # # частично не мой вар-т. Так мы переопреляем только элемент функционала CRUD
    # def list(self, request, *args, **kwargs):
    #     self.serializer_class = ThinNoteSerializer
    #     return super().list(request, *args, **kwargs)

    # полностью не мой вар-т. С одной стороны получилось более громоздко, с другой
    # из-за того, что мы не меняем на serializer_class, мы здесь можем посылать нормальные post запросы
    # (раньше при get запросе менялся serializer_class и для формы post запросов
    # использовался ThinNotesSerializer)
    # Наш serializer_class мы здесь не меняем а просто запихиваем наш queryset в отдельный сериалайзер,
    # который преобразует инфу из бд в OrderDict объект, а с помощью Response этот объект
    # уже преобразуется в json объект.
    def list(self, request, *args, **kwargs):
        notes = Note.objects.all()
        context = {'request': request,}
        serializer = ThinNoteSerializer(notes, many=True, context=context)

        print(f'\n\n###################################\n'
              f'dir(Note) \n {dir(Note)}\n\n'
              f'dir(Note.objects) \n {dir(Note.objects)}'
              f'\n####################################\n\n')
        return Response(serializer.data, status=status.HTTP_200_OK)



class NoteDetailAPIView(RetrieveUpdateDestroyAPIView):

    queryset = Note.objects.all()
    serializer_class = NoteSerializer


# Это наиболее краткие классы APIView. Эти классы уже заимсвуются от нужных миксинов,
# и там уже реализованы методы list, create, retrieve, update, destroy.
# В принципе ничего не мешает переопределять эти методы, как я это сделал в NotesListAPIView.
# Есть миксины, которые работают только в связке с GenericAPIView.
# (Поправка, ВСЕ миксины в DRF работают в связке с GenericAPIView)
# Эти классы наследуются от миксинов, и GenericAPIView.
# В общем, посмотри посмотри generics.py и mixins.py


# Тут есть некоторое неудобство в том, то мы определяем два класса
# ModelViewSet заимствуется от List, Create, Retrieve, Update, Destroy ModelMixin
# И от GenericViewSet, который имеет свою иерархию и наследуется от ViewSetMixin (базовый класс для viewset)
# и GenericAPIView. В общем загляни в файл viewsets.py
# Итак



class NoteCRUDModelViewSet(ModelViewSet):

    model = Note
    queryset = model.objects.none()
    serializer_class = NoteSerializer
    # здесь используется мой permission. Смотри permissions.py в приложении api
    # и вспоминай.
    permission_classes = (IsAuthorOrReadOnly,) #(IsAuthenticatedOrReadOnly,)
    http_method_names = 'get', 'post', 'put', 'patch', 'delete', 'head', 'options', 'trace',
    # http_method_names - аттрибут, который показывает, какие http методы доступны будут,
    # для этого контроллера. Аттрибут не обязательный.
    # Необязательный, потому что он уже определен в базовом Views
    # (django.views.generic, оттуда base.py), т.е. он не от DRF а от Django
    # http методы записываются в листе строчными буквами (не большими, это важно).
    # удобно кстати.



    def get_serializer_class(self):
        """Если нам нужно переопределить сериалайзер для определенного метода, или действия (CRUD)
        необязательно переопределять http method или action
        можно переопределить сериалайзер. А как узнать в какой момент его переопределять?
        для этого есть потрясающий аттрибут экземпляра - action
        Но он есть точно во VieSet, в других местах не факт что он есть"""
        if self.action == 'list':
            return ThinNoteSerializer
        return NoteSerializer


    def get_queryset(self):
        user = self.request.user
        if user.admin:
            return self.model.objects.all()
        return self.model.objects.filter(author=user)



    # def list(self, request, *args, **kwargs):
    #     context = {'request': request,}
    #     queryset = self.queryset
    #     # queryset = self.queryset.filter(author=request.user.id)
    #     serializer = ThinNoteSerializer(queryset, many=True, context=context)
    #     return Response(serializer.data, status=status.HTTP_200_OK)

    # благодаря perform_create мы подвязываем запись к определенному автору (в таблице User)
    # можем вручную привязывать(достать автора из бд), а можем через request

    # Первоначально perform_create определен в CreateModelMixin
    # обрати внимание на то, что способ сохранения в DRF отличается от Django
    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

# Правда, здесь есть свои нюансы для отображения в urls.py (Загляни туда)
# там мы должны вруную утанавливать соответствие между методами HTTP и действиями нашего котроллера
# в методе as_view()
# Кстати, обрати внимание на метода patch, и какое действие ему соответсвует (какой метод в mixins)
# метода - partial_update() (посмотри на него в mixins.py). HTTP method patch - делвет частичное обновление
# отсюда и действие partial update. Но вообще http метод patch - считается редким.


c



