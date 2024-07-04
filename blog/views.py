from django.shortcuts import redirect, render
from django.http import HttpResponse
from .models import (Blog, Category, CustomUser as User, Comments, Contact, Profile)
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from datetime import timedelta
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import uuid
from .helpers import *
# Create your views here.

def index(request):
    
    is_feature = Blog.objects.filter(is_featured=True).order_by('-id')[:1]
    blog_obj = Blog.objects.all().order_by('-id')
    active_category = Category.objects.filter(is_active=True)
    
    if request.method == 'POST':
        search = request.POST.get('search')
        if search:
            blog_obj = Blog.objects.filter(
                Q(title__icontains=search) |
                Q(author_name__icontains=search)
            ).distinct()
            
    try:
        paginated_blog = Paginator(blog_obj, 6)
        page = request.GET.get('page')
        blog_objs = paginated_blog.get_page(page)
    except PageNotAnInteger:
        blog_objs = paginated_blog.page(1)
    except EmptyPage:
        blog_objs = paginated_blog.page(paginated_blog.num_pages)
        
    context = {
        'is_feature': is_feature,
        'blog_objs': blog_objs,
        'active_category': active_category
    }
        
    return render(request, 'index.html', context)

def blogs(request):
    blog_obj = Blog.objects.all().order_by('-id')
    active_category = Category.objects.filter(is_active=True)
    
    context = {
        'blog_obj': blog_obj,
        'active_category': active_category
    }
    return render(request, 'blogs.html', context)

def blog_by_category(request, blog_slug):
    category = get_object_or_404(Category, slug=blog_slug)
    blog_obj = Blog.objects.filter(category=category)
    active_category = Category.objects.filter(is_active=True)
    
    context = {
        'category': category,
        'blog_obj': blog_obj,
        'active_category': active_category
    }
    return render(request, 'blogs.html', context)

def blog_detail(request, slug):
    
    blog = get_object_or_404(Blog, slug=slug)
    active_category = Category.objects.filter(is_active=True)
    comments = Comments.objects.filter(blog=blog)
   
    if request.method == 'POST':
        comment_text = request.POST.get('comment')
        
        if request.user.is_authenticated and comment_text:
            comment_obj = Comments.objects.create(
                user=request.user,
                comment=comment_text,
                blog=blog
            )
            comment_obj.save()
            messages.success(request, 'Comment added successfully')
        else:
            messages.error(request, 'You must be logged in to post a comment.')
        return redirect('blog-detail', slug=slug)
    
    context = {
        'blog_slug': blog,
        'active_category': active_category,
        'comments': comments
    }
    return render(request, 'blog-detail.html', context)

def signup(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email =  request.POST.get('email')
        password = request.POST.get('password')
        speical_char = ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '=']
        
        if len(password) < 8 and not any(char in speical_char for char in password):
            messages.error(request, "Password must be atleast 8 characters and must contain special characters")
            return redirect('signup')
        
        if User.objects.filter(email = email).exists():
            messages.error(request, "Account already exists")
            return redirect('signup')
        
        user = authenticate(email = email, password = password, first_name = name)
        if user is None:
            messages.info(request, "invalid Email and Password")
            
        user_obj = User.objects.create(
            first_name = name,
            email = email
        )
        user_obj.set_password(password)
        user_obj.save()
        login(request, user_obj)
        return redirect('/')
            
        
    return render(request, 'signup.html')

def login_page(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')
       
        user = authenticate(email = email, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'invalid Email and Password')
            return redirect('login')
       
    return render(request, 'login.html')

def dashboard(request):
    creator_obj = Blog.objects.filter(user=request.user)
    context = {
        'creator_obj': creator_obj
    }       
    return render(request, 'dashboard.html', context)

def add_blog(request):
    categories = Category.objects.all()
    
    if request.method == "POST":
        user = request.user
        title = request.POST.get('title')
        author_name = request.POST.get('author_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')

        category = Category.objects.get(id=category_id)
        
        blog_obj = Blog.objects.create(
            user=user,
            title=title,
            author_name=author_name,
            description=description,
            category=category,
            image=image,
        )
        messages.success(request, 'Blog added successfully')
        return redirect('dashboard')

    context = {
        'categories': categories
    }
    return render(request, 'add-blog.html', context)

def view_blog(request, slug):
    
    view_obj = get_object_or_404(Blog, slug=slug)
    
    context = {
        'view_obj': view_obj
    
    }
    return render(request, 'view-blog.html', context)

def edit_blog(request, slug):
    categories = Category.objects.all()
    edit_obj = get_object_or_404(Blog, slug=slug)
    
    if request.method == "POST":
        title = request.POST.get('title')
        author_name = request.POST.get('author_name')
        description = request.POST.get('description')
        category_id = request.POST.get('category')
        image = request.FILES.get('image')
        
        category = Category.objects.get(id=category_id)
        
        edit_obj.title = title
        edit_obj.author_name = author_name
        edit_obj.description = description
        edit_obj.category = category
        
        if image:
            edit_obj.image = image
        
        edit_obj.image = image
        
        edit_obj.save()
        
        messages.success(request, 'Blog updated successfully')
        return redirect('dashboard')
    
    context = {
        'edit_obj': edit_obj,
        'categories': categories
    }
    return render(request, 'edit-blog.html', context)

def delete_blog(request, slug):
    delete_obj = Blog.objects.get(slug=slug)    
    delete_obj.delete()
    messages.success(request, 'Blog deleted successfully')
    return redirect('dashboard')

def about(request):
    return render(request, 'about.html')

def contact(request):
    if request.method == "POST":
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')
        
        contact_obj = Contact.objects.create(
            name = name,
            email = email,
            message = message
        )
        contact_obj.save()
        messages.success(request, 'your record has been summitted')
        return redirect('contact')
    return render(request, 'contact.html')

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comments, id=comment_id)
    if request.user == comment.user:
        comment.delete()
        messages.success(request, 'Comment deleted successfully.')
    else:
        messages.error(request, 'You are not authorized to delete this comment.')
    return redirect('blog-detail', slug=comment.blog.slug)

def forget_password(request):
    try:
      if request.method == "POST":
          email = request.POST.get('email')
          
          if not User.objects.filter(email = email).exists():
              messages.info(request, 'Email does not exists')
              return redirect("forget_password")
          
          user_obj = User.objects.get(email=email)
          token = str(uuid.uuid4())
            
          profile_obj, created = Profile.objects.get_or_create(user=user_obj)
          profile_obj.forget_token = token
          profile_obj.save()  
          send_email(user_obj.email, token)  
          messages.success(request, 'An email has been sent.')
          return redirect('forget_password')
      
    except Exception as e:
        print(e)
    return render(request, 'forget_password.html')

def change_password(request, token):
    
    # Retrieve the Profile object associated with the provided token
    profile_obj = Profile.objects.filter(forget_token=token).first()
    
    # Check if the request method is POST
    if request.method == "POST":
        # Retrieve the password and confirm_password from the POST data
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        
        # Check if the password matches the confirm_password
        if password != confirm_password:
            # If passwords don't match, display a message and redirect back to the change password page
            messages.info(request, 'Password does not match')
            return redirect(f'change_password{token}')
        elif len(password) != 8 or not any(char in ['!', '@', '#', '$', '%', '^', '&', '*', '(', ')', '_', '+', '='] for char in password):
            messages.error(request, 'Password must be atleast 8 characters and must contain special characters')
            return redirect(f'change_password{token}')
        else:
            # Retrieve the User object associated with the profile's email
            user_obj = User.objects.get(email=profile_obj.user.email)
            
            # Set the new password for the user
            user_obj.set_password(password)
            
            # Save the user object with the new password
            user_obj.save()
            
            # Display a success message and redirect to the login page
            messages.info(request, 'Password has been changed successfully')
            return redirect('login')        
    return render(request, 'change_password.html')

def logout_user(request):
    logout(request)
    return redirect('/')