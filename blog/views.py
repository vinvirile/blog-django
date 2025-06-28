from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def index(request):
    return render(request, 'index.html')

def login(request):
    return render(request, 'login.html')

def register(request):
    return render(request, 'register.html')

def create_blog(request):
    return render(request, 'create-blog.html')

def view_blog(request):
    return render(request, 'blog.html')

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)