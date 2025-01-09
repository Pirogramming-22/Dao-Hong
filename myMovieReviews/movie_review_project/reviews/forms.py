from django import forms
from .models import MovieReview

class MovieReviewForm(forms.ModelForm):
    class Meta:
        model = MovieReview
        fields = ['title', 'director', 'cast', 'genre', 'release_year', 'runtime', 'rating', 'review_text']
