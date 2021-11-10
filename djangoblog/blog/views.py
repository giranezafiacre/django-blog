import time
from django.shortcuts import render
from .models import Like, Post, Comment
from .forms import Postform, Updateform, createComment
# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect


def index(request):
    """View function for home page of site."""
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)


def create_post(request):
    context = {}
    form = Postform(request.POST, request.FILES)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        response = redirect('/')
        return response
    else:
        form = Postform()

    context['form'] = form
    return render(request, 'create_post.html', context=context)


def update_post(request, id):
    context = {}
    instance = get_object_or_404(Post, id=id)
    form = Updateform(request.POST, request.FILES,instance=instance)
    if form.is_valid():
        form.instance.created_on = time.strftime(r"%Y-%m-%d", time.localtime())
        form.save()
        response = redirect('/dashboard')
        return response
    else:
        form = Updateform(request.POST or None, instance=instance)
    context['form'] = form
    return render(request, 'update_post.html', context=context)


def dashboard(request):
    posts = Post.objects.all()

    context = {
        'posts': posts
    }
    return render(request, 'datatable.html', context=context)


def delete_post(request,pk):
    record=Post.objects.get(id=pk)
    record.delete()
    response = redirect('/dashboard')
    return response


def fullpost(request, id):
    post = Post.objects.get(id=id)
    comment_form = createComment(request.POST or None)
    print(request.POST)
    if comment_form.is_valid():
        comment_form.instance.post = post
        comment_form.instance.user = request.user
        comment_form.save()
        comment_form = createComment()
    context = {
        'post': post,
        'comment_form': comment_form
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'fullpost.html', context=context)


def like_post(request, id):
    post = Post.objects.get(id=id)
    checkuser = Like.objects.filter(user=request.user,post=post)
    if not checkuser:
        Like.objects.create(
            post=post,
            user=request.user)
        print('done')
    print('not really')
    response = redirect('/')
    return response
