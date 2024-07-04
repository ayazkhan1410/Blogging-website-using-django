from django.contrib import admin
from .models import *

# Register your models here.
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ['email', 'phone', 'address', 'user_profile']
    search_fields = ['email', 'phone']
    list_filter = ['email', 'phone']

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']
    search_fields = ['name']
    list_filter = ['name']

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ['user', 'category', 'title', 'author_name', 'description', 'image', 'is_featured', 'created_at', 'slug']
    search_fields = ['category', 'title']
    list_filter = ['category', 'title']
    
@admin.register(Comments)
class CommentsAdmin(admin.ModelAdmin):
    list_display = ['blog', 'user', 'comment', 'created_at']
    search_fields = ['blog', 'user']
    list_filter = ['blog', 'user']

@admin.register(Contact)
class ContactAdmin(admin.ModelAdmin):
    list_display = ['name', 'email', 'message']
    search_fields = ['name', 'email']
    list_filter = ['name', 'email']

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'forget_token']
    search_fields = ['user']
    list_filter = ['user']