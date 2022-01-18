from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    title = forms.CharField(max_length=100, help_text='Article title', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    meta_title = forms.CharField(max_length=100, help_text='Title for SEO', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    meta_description = forms.CharField(max_length=1000, help_text='Description for SEO', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 2}))
    meta_keywords = forms.CharField(max_length=1000, help_text='Keywords for SEO', widget=forms.Textarea(attrs={'class': 'col-12', 'rows': 1}))
    text = forms.CharField(
        help_text='Article text',
        widget=forms.Textarea(attrs={'id': "text_editor", 'style': 'display:none;'}),
        required=True)

    class Meta:
        model = Post
        fields = ["title", "image", "text", "meta_title", "meta_description", "meta_keywords"]

