import time
from django.conf import settings
from django.shortcuts import render
from .models import CommentReply, Like, Post, Comment
from .forms import CreateUserForm, LoginForm, Postform, Updateform, commentReplyForm, createComment
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required,user_passes_test


def logout_required(function=None, logout_url='index'):
    actual_decorator = user_passes_test(
        lambda u: not u.is_authenticated,
        login_url=logout_url
    )
    if function:
        return actual_decorator(function)
    return actual_decorator

@login_required(login_url='login')
def index(request):
    """View function for home page of site."""
    context={}
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
    if request.method =='POST':
        if form.is_valid():
            form.instance.author = request.user
            form.save()
            response = redirect('/')
            return response
        else:
            form = Postform(request.POST, request.FILES)
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
    if(Post.objects.filter(author=request.user)):
        record=Post.objects.get(id=pk)
        record.delete()
        response = redirect('/dashboard')
        return response
    else:
        return redirect('index')

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
    else:
        checkuser.delete()
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

@logout_required()
def login_view(request):
    context={}
    # if request.user:
        # return redirect('index')
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

@login_required(login_url='login')
def commentReply(request, id,commentid):
    post = Post.objects.get(id=id)
    comments=Comment.objects.get(id=commentid)
    comment_form = commentReplyForm(request.POST or None)
    if comment_form.is_valid():
        comment_form.instance.comment = comments
        comment_form.instance.user = request.user
        comment_form.save()
        comment_form = commentReplyForm()
        return redirect('comments',id=id,commentid=commentid)
    context = {
        'post': post,
        'choosenComment':comments,
        'comment_form': comment_form
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'comments.html', context=context)

@login_required(login_url='login')
def editComment(request, id,commentid):
    post = Post.objects.get(id=id)
    comments=Comment.objects.get(id=commentid)
    instance = get_object_or_404(Comment, id=commentid)
    comment_form = createComment(request.POST or None,instance=instance)
    if(comments.user!=request.user):
        return redirect('fullpost',id=id)
    if comment_form.is_valid():
        comment_form.save()
        comment_form = createComment()
        return redirect('fullpost',id=id)
    context = {
        'post': post,
        'choosenComment':comments,
        'comment_form': comment_form
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'editComment.html', context=context)

@login_required(login_url='login')
def deleteComment(request, id,commentid):
  if(Comment.objects.filter(user=request.user)):
        record=Comment.objects.get(id=commentid)
        record.delete()
        return redirect('fullpost',id=id)
  else:
       return redirect('fullpost',id=id)


@login_required(login_url='login')
def editReply(request, id,commentid, replyid):
    post = Post.objects.get(id=id)
    comments=Comment.objects.get(id=commentid)
    instance = get_object_or_404(CommentReply, id=replyid)
    comment_form = commentReplyForm(request.POST or None,instance=instance)
    chosenreply= CommentReply.objects.get(id=replyid)
    if comment_form.is_valid():
        comment_form.save()
        comment_form = commentReplyForm()
        return redirect('comments',id=id,commentid=commentid)
    context = {
        'post': post,
        'choosenComment':comments,
        'chosenreply':chosenreply,
        'comment_form': comment_form
    }
    # Render the HTML template index.html with the data in the context variable
    return render(request, 'editReply.html', context=context)

@login_required(login_url='login')
def deleteReply(request, id,commentid, replyid):
  if(CommentReply.objects.filter(user=request.user)):
        record=CommentReply.objects.get(id=replyid)
        record.delete()
        return redirect('comments',id=id,commentid=commentid)
  else:
       return redirect('comments',id=id,commentid=commentid)
