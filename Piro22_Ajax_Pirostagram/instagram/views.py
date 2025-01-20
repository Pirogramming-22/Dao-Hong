from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.http import JsonResponse
from .forms import PostForm
from .models import Post, PostImage, Comment, Like
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import render, redirect

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('main') 
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('main')
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})


def main_page(request):
    sort_option = request.GET.get('sort', 'recent')
    if sort_option == 'old':
        posts = Post.objects.all().order_by('created_at')
    else:
        posts = Post.objects.all().order_by('-created_at')

    context = {
        'posts': posts,
        'post_count': 123,
        'follower_count': 123,
        'following_count': 123,
    }
    return render(request, 'main.html', context)
@login_required
def create_post(request):
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                # 게시글 저장
                post = form.save(commit=False)
                post.user = request.user
                post.save()

                # 이미지 저장
                for image in request.FILES.getlist('images'):
                    PostImage.objects.create(
                        post=post,
                        image=image
                    )
                return redirect('main')
            except Exception as e:
                print("Error:", str(e))
                if 'post' in locals():
                    post.delete()
                form.add_error(None, "게시글 작성 중 오류가 발생했습니다.")
        else:
            print("Form errors:", form.errors)
    else:
        form = PostForm()
    
    return render(request, 'create_post.html', {'form': form})
def post_detail(request, post_id):
    post = get_object_or_404(Post, pk=post_id)
    images = post.images.all()
    comments = post.comments.filter(parent__isnull=True).order_by('-created_at')

    liked = False
    if request.user.is_authenticated:
        liked = Like.objects.filter(post=post, user=request.user).exists()

    context = {
        'post': post,
        'images': images,
        'comments': comments,
        'liked': liked
    }
    return render(request, 'post_detail.html', context)
@login_required
def add_comment(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        content = request.POST.get('content')
        parent_id = request.POST.get('parent_id', None)

        post = get_object_or_404(Post, pk=post_id)
        if parent_id:
            parent_comment = get_object_or_404(Comment, pk=parent_id)
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content,
                parent=parent_comment
            )
        else:
            comment = Comment.objects.create(
                post=post,
                user=request.user,
                content=content
            )

        return JsonResponse({
            'status': 'ok',
            'comment_id': comment.id,
            'content': comment.content,
            'username': comment.user.username
        })
    return JsonResponse({'status': 'fail'}, status=400)
@login_required
def toggle_like(request):
    if request.method == 'POST':
        post_id = request.POST.get('post_id')
        post = get_object_or_404(Post, pk=post_id)

        like_qs = Like.objects.filter(post=post, user=request.user)
        if like_qs.exists():
            like_qs.delete()
            liked = False
        else:
            Like.objects.create(post=post, user=request.user)
            liked = True

        like_count = post.likes.count()

        return JsonResponse({
            'liked': liked,
            'like_count': like_count,
        })
    return JsonResponse({'error': 'Invalid request'}, status=400)
def search_posts(request):
    q = request.GET.get('q', '')
    posts = Post.objects.filter(
        Q(caption__icontains=q) | Q(user__username__icontains=q)
    )
    result_list = [
        {
            'post_id': p.id,
            'caption': p.caption,
            'username': p.user.username,
            'image_url': p.images.first().image.url if p.images.first() else ''
        }
        for p in posts
    ]
    return JsonResponse({'results': result_list})
@login_required
def delete_comment(request):
    if request.method == 'POST':
        comment_id = request.POST.get('comment_id')
        comment = get_object_or_404(Comment, pk=comment_id)
        
        # 댓글 작성자나 게시글 작성자만 삭제 가능
        if request.user == comment.user or request.user == comment.post.user:
            comment.delete()
            return JsonResponse({'status': 'ok'})
        else:
            return JsonResponse({'status': 'error', 'message': '삭제 권한이 없습니다.'}, status=403)
    
    return JsonResponse({'status': 'error', 'message': '잘못된 요청입니다.'}, status=400)