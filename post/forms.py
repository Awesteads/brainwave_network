from django import forms

from .models import Post, Comment

INPUT_CLASSES = 'w-full py-4 px-6 rounded-xl border'

class NewPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'texto')
        widgets = {
            'titulo': forms.TextInput(attrs={
                'placeholder': 'Título',
                'class': INPUT_CLASSES
            }),
            'texto': forms.Textarea(attrs={
                'placeholder': 'Escreva sua publicação',
                'class': INPUT_CLASSES
            }),
        }

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'placeholder': 'Escreva seu comentário',
                'class': INPUT_CLASSES
            }),
        }

class EditPostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ('titulo', 'texto')
        widgets = {
            'titulo': forms.TextInput(attrs={
                'class': INPUT_CLASSES
            }),
            'texto': forms.Textarea(attrs={
                'class': INPUT_CLASSES
            })
        }