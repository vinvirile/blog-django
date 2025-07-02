from django.shortcuts import render, redirect
from django.http import HttpResponse
from ..forms import CreateBlogForm
from ..models import Members, Blogs
from .utils import grab_user_content, hash_string
import datetime

def create_blog(request):
    # check if user logged in
    if not request.session.get('eid'):
        return redirect('../login')

    eid = request.GET.get('id') or ''
    blog_values = None
    is_editing = False

    if eid:
        try:
            blog_values = Blogs.objects.get(eid=eid)
            if blog_values.author_eid != request.session.get('eid'):
                return redirect('../')
            is_editing = True
        except Blogs.DoesNotExist:
            return redirect('../')

    if request.method == 'POST':
        form = CreateBlogForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            category = form.cleaned_data['category']
            excerpt = form.cleaned_data['excerpt']
            image_url = form.cleaned_data['image_url']
            blog_content = form.cleaned_data['blog_content']
            tags = form.cleaned_data['hidden_tags']
            status = form.cleaned_data['status']

            if status == True:
                status = 'published'
            else:
                status = 'draft'

            if is_editing:
                # Update existing blog
                blog_values.title = title
                blog_values.category = category
                blog_values.excerpt = excerpt
                blog_values.image_url = image_url
                blog_values.blog_content = blog_content
                blog_values.tags = tags
                blog_values.status = status
                blog_values.save()
                return redirect('../blog?id='+blog_values.eid)
            else:
                # Create new blog
                blog = Blogs(
                    author_eid=request.session.get('eid'),
                    eid=hash_string(title+category+tags+str(datetime.datetime.now())),
                    title=title,
                    category=category,
                    excerpt=excerpt,
                    image_url=image_url,
                    blog_content=blog_content,
                    tags=tags,
                    status=status
                )
                blog.save()
                return redirect('../blog?id='+blog.eid)

        return HttpResponse('Something went wrong')

    # Initialize form with existing data if editing
    if is_editing:
        initial_data = {
            'title': blog_values.title,
            'category': blog_values.category,
            'excerpt': blog_values.excerpt,
            'image_url': blog_values.image_url,
            'blog_content': blog_values.blog_content,
            'hidden_tags': blog_values.tags,
            'status': blog_values.status == 'published'
        }
        form = CreateBlogForm(initial=initial_data)
    else:
        form = CreateBlogForm()

    return render(request, 'create-blog.html', {
        'user': grab_user_content(request), 
        'form': form, 
        'blog_values': blog_values,
        'is_editing': is_editing
    })


def view_blog(request):
    if request.method == 'GET':
        eid = request.GET.get('id')
        blog = Blogs.objects.get(eid=eid)
        blog.author = Members.objects.get(eid=blog.author_eid)
        
        # Check if the current user is the author of this blog
        user_eid = request.session.get('eid')
        is_author = user_eid == blog.author_eid if user_eid else False
        
        return render(request, 'blog.html', {
            'user': grab_user_content(request), 
            'blog': blog,
            'is_author': is_author
        })
    return render(request, 'demo-blog.html', {'user': grab_user_content(request)})