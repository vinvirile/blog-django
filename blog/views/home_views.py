from django.shortcuts import render
from .utils import grab_user_content, grab_blogs

def index(request):
    blogs = grab_blogs()
    published_vlogs = []
    drafted_vlogs = []
    for blog in blogs:
        if blog.status == 'published':
            published_vlogs.append(blog)
        else:
            if blog.status == 'draft':
                if request.session.get('eid') == blog.author_eid:
                    drafted_vlogs.append(blog)
    published_vlogs = published_vlogs[::-1]
    return render(request, 'index.html', {'user': grab_user_content(request), 'blogs': published_vlogs, 'drafts': drafted_vlogs})
