from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include

urlpatterns = [
    path('', views.idea_list, name='idea_list'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('ideas/new/', views.idea_new, name='idea_new'),
    path('ideas/<int:pk>/', views.idea_detail, name='idea_detail'),
    path('ideas/<int:pk>/edit/', views.idea_edit, name='idea_edit'),
    path('devtools/', views.devtool_list, name='devtool_list'),
    path('devtools/new/', views.devtool_new, name='devtool_new'),
    path('devtools/<int:pk>/', views.devtool_detail, name='devtool_detail'),
    path('devtools/<int:pk>/edit/', views.devtool_edit, name='devtool_edit'),
    path('ideas/<int:pk>/delete/', views.idea_delete, name='idea_delete'),
    path('devtools/<int:pk>/delete/', views.devtool_delete, name='devtool_delete'),
    path('ideas/change-interest/', views.change_interest, name='idea_change_interest'),
    path('toggle-star/', views.toggle_star, name='toggle_star'),
    path('signup/', views.signup, name='signup'),
    path('login/', views.user_login, name='login'),
    path('ideas/', views.idea_list, name='idea_list'),
    path('search/', views.idea_search, name='idea_search'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)