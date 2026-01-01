"""NewsPortal URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from news.views import *
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', Home, name='home'),
    path('about',about, name='about'),
    path('contact',contact, name='contact'),
    path('login',adminlogin,name='login'),
    path('changepassword',changepassword,name='changepassword'),
    path('admin_home',admin_home,name='admin_home'),
    path('logout',Logout,name='logout'),
    path('about/',about, name='about'),
    path('contact/',contact, name='contact'),
    path('login/',adminlogin,name='login'),
    path('changepassword/',changepassword,name='changepassword'),
    path('admin_home/',admin_home,name='admin_home'),
    path('logout/',Logout,name='logout'),

    path('add_category',add_category,name='add_category'),
    path('view_category',view_category,name='view_category'),
    path('delete_category/<int:pid>', delete_category,name='delete_category'),
    path('add_post',add_post,name='add_post'),
    path('view_post',view_post,name='view_post'),
    path('delete_post/<int:pid>', delete_post,name='delete_post'),
    path('post_detail/<int:pid>', post_detail,name='post_detail'),
    path('categorynews/<int:pid>',categorynews,name='categorynews'),
    path('news_detail/<int:pid>',news_detail,name='news_detail'),
path('unread_queries',unread_queries, name='unread_queries'),
    path('read_queries', read_queries, name='read_queries'),
    path('view_queries/<int:pid>',view_queries, name="view_queries"),
    path('search',search, name='search'),

path('unapproved_comment',unapproved_comment, name='unapproved_comment'),
    path('approved_comment',approved_comment, name='approved_comment'),
    path('view_commentdetail/<int:pid>',view_commentdetail, name="view_commentdetail"),
path('delete_comment/<int:pid>', delete_comment,name='delete_comment'),

]+static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
