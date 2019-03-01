from django import forms
from .models import Post


class PostForm(forms.ModelForm):
    field_order = ["title", "author", "date", "abstract", ]

    class Meta:
        model = Post
        fields = ("title", "author", "date", "abstract",)


class SearchForm(forms.Form):
    title = forms.CharField(min_length=0, max_length=100, required=False)
    author = forms.CharField(min_length=0, max_length=100, required=False)
    abstract = forms.CharField(min_length=0, max_length=100, required=False)
