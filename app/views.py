from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from django.views.generic import ListView
from .models import Post, PostFav
from .forms import PostForm, SearchForm, FavForm
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q, Count
from django.template import RequestContext
from datetime import datetime
from django.contrib.auth.decorators import login_required

from django.shortcuts import render_to_response
# Create your views here.


def listing(request, order):
    form_fav = FavForm()
    if request.method == "POST":
        form_fav = FavForm(request.POST)
        print(form_fav.data["select"])
        PostFav.objects.update_or_create(
            user=request.user,
            fav_id=form_fav.data["fav_id"],
            defaults={
                "fav_date": timezone.now(),
                "score": form_fav.data["select"],
            }
        )

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

    return form, cposts, form_fav


def post_list(request):
    form, cposts, form_fav = listing(request, "id")
    return render(request, 'app/post_list.html',
                  {'form': form, 'posts': cposts,
                   'form_fav': form_fav})


def post_list_old(request):
    form, cposts, form_fav = listing(request, "-id")
    return render(request, 'app/post_list.html',
                  {'form': form, 'posts': cposts,
                   'form_fav': form_fav})


def fav(request):
    if request.method == "POST":
        form_fav = FavForm(request.POST)
        print(form_fav.cleaned_data["select"])


def favorite(request):
    form_fav = FavForm()
    if request.method == "POST":
        form_fav = FavForm(request.POST)
        form_fav.initial = 3
        print(form_fav.data["select"])
        PostFav.objects.update_or_create(
            user=request.user,
            fav_id=form_fav.data["fav_id"],
            defaults={
                "fav_date": timezone.now(),
                "score": form_fav.data["select"],
            }
        )
    post_user = PostFav.objects.filter(
        user=request.user
    )
    posts = Post.objects.filter(
        id__in=PostFav.objects.filter(user=request.user, score=3).values(
            "fav_id").annotate(dcount=Count("fav_id")).values("fav_id")
    ).order_by("id")

    return render(request, "app/favorite.html",
                  {"posts": posts, "form_fav": form_fav})


def want(request):
    form_fav = FavForm()
    if request.method == "POST":
        form_fav.initial = 1
        form_fav = FavForm(request.POST)
        print(form_fav.data["select"])
        PostFav.objects.update_or_create(
            user=request.user,
            fav_id=form_fav.data["fav_id"],
            defaults={
                "fav_date": timezone.now(),
                "score": form_fav.data["select"],
            }
        )
    post_user = PostFav.objects.filter(
        user=request.user
    )
    posts = Post.objects.filter(
        id__in=PostFav.objects.filter(user=request.user, score=1).values(
            "fav_id").annotate(dcount=Count("fav_id")).values("fav_id")
    ).order_by("id")

    return render(request, "app/want.html",
                  {"posts": posts, "form_fav": form_fav})


def read(request):
    form_fav = FavForm()
    if request.method == "POST":
        form_fav.initial = 2
        form_fav = FavForm(request.POST)
        print(form_fav.data["select"])
        PostFav.objects.update_or_create(
            user=request.user,
            fav_id=form_fav.data["fav_id"],
            defaults={
                "fav_date": timezone.now(),
                "score": form_fav.data["select"],
            }
        )
    post_user = PostFav.objects.filter(
        user=request.user
    )
    posts = Post.objects.filter(
        id__in=PostFav.objects.filter(user=request.user, score=2).values(
            "fav_id").annotate(dcount=Count("fav_id")).values("fav_id")
    ).order_by("id")

    return render(request, "app/read.html",
                  {"posts": posts, "form_fav": form_fav})


def famous(request):
    post_user = PostFav.objects.filter(
        user=request.user
    )
    posts = Post.objects.filter(
        id__in=PostFav.objects.all().values(
            "fav_id").annotate(
                dcount=Count("fav_id")).order_by(
                    "dcount").values(
                        "fav_id")
    )

    return render(request, "app/famous.html", {"posts": posts})


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
