from datetime import date, datetime
import uuid

from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User


class BlogType(models.Model):
    name = models.CharField(max_length=200, help_text='Enter a blog type(e.g. Celebrity Gist)')

    def __str__(self):
        return self.name


class Blog(models.Model):
    BLOG_CHOICES = (
        ("F", "Food"),
        ("T", "Travel"),
        ("H", "Health"),
        ("L", "Lifestyle"),
        ("FB", "Fashion & Beauty"),
        ("PH", "Photography"),
        ("P", "Personal"),
        ("DC", "DIY Craft")

    )
    title = models.CharField(max_length=200)
    description = models.TextField()
    writer = models.ForeignKey('Writer', models.DO_NOTHING, blank=True, null=True)
    blog_type = models.CharField(max_length=2, choices=BLOG_CHOICES)
    id = models.CharField(primary_key=True, max_length=32)

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('blog-detail', args=[str(self.id)])


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4(),
                          help_text='Unique ID for this particular comment')
    blog = models.ForeignKey(Blog, on_delete=models.DO_NOTHING, null=True)
    written_date = models.DateField(datetime, auto_now=True, null=True, blank=True)

    class Meta:
        ordering = ['written_date']

    def __str__(self):
        return f'{self.id} ({self.blog.title})'


class BlogInstance(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, help_text='Unique ID for this particular blog '
                                                                          'instance across'
                                                                          'whole blog website')
    blog = models.ForeignKey('Blog', on_delete=models.RESTRICT, null=True)
    imprint = models.CharField(max_length=200)
    due_back = models.DateField(null=True, blank=True)
    subscriber = models.ForeignKey(User, on_delete=models.SET_NULL,
                                   null=True, blank=True)
    permissions = (("can_mark_subscribed", "Set blog as subscribed"),)

    SUBSCRIPTION_STATUS = (
        ("F", "Freemium"),
        ("P", "Pay-As-You-Go"),
        ("FU", "Fixed Usage"),
        ('U', 'Unlimited'),
    )

    status = models.CharField(
        max_length=2,
        choices=SUBSCRIPTION_STATUS,
        blank=True,
        default="F",
        help_text='Blog subscription',
    )

    @property
    def is_overdue(self):
        return bool(self.due_back and date.today() > self.due_back)

    class Meta:
        ordering = ['due_back']

    def __str__(self):
        return f'{self.id} ({self.blog.title})'


class Writer(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.EmailField(unique=True)
    id = models.CharField(primary_key=True, max_length=32)

    def get_absolute_url(self):
        return reverse('writer-detail', args=[str(self.id)])

    def __str__(self):
        return f'{self.first_name} {self.last_name}'

    class Meta:
        ordering = ['first_name']
