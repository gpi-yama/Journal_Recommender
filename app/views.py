from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from .models import Post
from .forms import PostForm, SearchForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q
from django.template import RequestContext

from django.shortcuts import render_to_response
# Create your views here.


def listing(request, order):
    if request.method == 'POST':
        form = SearchForm(request.POST)
        posts = Post.objects.all()

        if form.is_valid():
            posts = Post.objects.filter(
                Q(title__contains=form.cleaned_data["title"]) &
                Q(author__contains=form.cleaned_data["author"]) &
                Q(abstract__contains=form.cleaned_data["abstract"])
            ).order_by(order)

    else:
        form = SearchForm()
        posts = Post.objects.all().order_by(order)

    paginator = Paginator(posts, 10)
    page = request.GET.get("page")

    try:
        cposts = paginator.page(page)
    except PageNotAnInteger:
        cposts = paginator.page(1)
    except EmptyPage:
        cposts = paginator.page(paginator.num_pages)

    return form, cposts


def post_list(request):
    form, cposts = listing(request, "id")
    return render(request, 'app/post_list.html',
                  {'form': form, 'posts': cposts})


def post_list_old(request):
    form, cposts = listing(request, "-id")
    return render(request, 'app/post_list.html',
                  {'form': form, 'posts': cposts})


"""
def post_list_created_date(request):
    posts = Post.objects.filter(
        author=request.user
    ).order_by("created_date")
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.created_date = timezone.now()
            post.save()
    else:
        form = PostForm()
    return render(request, 'app/post_list.html', {'posts': posts, 'form': form})


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    now = timezone.now()
    return render(request, 'app/post_detail.html', {'post': post, 'now': now})


def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect(post_detail, pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'app/post_edit.html', {'form': form, 'post': post})


class BoardListView(ListView):
    model = Post
    context_object_name = 'boards'
    template_name = 'app/home.html'
"""
