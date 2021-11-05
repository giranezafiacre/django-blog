import time
from django.shortcuts import render
from .models import Post, Comment
from .forms import Postform, Updateform
# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404,redirect

def index(request):
    """View function for home page of site."""

    posts=Post.objects.all()
    for post in posts:
        print(type(post.created_on))

    context = {
        'posts':posts
    }

    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

def create_post(request):
    context ={}
 
    form = Postform(request.POST,request.FILES)
    
    print(form)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
         
    context['form']= form
    return render(request, 'create_post.html', context=context)

def update_post(request,id):
    context ={}
    instance = get_object_or_404(Post, id=id)
    form = Updateform(request.POST or None, instance=instance)
    # print('hi there',datetime.date.today)
    if form.is_valid():
        form.instance.created_on = time.strftime(r"%Y-%m-%d", time.localtime())
        form.save()

    context['form']= form
    return render(request, 'update_post.html', context=context)