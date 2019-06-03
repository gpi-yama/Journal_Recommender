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
from django.core.cache import cache
from django.shortcuts import render_to_response
from django import db
# Create your views here.


def listing(request, order):
    form_fav = FavForm()
    if request.method == "POST":
        print("WHAHA", request.POST["post_fav"])
        form_fav = FavForm(request.POST)
        PostFav.objects.update_or_create(
            user=request.user,
            fav_id=form_fav.data["fav_id"],
            defaults={
                "fav_date": timezone.now(),
                "score": form_fav.data["select"],
            }
        )
    query = False
    if request.GET.get("title") is not None:
        title = request.GET.get("title")
        query = True
    if request.GET.get('author') is not None:
        author = request.GET.get('author')
        query = True
    if request.GET.get('abstract') is not None:
        abstract = request.GET.get('abstract')
        query = True

    form = SearchForm()
    if query is True:
        posts = Post.objects.filter(
            Q(title__contains=title) &
            Q(author__contains=author) &
            Q(abstract__contains=abstract)
        ).order_by(order)

    else:
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
                   'form_fav': form_fav, 'query_string': request.GET.urlencode()})


def post_list_old(request):
    form, cposts, form_fav = listing(request, "-id")
    return render(request, 'app/post_list.html',
                  {'form': form, 'posts': cposts,
                   'form_fav': form_fav})
    del form, cposts, form_fav


def url_replace(request, field, value):
    url_dict = request.GET.copy()
    url_dict[field] = str(value)
    return url_dict.urlencode()


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

    del request, posts, form_fav, post_user


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
    del request, posts, form_fav, post_user


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
    del request, posts, form_fav, post_user


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
    del posts, post_user, request


def cash_clear(request):
    db.reset_queries()
    cache.clear()
    return render(request, "app/cash_clear.html")


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
