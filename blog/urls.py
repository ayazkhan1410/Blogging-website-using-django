from django.urls import path
from . import views

urlpatterns = [
   
   path('', views.index, name='home'),
   
   # Blogs
   path('blogs', views.blogs, name='blogs'),
   path('blog-by-category/<str:blog_slug>', views.blog_by_category, name='blog-by-category'),
   path('blog-detail/<str:slug>', views.blog_detail, name='blog-detail'),
   path('comment/<int:comment_id>/delete/', views.delete_comment, name='delete_comment'),

   # Auth
   path('signup', views.signup, name='signup'),
   path('login', views.login_page, name='login'),
   path('logout', views.logout_user, name='logout'),
   path('forget_password', views.forget_password, name='forget_password'),
   path('change_password/<token>/', views.change_password, name='change_password'),
   # CRUD
   path('dashboard', views.dashboard, name='dashboard'),
   path('add-blog', views.add_blog, name='add-blog'),
   path('view-blog/<str:slug>', views.view_blog, name='view-blog'),
   path('edit-blog/<str:slug>', views.edit_blog, name='edit-blog'),
   path('delete-blog/<str:slug>', views.delete_blog, name='delete-blog'),
   
   # About
   path('about', views.about, name='about'),
   #contact
   path('contact', views.contact, name='contact'),

]
