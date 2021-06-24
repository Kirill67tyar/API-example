from django.urls import path
from api.views import (notes_list, note_detail,
    NotesListView, NoteDetailView,
    NotesListViewMixin, NoteDetailViewMixin,
    NotesListAPIView, NoteDetailAPIView,
    NoteCRUDModelViewSet,
    UserViewSet)
from rest_framework.urlpatterns import format_suffix_patterns
from rest_framework.routers import DefaultRouter



# 1 --------------------------------------------------------------------------------
# Наиболее краткий способ записать urlpatterns (мне не понравилось)
router = DefaultRouter()
router.register('notes', NoteCRUDModelViewSet, basename='notes')
router.register('users', UserViewSet, basename='users')
urlpatterns = router.urls
# ---------------------------------------------------------------------------------

#                                  OR

# 2 ===============================================================================
# # Mapper который делает соответствие между методами HTTP и действиями viewset (используется для ViewSet)
# for_many_elements = {
#     'get': 'list',
#     'post': 'create',
# }
#
# for_one_element = {
#     'get': 'retrieve',
#     'put': 'update',
#     'patch': 'partial_update',
#     'delete': 'destroy',
# }
#
# urlpatterns = [
#     ## url пути для функций
#     # path('notes/', notes_list, name='notes-list'),
#     # path('notes/<int:pk>/', note_detail, name='notes-detail'),
#
#     ## url пути для class based view - APIView
#     # path('notes/', NotesListView.as_view(), name='notes-list'),
#     # path('notes/<int:pk>/', NoteDetailView.as_view(), name='notes-detail'),
#
#     ## url пути для миксинов, и generic (базовые)
#     # path('notes/', NotesListViewMixin.as_view(), name='notes-list'),
#     # path('notes/<int:pk>/', NoteDetailViewMixin.as_view(), name='notes-detail'),
#
#
#     ## url пути для APIView из дженериков, но с полным функционалом, заимствованным от миксинов
#     # path('notes/', NotesListAPIView.as_view(), name='notes-list'),
#     # path('notes/<int:pk>/', NoteDetailAPIView.as_view(), name='notes-detail'),
#
#
#     ## url для ModelViewSet (rest_framework.viewsets)
#     path('notes/', NoteCRUDModelViewSet.as_view(for_many_elements), name='notes-list'),
#     path('notes/<int:pk>/', NoteCRUDModelViewSet.as_view(for_one_element), name='notes-detail'),
#
#     path('accounts/', UsersListAPIView.as_view(), name='accounts-list'),
#     path('accounts/<int:pk>', UserDetailAPIView.as_view(), name='accounts-detail'),
#
#
# ]
#
# # Не забывай, что аргумент name в функции path нужен для того, чтобы мы могли обратиться к
# # этому url из других мест программы. Вспоминай reverse, reverse_lazy
#
# # это если нам надо, чтобы апишка отображалась не через базовую страницу для api
# # а как-то подругому
# urlpatterns = format_suffix_patterns(urlpatterns)
# ======================================================================================================
