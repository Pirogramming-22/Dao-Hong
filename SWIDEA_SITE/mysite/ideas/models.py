from django.db import models

# Create your models here.


class Idea(models.Model):
    title = models.CharField(max_length=200)
    image = models.ImageField(upload_to='images/')
    content = models.TextField()
    interest = models.IntegerField(default=0)
    devtool = models.ForeignKey('DevTool', on_delete=models.SET_NULL, null=True)
    
    def is_starred(self, user):
        return self.ideastar_set.filter(user=user, starred=True).exists()

class IdeaStar(models.Model):
    user = models.ForeignKey('auth.User', on_delete=models.CASCADE, null=True)
    idea = models.ForeignKey('Idea', on_delete=models.CASCADE)
    starred = models.BooleanField(default=False)

class DevTool(models.Model):
    name = models.CharField(max_length=200)
    kind = models.CharField(max_length=100)
    content = models.TextField()

#로그인 기능을 구현하라는 말은 없어서 유저 커스텀 모델만 구현하였음
class CustomUser(models.Model):
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    date_joined = models.DateTimeField(auto_now_add=True)