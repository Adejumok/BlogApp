import datetime

from django.contrib.auth.decorators import login_required, permission_required
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.http import HttpResponseRedirect
from django.shortcuts import render, get_object_or_404
from django.views import generic

from blog.forms import RenewBlogForm
from blog.models import Blog, Comment, Writer, BlogInstance


@login_required
# @permission_required('blog.can_mark_subscribed', raise_exception=True)
# @permission_required('blog.can_edit')
def index(request):
    num_blogs = Blog.objects.all().count()
    num_comments = Comment.objects.all().count()
    num_instances = BlogInstance.objects.all().count()
    num_instances_available = BlogInstance.objects.filter(status__exact='F').count()
    num_writers = Writer.objects.count()
    num_visits = request.session.get('num_visits', 0)
    request.session['num_visits'] = num_visits + 1

    context = {
        'num_blogs': num_blogs,
        'num_comments': num_comments,
        'num_writers': num_writers,
        'num_instances': num_instances,
        'num_instances_available': num_instances_available,
        'num_visits': num_visits
    }

    return render(request, 'index.html', context=context)


class BlogListView(LoginRequiredMixin, generic.ListView):
    model = Blog
    context_object_name = 'blog_list'
    paginate_by = 10
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    queryset = Blog.objects.all()
    template_name = 'blog_list.html'
    permission_required = ('blog.can_mark_subscribed', 'blog.can_edit')

    def get_queryset(self):
        return Blog.objects.filter(title__icontains='aba')[:2]

    def get_context_data(self, **kwargs):
        context = super(BlogListView, self).get_context_data(**kwargs)
        context['some_data'] = 'This is just some data'
        return context


class WriterListView(LoginRequiredMixin, generic.ListView):
    model = Writer
    context_object_name = 'writer_list'
    login_url = '/login/'
    redirect_field_name = 'redirect_to'
    queryset = Writer.objects.all()
    template_name = 'writer_list.html'


class BlogDetailView(generic.DetailView):
    model = Blog
    queryset = Blog.objects.all()
    template_name = 'blog_detail.html'


class WriterDetailView(generic.DetailView):
    model = Writer
    queryset = Writer.objects.all()
    template_name = 'writer_detail.html'


class SuscribeToBlogByUserListView(LoginRequiredMixin, generic.ListView):
    """Generic class-based view listing blogs subscribed by current user."""
    model = BlogInstance
    template_name = 'bloginstance_list_subscribed_user.html'
    paginate_by = 10

    # @permission_required('blog.can_mark_subscribed', raise_exception=True)
    def get_queryset(self):
        return BlogInstance.objects.filter(subscriber=self.request.user).filter(status__exact='P').order_by('due_back')


@login_required
@permission_required('blog.can_mark_subscribed', raise_exception=True)
def renew_blog_staff(request, pk):
    blog_instance = get_object_or_404(BlogInstance, pk=pk)

    if request.method == 'POST':

        form = RenewBlogForm(request.POST)

        if form.is_valid():
            blog_instance.due_back = form.cleaned_data['renewal_date']
            blog_instance.save()

            return HttpResponseRedirect('/')

    else:
        proposed_renewal_date = datetime.date.today() + datetime.timedelta(weeks=3)
        form = RenewBlogForm(initial={'renewal_date': proposed_renewal_date})

    context = {
        'form': form,
        'blog_instance': blog_instance,
    }

    return render(request, 'blog_renew_staff.html', context)
