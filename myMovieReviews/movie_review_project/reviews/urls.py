from django.urls import path
from . import views
from django.conf.urls import handler404
from django.shortcuts import render

urlpatterns = [
    path('', views.review_list, name='review_list'),
    path('<int:pk>/', views.review_detail, name='review_detail'),
    path('new/', views.review_create, name='review_create'),
    path('<int:pk>/edit/', views.review_edit, name='review_edit'),
    path('<int:pk>/delete/', views.review_delete, name='review_delete'),
]


def custom_404(request, exception):
    return render(request, '404.html', status=404)

handler404 = custom_404