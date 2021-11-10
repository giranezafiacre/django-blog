import time
from django.shortcuts import render
from .models import Like, Post, Comment
from .forms import CreateUserForm, LoginForm, Postform, Updateform, createComment
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
# Create your views here.
from django.views import generic
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required


@login_required(login_url='login')
def index(request):
    """View function for home page of site."""
    posts = Post.objects.all()
    context = {
        'posts': posts,
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'index.html', context=context)

@login_required(login_url='login')
def create_post(request):
    context = {}
    form = Postform(request.POST, request.FILES)
    print(form)
    if form.is_valid():
        form.instance.author = request.user
        form.save()
        response = redirect('/')
        return response
    else:
        form = Postform()

    context['form'] = form
    return render(request, 'create_post.html', context=context)

@login_required(login_url='login')
def update_post(request, id):
    context = {}
    instance = get_object_or_404(Post, id=id)
    form = Updateform(request.POST, request.FILES,instance=instance)
    if(Post.objects.filter(author=request.user,id=id)):
        if form.is_valid():
            form.instance.created_on = time.strftime(r"%Y-%m-%d", time.localtime())
            form.save()
            response = redirect('/dashboard')
            return response
        else:
            form = Updateform(request.POST or None, instance=instance)
        context['form'] = form
        return render(request, 'update_post.html', context=context)
    else:
        messages.info(request,'401 Not Authorized')
        return render(request, 'errors.html')

@login_required(login_url='login')
def dashboard(request):
    posts = Post.objects.filter(author=request.user)

    context = {
        'posts': posts
    }
    return render(request, 'datatable.html', context=context)

@login_required(login_url='login')
def delete_post(request,pk):
    if request.method=='POST':
        if(Post.objects.filter(author=request.user)):
            record=Post.objects.get(id=pk)
            record.delete()
            response = redirect('/dashboard')
            return response
        else:
            return redirect('index')
    else:
        return redirect('dashboard')

@login_required(login_url='login')
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

@login_required(login_url='login')
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
    
def register(request):
    form = CreateUserForm(request.POST or None)
    if form.is_valid():
        form.save()
        return redirect('login')
    else:
        form = CreateUserForm()

    context = {'form':form}

    return render(request,'registration/register.html',context)

def login_view(request):
    context={}
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('dashboard')
        else:
            messages.info(request,'username or password is incorrect')
            form = LoginForm()
            context = {'form':form}
    else:
        form = LoginForm()
        context = {'form':form}

    return render(request,'registration/login.html',context)

def logout_view(request):
    logout(request)
    return redirect('login')