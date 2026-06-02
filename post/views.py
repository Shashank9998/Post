from django.contrib import messages
from django.core.paginator import Paginator
from django.db.models import Q
from django.views.decorators.http import require_POST
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CommentForm, PostForm
from .models import Comment, Post


def _remember_search(request, query):
    searches = request.session.get("recent_searches", [])
    searches = [item for item in searches if item != query]
    searches.insert(0, query)
    request.session["recent_searches"] = searches[:5]


def post_list(request):
    query = request.GET.get("q", "").strip()
    posts = Post.objects.prefetch_related("comments").all()

    if query:
        filters = Q(title__icontains=query)
        if query.isdigit():
            filters |= Q(id=int(query))
        posts = posts.filter(filters)
        _remember_search(request, query)

    if request.method == "POST":
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            post = form.save()
            messages.success(request, "Post uploaded successfully.")
            return redirect("post:post_detail", pk=post.pk)
    else:
        form = PostForm()

    paginator = Paginator(posts, 6)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "post/post_list.html",
        {
            "form": form,
            "page_obj": page_obj,
            "query": query,
            "recent_searches": request.session.get("recent_searches", []),
        },
    )


def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)

    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            messages.success(request, "Comment added successfully.")
            return redirect("post:post_detail", pk=post.pk)
    else:
        form = CommentForm()

    comments = Comment.objects.filter(post=post)
    paginator = Paginator(comments, 5)
    page_obj = paginator.get_page(request.GET.get("page"))

    return render(
        request,
        "post/post_detail.html",
        {
            "post": post,
            "form": form,
            "page_obj": page_obj,
        },
    )

@require_POST
def delete_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if post.photo:
        post.photo.delete(save=False)
    post.delete()
    messages.success(request, "Post deleted successfully.")
    return redirect("post:post_list")
