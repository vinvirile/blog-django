import string
from ..models import Members, Blogs

def grab_user_content(request):
    if request.session.get('eid'):
        return Members.objects.get(eid=request.session.get('eid'))
    return None

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

def grab_blogs():
    blogs = Blogs.objects.all()

    blogs_with_authors = []

    # adds author's username to blog
    for blog in blogs:
        blog.author = Members.objects.get(eid=blog.author_eid).username
        blogs_with_authors.append(blog)

    return blogs_with_authors

def grab_blog(eid):
    return Blogs.objects.get(eid=eid)