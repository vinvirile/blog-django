from django.contrib import admin
from .models import Members

class MembersAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'email', 'created_at') # Add 'created_at' to the list display
    readonly_fields = ('created_at',) # Make 'created_at' read-only

admin.site.register(Members, MembersAdmin)
