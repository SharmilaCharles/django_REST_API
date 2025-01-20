from django.contrib import admin
from .models import Blog,Comment


class BlogAdmin(admin.ModelAdmin):
    # Ordering the blog fields
    fields = ['blog_title','blog_body'] 

    #search the blog fields content
    search_fields = ['blog_title']

    # Filter the blog felds
    list_filter = ['blog_title', 'blog_body']

    #display the blog table title
    list_display = ['blog_title', 'blog_body']

    # edit the blog fields content 
    list_editable = ['blog_body']

admin.site.register(Blog, BlogAdmin)
admin.site.register(Comment)


