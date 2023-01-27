from django.shortcuts import render
from django.views import generic

from blog.models import Blog, Comment, Writer


def index(request):
    num_blogs = Blog.objects.all().count()
    num_comments = Comment.objects.all().count()
    num_writers = Writer.objects.count()
    num_blogs_travel = Blog.objects.filter(blog_type__exact='P').count()

    context = {
        'num_blogs': num_blogs,
        'num_comments': num_comments,
        'num_writers': num_writers,
        'num_blogs_travel': num_blogs_travel
    }

    return render(request, 'index.html', context=context)


class BlogListView(generic.ListView):
    model = Blog
    context_object_name = 'blog_list'
    paginate_by = 10

    def get_queryset(self):
        return Blog.objects.filter(title__icontains='aba')[:2]

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class WriterListView(generic.ListView):
    model = Writer
    context_object_name = 'writer_list'
