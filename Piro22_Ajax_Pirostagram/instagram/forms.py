from django import forms
from .models import Post, PostImage

class MultipleFileInput(forms.FileInput):
    input_type = 'file'

    def get_context(self, name, value, attrs):
        attrs['multiple'] = True
        return super().get_context(name, value, attrs)

class PostForm(forms.ModelForm):
    images = forms.FileField(
        widget=MultipleFileInput(attrs={'accept': 'image/*'}),
        required=True,
        label='이미지',
        help_text='최대 5장까지 업로드 가능합니다.'
    )

    class Meta:
        model = Post
        fields = ['caption']

    def clean_images(self):
        files = self.files.getlist('images')
        if not files:
            raise forms.ValidationError("최소 1장의 이미지를 업로드해야 합니다.")
        if len(files) > 5:
            raise forms.ValidationError("이미지는 최대 5장까지 업로드 가능합니다.")
        
        for file in files:
            if not file.content_type.startswith('image/'):
                raise forms.ValidationError("이미지 파일만 업로드 가능합니다.")
        
        return files
