from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import *
from .models import *


def HomeView(request):
    yaxshi_post = CreatePostModel.objects.filter(turi='yaxshi')
    yomon_post = CreatePostModel.objects.filter(turi='yomon')
    yaxshi_count = yaxshi_post.count()
    yomon_count = yomon_post.count()
    
    ctx = {
        'yaxshi':yaxshi_post,
        'yomon':yomon_post,
        'yaxshi_count':yaxshi_count,
        'yomon_count':yomon_count
    }
    
    return render(request,'home.html',ctx)


def LoginView(request):
    
    if request.POST:
        userName = request.POST['username']
        userPassword = request.POST['password']
        user = authenticate(request,username=userName,password=userPassword)
        if user is not None:
            login(request,user)
            return redirect('/')
        else:
            return redirect('login')
        
    return render(request,'login.html')


def LogoutView(request):
    logout(request)
    return render(request,'home.html')



def RegisterView(request):
    if request.POST:
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Siz registratsiyadan muvaffaqiyatli otdingiz !!!')
            return redirect('login')
        else:
            messages.error(request,'Afsuski registratsiyadan otmadingiz')
            return redirect('register')
    
    form = RegisterForm()    
    
    ctx = {
            'forms':form
           }
    
    return render(request,'register.html',ctx)


@login_required(login_url="/register/")
def ProfileView(request,pk):
    user_edit = ProfileModel.objects.get(user_id=pk)
    if request.POST:
        form = ProfileForm(request.POST, request.FILES, instance=user_edit)
        if form.is_valid():
            form.save()
            messages.success(request,"Profilingiz muvaffaqiyatli o'zgartirildi !!!")
            return redirect('/')
        else:
            messages.error(request,'Afsuski xatolik bor !!!')
            return redirect('profil', pk=user_edit.user_id)
        
        
    form = ProfileForm(instance=user_edit)
    
    ctx={
        'form':form
    }
    
    return render(request,'profile.html',ctx)


@login_required(login_url="/register/")
def CreatePostView(request,pk):
    post_id = ProfileModel.objects.get(user_id=pk)
    if request.POST:
        form = CreateForm(request.POST,request.FILES)
        if form.is_valid():
            profil_title = form.cleaned_data['title']
            profil_text = form.cleaned_data['information']
            profil_image = form.cleaned_data['image']
            profil_turi = form.cleaned_data['turi']
            form_data = CreatePostModel(user=post_id,title=profil_title,information=profil_text,image=profil_image,turi=profil_turi)
            form_data.save()
            messages.success(request,'Yangi post chiqarildi')
            return redirect('/')
        else:
            messages.error(request,'Afsuski postingiz saqlanmadi !!!')
            
    form = CreateForm()
    
    ctx = {
        'form':form
    }
    
    return render(request,'create_post.html',ctx)



@login_required(login_url="/register/")
def PostsView(request,pk):
    
    user_posts = CreatePostModel.objects.filter(user_id=pk)
    user_count = user_posts.count()
    
    ctx = {
        'posts':user_posts,
        'user_count':user_count
    }
    
    return render(request,'posts.html',ctx)



@login_required(login_url="/register/")
def EditpostView(request,pk):
    editpost = CreatePostModel.objects.get(id=pk)
    if request.POST:
        form = CreateForm(request.POST,request.FILES,instance=editpost)
        if form.is_valid():
            form.save()
            messages.success(request,"Post muvaffaqiyatli o'zgartirildi ")
            return redirect('posts',request.user.id)
        else:
            messages.error(request,"Barchasini to'ldiring !")
        
    form = CreateForm(instance=editpost)
    ctx={
        'form':form,
        'pk':pk
    }
    
    return render(request,'edit_post.html',ctx)


@login_required(login_url="/register/")
def DeletepostView(request,pk):
    deletepost = CreatePostModel.objects.get(id=pk)
    deletepost.delete()
    
    return redirect('posts',request.user.id)



@login_required(login_url="/register/")
def CommentView(request,pk):
    post_s = CreatePostModel.objects.get(id=pk)
    if request.POST:
        form = CommentForm(request.POST)
        if form.is_valid():
            data = form.save(commit=True)
            data.post = CreatePostModel.objects.get(id=pk)
            data.user = ProfileModel.objects.get(id=request.user.id)
            data.save()
            return redirect('comment',pk)
        else:
            return redirect('comment',pk)
        
    form = CommentForm()
    forms = CommentModel.objects.filter(post_id=pk)
    forms_count = forms.count()
    
    ctx = {
        'forms':forms,
        'form':form,
        'posts':post_s,
        'count':forms_count
    }
    return render(request,'comment.html',ctx)



@login_required(login_url="/register/")
def EditCommentView(request,pk):
    edit_comment = CommentModel.objects.get(id=pk)
    if request.POST:
        form = CommentForm(request.POST,instance=edit_comment)
        if form.is_valid():
            form.save()
            data = form.save(commit=True)
            return redirect('comment',data.post.id)
        else:
            messages.error(request,'error')
    
    form = CommentForm(instance=edit_comment)
    ctx = {
        'form':form,
        'pk':pk
    }
    
    return render(request,'edit_comment.html',ctx)

    

