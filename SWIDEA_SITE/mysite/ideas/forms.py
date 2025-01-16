from django import forms
from .models import Idea, DevTool
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm

class DevToolChoiceField(forms.ModelChoiceField):
    def label_from_instance(self, obj):
        return obj.name

class IdeaForm(forms.ModelForm):
    devtool = DevToolChoiceField(
    queryset=DevTool.objects.all(),
    widget=forms.Select(attrs={'class': 'form-control'})
    )
    class Meta:
        model = Idea
        fields = ['title', 'image', 'content', 'interest', 'devtool']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
            'interest': forms.NumberInput(attrs={'class': 'form-control'}),
            # 'devtool': forms.Select(attrs={'class': 'form-control'}),
            'image': forms.FileInput(attrs={'class': 'form-control-file'}),
        }

class DevToolForm(forms.ModelForm):
    class Meta:
        model = DevTool
        fields = ['name', 'kind', 'content']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'kind': forms.TextInput(attrs={'class': 'form-control'}),
            'content': forms.Textarea(attrs={'class': 'form-control'}),
        }

class SignUpForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('username', 'password1', 'password2')

class LoginForm(AuthenticationForm):
    pass
