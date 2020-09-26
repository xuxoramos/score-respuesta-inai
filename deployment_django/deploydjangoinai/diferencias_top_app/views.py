from django.shortcuts import render

# Create your views here.
def index(request):
    return render(request, 'index.html')


def diferencias_top_app(request):
    return render(request, 'index.html')