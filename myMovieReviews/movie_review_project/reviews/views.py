from django.shortcuts import render, get_object_or_404, redirect
from .models import MovieReview
from .forms import MovieReviewForm
from django.db.models import F

# Review List
def review_list(request):
    sort_by = request.GET.get('sort', 'title')  # 기본 정렬은 'title'
    reviews = MovieReview.objects.all().order_by(sort_by)
    return render(request, 'reviews/review_list.html', {'reviews': reviews})

# Review Detail
def review_detail(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    return render(request, 'reviews/review_detail.html', {'review': review})

# Create Review
def review_create(request):
    if request.method == 'POST':
        form = MovieReviewForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('review_list')
    else:
        form = MovieReviewForm()
    return render(request, 'reviews/review_form.html', {'form': form})

# Edit Review
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

# Delete Review
def review_delete(request, pk):
    review = get_object_or_404(MovieReview, pk=pk)
    if request.method == 'POST':
        review.delete()
        return redirect('review_list')
    return render(request, 'reviews/review_confirm_delete.html', {'review': review})
