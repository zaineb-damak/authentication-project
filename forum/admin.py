from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from forum.models import Post,CustomUser

class CustomUserAdmin(UserAdmin):
    model = CustomUser
    list_display = ['username', 'email','first_name', 'last_name', 'is_staff']
 
admin.site.register(Post)
admin.site.register(CustomUser, CustomUserAdmin)
#admin.site.register(UserAPIKey)

