from django.contrib import admin
from blog.models import Blog, Writer, BlogType, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer', 'blog_type')
    inlines = [CommentInline]


class BlogInline(admin.TabularInline):
    model = Blog
    extra = 0


class WriterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

    fields = ['last_name', 'first_name', 'email']
    inlines = [BlogInline]


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('blog', 'written_date')


admin.site.register(Writer, WriterAdmin)
admin.site.register(BlogType)

# Register your models here.
