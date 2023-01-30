from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('writer/', views.WriterListView.as_view(), name='writer'),
    path('blog/<str:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('writer/<str:pk>', views.WriterDetailView.as_view(), name='writer-detail'),
    path('subscribed-blogs/', views.SuscribeToBlogByUserListView.as_view(), name='subscribed'),
    path('blog/<uuid:pk>/renew/', views.renew_blog_staff, name='renew-blog-staff'),
]

