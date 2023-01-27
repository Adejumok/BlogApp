from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('writer/', views.WriterListView.as_view(), name='writer'),
    path('blog/blog/<uuid:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
]

