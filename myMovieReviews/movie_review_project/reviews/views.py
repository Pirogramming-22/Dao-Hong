from django.shortcuts import render, get_object_or_404, redirect
from .models import MovieReview
from .forms import MovieReviewForm
from django.db.models import F
from .utils import fetch_movie_details


def review_list(request):
    # 정렬 조건 가져오기
    sort_option = request.GET.get('sort', 'title')  # 기본 정렬은 'title'
    
    # 정렬 기준 적용
    if sort_option == 'title':
        reviews = MovieReview.objects.order_by('title')
    elif sort_option == 'rating':
        reviews = MovieReview.objects.order_by('-rating')  # 평점 내림차순
    elif sort_option == 'release_year':
        reviews = MovieReview.objects.order_by('-release_year')  # 개봉년도 내림차순
    else:
        reviews = MovieReview.objects.all()  # 기본 값

    return render(request, 'reviews/review_list.html', {'reviews': reviews})

def review_detail(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    
    # 러닝타임 계산 (시간과 분)
    runtime_hours = review.runtime // 60
    runtime_minutes = review.runtime % 60
    
    return render(request, 'reviews/review_detail.html', {
        'review': review,
        'runtime_hours': runtime_hours,
        'runtime_minutes': runtime_minutes,
    })

def fetch_movie(request):
    """Fetch movie details based on user input."""
    if request.method == "POST":
        title = request.POST.get("title")
        movie_details = fetch_movie_details(title)
        return render(request, "reviews/movie_form.html", {"movie_details": movie_details})
    return render(request, "reviews/movie_form.html")

def review_create(request):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = MovieReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})

def review_edit(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    if request.method == 'POST':
        form = MovieReviewForm(request.POST, instance=review)
        if form.is_valid():
            form.save()
            return redirect('review_detail', pk=pk)
    else:
        form = MovieReviewForm(instance=review)
    return render(request, 'reviews/review_form.html', {'form': form})

def review_delete(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'reviews/review_delete.html', {'review': review})
