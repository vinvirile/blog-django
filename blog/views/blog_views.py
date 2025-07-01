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

            # return a table of all the fields in a HttpResponse

            # Create HTML table to display form field values
            # table_html = f"""
            # <table border="1" style="border-collapse: collapse; width: 100%;">
            #     <tr><th style="padding: 8px;">Field</th><th style="padding: 8px;">Value</th></tr>
            #     <tr><td style="padding: 8px;">Title</td><td style="padding: 8px;">{title}</td></tr>
            #     <tr><td style="padding: 8px;">Category</td><td style="padding: 8px;">{category}</td></tr>
            #     <tr><td style="padding: 8px;">Excerpt</td><td style="padding: 8px;">{excerpt}</td></tr>
            #     <tr><td style="padding: 8px;">Image URL</td><td style="padding: 8px;">{image_url}</td></tr>
            #     <tr><td style="padding: 8px;">Blog Content</td><td style="padding: 8px;">{blog_content}</td></tr>
            #     <tr><td style="padding: 8px;">Tags</td><td style="padding: 8px;">{tags}</td></tr>
            #     <tr><td style="padding: 8px;">Status</td><td style="padding: 8px;">{status}</td></tr>
            # </table>
            # """

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

    form = CreateBlogForm()
    return render(request, 'create-blog.html', {'user': grab_user_content(request), 'form': form})

def view_blog(request):
    if request.method == 'GET':
        eid = request.GET.get('id')
        blog = Blogs.objects.get(eid=eid)
        blog.author = Members.objects.get(eid=blog.author_eid)
        return render(request, 'blog.html', {'user': grab_user_content(request), 'blog': blog})
    return render(request, 'demo-blog.html', {'user': grab_user_content(request)})