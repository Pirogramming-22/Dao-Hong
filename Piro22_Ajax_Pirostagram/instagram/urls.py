from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from django.shortcuts import redirect

urlpatterns = [
    path('', views.main_page, name='main'),        
    path('post/new/', views.create_post, name='create_post'),  
    path('post/<int:post_id>/', views.post_detail, name='post_detail'), 

    path('comment/add/', views.add_comment, name='add_comment'),
    path('like/toggle/', views.toggle_like, name='toggle_like'),
    path('search/', views.search_posts, name='search_posts'),
    path('login/', views.login_view, name='login'),
    path('register/', views.register_view, name='register'),
    path('comment/delete/', views.delete_comment, name='delete_comment'),
]



def logout_view(request):
    logout(request)
    return redirect('main')

urlpatterns += [
    path('logout/', logout_view, name='logout'),
]


if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)