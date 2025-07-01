import string
from django.shortcuts import render
from .forms import LoginForm, RegisterForm, CreateBlogForm
from django.http import HttpResponse
from django.contrib.auth.hashers import make_password, check_password
from .models import Members, Blogs
from django.shortcuts import redirect
import datetime

def grab_user_content(request):
    if request.session.get('eid'):
        return Members.objects.get(eid=request.session.get('eid'))
    return None

# Create your views here.
def index(request):
    return render(request, 'index.html', {'user': grab_user_content(request)})

def hash_string(text):
                """Create custom hash with random letters and numbers"""
                # Use built-in hash for consistency, then convert to alphanumeric
                hash_int = hash(text)
                
                # Convert to positive number and create alphanumeric string
                hash_abs = abs(hash_int)
                chars = string.ascii_letters + string.digits
                result = ""
                
                # Convert number to base-62 (letters + digits)
                while hash_abs > 0:
                    result = chars[hash_abs % 62] + result
                    hash_abs //= 62
                
                return result[:16]  # Limit to 16 characters

def login(request):

    # if logged in already send to index
    if request.session.get('eid'):
        return redirect('index')


    if request.method == 'POST':
        error = 'Something went wrong'
        form = LoginForm(request.POST)
        if form.is_valid():
            identifier = form.cleaned_data['identifier']
            password = form.cleaned_data['password']

            # check if user exists
            if not Members.objects.filter(username=identifier).exists() and not Members.objects.filter(email=identifier).exists():
                error = 'Username or email does not exist'
                return render(request, 'login.html', {'error': error, 'form': form})

            user = Members.objects.filter(username=identifier).first() or Members.objects.filter(email=identifier).first()

            if not check_password(password, user.password):
                error = 'Password is incorrect'
                return render(request, 'login.html', {'error': error, 'form': form})
            
            # login user
            request.session['eid'] = user.eid
            

            return redirect('../?login=successful')

    return render(request, 'login.html', {'form': LoginForm()})

def register(request):

    # if logged in already send to index
    if request.session.get('eid'):
        return redirect('index')

    if request.method == 'POST':
        error = 'Something went wrong. Please try again.'
        form = RegisterForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            confirm_password = form.cleaned_data['confirm_password']

            # check if passwords match
            if password != confirm_password:
                error = 'Passwords do not match'
                return render(request, 'register.html', {'error': error, 'form': form})
            
            # check if passwords are less than 8 characters
            if len(password) < 8:
                error = 'Password must be at least 8 characters'
                return render(request, 'register.html', {'error': error, 'form': form})
            
            # encrypts password
            encrypted_password = make_password(password)

            # check if user already exist
            if Members.objects.filter(username=username).exists():
                error = 'Username already exists'
                return render(request, 'register.html', {'error': error, 'form': form})
            
            # check if email already exist
            if Members.objects.filter(email=email).exists():
                error = 'Email already exists'
                return render(request, 'register.html', {'error': error, 'form': form})

            # no spaces in username
            if ' ' in username:
                error = 'Username cannot contain spaces'
                return render(request, 'register.html', {'error': error, 'form': form})
                
            # no spaces in email
            if ' ' in email:
                error = 'Email cannot contain spaces'
                return render(request, 'register.html', {'error': error, 'form': form})
            
            # create a function that checks if a symbol is used in a string
            def contains_symbol(string):
                symbols = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '-', '_', '+', '=', '[', ']', '{', '}', '|', '\\', ':', ';', '"', '\'', ',', '<', '>', '.', '?', '/']
                for symbol in symbols:
                    if symbol in string:
                        return True
                return False

            # no symbols in username
            if contains_symbol(username):
                error = 'Username cannot contain symbols'
                return render(request, 'register.html', {'error': error, 'form': form})
            
            
            # grab the current date
            date = datetime.datetime.now()

            

            # create user
            members = Members(
                username=username,
                email=email,
                password=encrypted_password,
                eid=hash_string(username+email+str(date))
            )
            members.save()
            # redirect to ./login
            return redirect('../login?reg=success')

    return render(request, 'register.html', {'form': RegisterForm()})

def logout(request):
    # logout user
    del request.session['eid']
    return redirect('../login?logout=success')

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

def page_not_found_view(request, exception):
    return render(request, '404.html', status=404)