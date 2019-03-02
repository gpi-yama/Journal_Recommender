from django import forms
from .models import Post, PostFav


class PostForm(forms.ModelForm):
    field_order = ["title", "author", "date", "abstract", ]

    class Meta:
        model = Post
        fields = ("title", "author", "date", "abstract",)


class SearchForm(forms.Form):
    title = forms.CharField(min_length=0, max_length=100, required=False)
    author = forms.CharField(min_length=0, max_length=100, required=False)
    abstract = forms.CharField(min_length=0, max_length=100, required=False)


CHOICE = [
    ("0", "unread"),
    ("1", "want"),
    ("2", "read"),
    ("3", "fav"),
]


class FavForm(forms.Form):
    initial = 0
    fav_id = forms.IntegerField()
    select = forms.ChoiceField(
        label="評価：",
        widget=forms.RadioSelect,
        choices=CHOICE,
        initial=initial)
