from django.contrib import admin
from blog.models import Blog, Writer, BlogType, Comment, BlogInstance


class BlogInstanceInline(admin.TabularInline):
    model = BlogInstance
    extra = 0


@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    list_display = ('title', 'writer')
    inlines = [BlogInstanceInline]


# def display_blog_type(self):
#     return ', '.join(blog_type.name for blog_type in self.blog_type.all()[:3])
#
#
# display_blog_type.short_description = 'Blog_Type'


class WriterAdmin(admin.ModelAdmin):
    list_display = ('first_name', 'last_name', 'email')

    fields = ['last_name', 'first_name', 'email']


@admin.register(BlogInstance)
class BookInstanceAdmin(admin.ModelAdmin):
    list_display = ('blog', 'status', 'subscriber', 'due_back', 'id')
    list_filter = ('status', 'due_back')

    fieldsets = (
        (None, {
            'fields': ('blog', 'imprint', 'id')
        }),
        ('Subscription', {
            'fields': ('status', 'due_back', 'subscriber')
        }),
    )


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_filter = ('blog', 'written_date')


admin.site.register(Writer, WriterAdmin)
admin.site.register(BlogType)
