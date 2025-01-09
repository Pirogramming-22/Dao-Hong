from django.db import models

class MovieReview(models.Model):
    GENRE_CHOICES = [
        ('액션', '액션'),
        ('코미디', '코미디'),
        ('드라마', '드라마'),
        ('스릴러', '스릴러'),
        ('애니메이션', '애니메이션'),
        ('SF', 'SF'),
    ]
    title = models.CharField(max_length=100)
    director = models.CharField(max_length=100)
    cast = models.CharField(max_length=200)
    genre = models.CharField(max_length=50, choices=GENRE_CHOICES)
    release_year = models.IntegerField(default=1990)
    runtime = models.IntegerField(default=120)
    rating = models.FloatField(default=3.0)
    review_text = models.TextField(default='')
    image = models.ImageField(upload_to='review_images/', blank=True, null=True)

    def __str__(self):
        return self.title
