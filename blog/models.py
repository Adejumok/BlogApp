import datetime
import uuid

from django.db import models
from django.urls import reverse


# Create your models here.
class BlogType(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a blog type(e.g. Celebrity Gist)')

    def __str__(self):
        return self.name


class Blog(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          help_text='Unique ID for this particular blog')
    title = models.CharField(max_length=200)
    writer = models.ForeignKey('Writer', on_delete=models.SET_NULL, null=True)
    blog_type = models.ManyToManyField(BlogType, help_text='Select a type for this blog')
    description = models.TextField(max_length=1000, help_text='Enter the description of this blog')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          help_text='Unique ID for this particular comment')
    blog = models.ForeignKey(Blog, on_delete=models.RESTRICT, null=True)
    written_date = models.DateField(datetime.datetime, auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['written_date']

    def __str__(self):
        return f'{self.id} ({self.blog.title})'


class Writer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)

    class Meta:
        ordering = ['first_name', 'last_name']

    def get_absolute_url(self):
        return reverse('writer-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'
