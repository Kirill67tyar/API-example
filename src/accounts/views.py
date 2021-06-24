from django.shortcuts import render, HttpResponse
import random
import string

def controller(request):
    st = ''.join([random.choice(string.printable[:62]) for i in range(15)])
    return HttpResponse('<h1>{}</h1><br><br><hr>{}'.format(st, string.printable))

