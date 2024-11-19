from django.shortcuts import render, get_object_or_404
from django.http import Http404

from blog.models import Post, Category

# Create your views here.
from django.utils import timezone


def post_detail(request, post_id):
    template = "blog/detail.html"

    post = get_object_or_404(
        Post, pk=post_id, is_published=True, pub_date__lte=timezone.now()
    )

    if post.category and not post.category.is_published:
        raise Http404("Пост относится к категории, снятой с публикации.")

    return render(request, template, {"post": post})


def category_posts(request, category_slug):
    template = "blog/category.html"
    category_object = get_object_or_404(
        Category, slug=category_slug, is_published=True, created_at__lte=timezone.now()
    )

    context = {
        "post_list": Post.objects.all().filter(
            category_id=category_object.id,
            is_published=True,
            pub_date__lte=timezone.now(),
        )
    }
    context["category"] = category_object

    return render(request, template, context)


def index(request):
    template = "blog/index.html"
    category_object = Category.objects.filter(is_published=True)

    context = {
        "post_list": Post.objects.all()
        .filter(
            pub_date__lte=timezone.now(),
            is_published=True,
            category__in=category_object,
        )
        .order_by("-id")[:5]
    }
    return render(request, template, context)
