from django.shortcuts import render
from .utils import grab_user_content, grab_blogs

def index(request):
    return render(request, 'index.html', {'user': grab_user_content(request), 'blogs': grab_blogs()})
