from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('blog/', views.WriterListView.as_view(), name='writer'),
]

