from django.urls import path

from blog import views

urlpatterns = [
    path('', views.index, name='index'),
    path('blog/', views.BlogListView.as_view(), name='blog'),
    path('writer/', views.WriterListView.as_view(), name='writer'),
    path('blog/<str:pk>', views.BlogDetailView.as_view(), name='blog-detail'),
    path('writer/<str:pk>', views.WriterDetailView.as_view(), name='writer-detail'),
    path('subscribed-blogs/', views.SuscribeToBlogByUserListView.as_view(), name='subscribed'),
    path('blog/<uuid:pk>/renew/', views.renew_subscription_staff, name='renew-subscription-staff'),
    path('writer/create/', views.WriterCreate.as_view(), name='writer-create'),
    path('writer/<str:pk>/update/', views.WriterUpdate.as_view(), name='writer-update'),
    path('writer/<str:pk>/delete/', views.WriterDelete.as_view(), name='writer-delete'),
    path('blog/create/', views.BLogCreate.as_view(), name='blog-create'),
    path('blog/<str:pk>/update/', views.BlogUpdate.as_view(), name='blog-update'),
    path('blog/<str:pk>/delete/', views.BlogDelete.as_view(), name='blog-delete'),
]

