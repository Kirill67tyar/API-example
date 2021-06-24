from django.urls import path
from .views import example, ExampleAPIView

app_name = 'notes'

urlpatterns = [
    path('example/', example, name='example'),
    path('example2/', ExampleAPIView.as_view(), name='example2'),


]


