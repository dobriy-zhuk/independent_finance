from django.shortcuts import render
from django.contrib import messages
from django.shortcuts import render, get_object_or_404, redirect
from .models import Post
from django.utils import timezone
from .forms import PostForm
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger


def post_list(request):
    posts = Post.objects.all()
    return render(request, 'blog/blog.html', {'posts': posts})


def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug)
    return render(request, 'blog/blog_post.html', {'post': post})


def post_new(request):
    if request.method == "POST":
        post = PostForm(request.POST, request.FILES)
        if post.is_valid():
            post = post.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            #post.image = request.FILES
            post.save()
            messages.success(request, 'Saved')
            return redirect('post_detail', slug=post.slug)
    else:
        post = PostForm()
    return render(request, 'blog/new_post.html', {'post': post})


@login_required
def edit_post(request, slug):

    post = get_object_or_404(Post, slug=slug)

    if request.method == "POST":
        post_form = PostForm(request.POST, request.FILES, instance=post)
        if post_form.is_valid():
            post_form.save()
            messages.success(request, 'Success')
        return redirect("blog")
    else:
        post_form = PostForm(instance=post)

    return render(request, "blog/edit_post.html", {"post_form": post_form, })


@login_required
def remove_post(request, slug):
    try:
        post = get_object_or_404(Post, slug=slug)
        post.delete()
    except Post.DoesNotExist:
        messages.error(request, "Couldn`t remove. Try again")
        #return render(request, 'front.html')
        return redirect('blog')

    except Exception as e:
        return redirect('blog', {'err': e})

    return redirect('blog')