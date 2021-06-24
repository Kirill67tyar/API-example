from django.shortcuts import render, HttpResponse
from django.views import View
from django.views.generic import ListView
from rest_framework.viewsets import ModelViewSet
from rest_framework.views import APIView
from notes.models import Note
from api.serializers import NoteSerializer

class V(ListView):
    pass

def example(request):
    r = request.GET.get('s', None)
    context = {'r': r}

    print(f'\n\n##########################\n'
          f'request.GET - {request.GET}\n'
          f'request.GET.get("s", None) - {request.GET.get("s", None)}\n'
          f'###############################\n\n')
    return render(request=request, template_name='notes/example.html', context=context)



class ExampleAPIView(APIView):
    # queryset = Note.objects.all()
    # serializer_class = NoteSerializer
    """
        доказательство того, что query_params работает как GET
        request.GET.get() == request.query_params.get() (тот же самый QueryDict)
        но query_params есть только в APIView (в View Django я его не нашел)
    """

    def get(self, request, *args, **kwargs):
        r = request.query_params.get('s', None)
        print(f'\n\n ########################\n'
              f'request.query_params - {request.query_params}'
              f'\n###############################\n\n')
        context = {'r': r}
        return render(request=request, template_name='notes/example.html', context=context)


