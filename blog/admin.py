from django.contrib import admin
from .models import Members, Blogs

class MembersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at') # Add 'created_at' to the list display
    readonly_fields = ('created_at',) # Make 'created_at' read-only

class BlogsAdmin(admin.ModelAdmin):
    list_display = ('id', 'author_eid', 'title', 'created_at', 'updated_at', 'read_time', 'tags', 'status') # Add 'created_at' to the list display
    readonly_fields = ('created_at', 'updated_at') # Make 'created_at' read-only

admin.site.register(Blogs, BlogsAdmin)
admin.site.register(Members, MembersAdmin)
