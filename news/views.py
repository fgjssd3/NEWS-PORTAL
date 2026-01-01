from django.shortcuts import render
from django.db.models import Q
from django.shortcuts import render,redirect
from .models import *
from django.contrib.auth.models import User
from django.contrib.auth import login,logout,authenticate
from django.contrib import messages
from datetime import date
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
# Create your views here.

def Home(request):
    category1 = Category.objects.all()
    last_records = Newspost.objects.all().order_by('-id')[:3]


    all_post = Paginator(Newspost.objects.all(),2)
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)

    d = {'category1': category1, 'last_records': last_records,'posts':posts}
    return render(request, 'index.html', d)




def categorynews(request,pid):
    category = Category.objects.get(id=pid)
    category1 = Category.objects.all()

    last_records = Newspost.objects.all().order_by('-id')[:3]

    all_post = Paginator(Newspost.objects.filter(category=category),2)
    postcount = Newspost.objects.filter(category=category).count()
    page = request.GET.get('page')
    try:
        posts = all_post.page(page)
    except PageNotAnInteger:
        posts = all_post.page(1)
    except EmptyPage:
        posts = all_post.page(all_post.num_pages)

    d = {'category1': category1,'category': category, 'last_records': last_records,'posts':posts,'postcount':postcount}
    return render(request, 'category.html', d)



def search(request):
    q = request.GET.get('q')
    newspost = Newspost.objects.filter(Q(posttitle__icontains=q) | Q(postdetail__icontains=q)).distinct()

    last_records = Newspost.objects.all().order_by('-id')[:3]
    category1 = Category.objects.all()

    d = {'newspost': newspost,'category1': category1,'last_records':last_records}
    return render(request, 'search.html',d)




def news_detail(request,pid):
    category1 = Category.objects.all()
    newspost = Newspost.objects.get(id=pid)
    comment = Comment.objects.filter(Q(newspost=newspost) & Q(status="Accept"))
    error = ""
    if request.method == 'POST':
        name = request.POST['name']
        emailid = request.POST['emailid']
        commentmsg = request.POST['commentmsg']
        cdate = date.today()
        status = "pending"
        try:
            Comment.objects.create(newspost=newspost,name=name, emailid=emailid,commentmsg=commentmsg, cdate=cdate,status=status)
            error = "no"
        except:
            error = "yes"

    d = {'category1': category1,'newspost':newspost,'comment':comment,'error':error}
    return render(request, 'news_detail.html', d)

def about(request):
    return render(request, 'about.html')

def contact(request):
    error = ""
    if request.method == 'POST':
        n = request.POST['name']
        e = request.POST['email']
        mn = request.POST['mobnum']
        msg = request.POST['message']
        try:
            Contact.objects.create(name=n, contact=mn, emailid=e,message=msg,mdate=date.today(),isread="no")
            error = "no"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'contact.html',d)


def adminlogin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error="no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'login.html',d)



def admin_home(request):
    if not request.user.is_authenticated:
        return redirect('login')
    totalnews = Newspost.objects.all().count()
    totalcategory = Category.objects.all().count()
    totalpcontact = Contact.objects.filter(isread="no").count()
    totalacontact = Contact.objects.filter(isread="yes").count()
    totalpcomment = Comment.objects.filter(status="pending").count()
    totalacomment = Comment.objects.filter(status="Accept").count()
    d = {'totalnews':totalnews,'totalcategory':totalcategory,'totalpcontact':totalpcontact,'totalacontact':totalacontact,'totalpcomment':totalpcomment,'totalacomment':totalacomment}
    return render(request, 'admin_home.html',d)






def Logout(request):
    logout(request)
    return redirect('home')


def changepassword(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method=="POST":
        o = request.POST['currentpassword']
        n = request.POST['newpassword']
        c = request.POST['confirmpassword']
        if c == n:
            u = User.objects.get(username__exact=request.user.username)
            u.set_password(n)
            u.save()
            error = "yes"
        else:
            error = "not"
    d = {'error':error}
    return render(request,'change_password.html',d)


def add_category(request):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    if request.method=="POST":
        cn = request.POST['catname']

        try:
            Category.objects.create(categoryname=cn)
            error = "no"
        except:
            error = "yes"
    d = {'error':error}
    return render(request, 'add_category.html', d)


def view_category(request):
    if not request.user.is_authenticated:
        return redirect('login')
    category = Category.objects.all()
    d = {'category': category}
    return render(request, 'view_category.html', d)

def delete_category(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    category = Category.objects.get(id=pid)
    category.delete()
    return redirect('view_category')



def add_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    category = Category.objects.all()
    error = ""
    if request.method=="POST":
        pt = request.POST['posttitle']
        c = request.POST['categoryname']
        pd = request.POST['postdetail']
        pi = request.FILES['postimage']
        postd = date.today()
        c1 = Category.objects.get(categoryname=c)
        try:
            Newspost.objects.create(posttitle=pt,category=c1,postdetail=pd,postimage=pi,postdate=postd)
            error = "no"
        except:
            error = "yes"
    d = {'error':error,'category':category}
    return render(request, 'add_post.html', d)


def view_post(request):
    if not request.user.is_authenticated:
        return redirect('login')
    newspost = Newspost.objects.all()
    d = {'newspost': newspost}
    return render(request, 'view_post.html', d)

def post_detail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error = ""
    category = Category.objects.all()
    newspost = Newspost.objects.get(id=pid)

    if request.method == 'POST':
        pt = request.POST['posttitle']
        c = request.POST['categoryname']
        pd = request.POST['postdetail']


        try:
            pi = request.FILES['postimage']
            newspost.postimage = pi
            newspost.save()

        except:
            pass

        if c:
            try:
                c1 = Category.objects.get(categoryname=c)
                newspost.category = c1
                newspost.save()
            except:
                pass
        else:
            pass

        newspost.posttitle = pt
        newspost.postdetail = pd
        newspost.save()
        error = "no"

    d = {'newspost': newspost,'category':category,'error':error}
    return render(request,'post_detail.html', d)

def delete_post(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    newspost = Newspost.objects.get(id=pid)
    newspost.delete()
    return redirect('view_post')


def unread_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.all()
    d = {'contact': contact}
    return render(request, 'unread_queries.html', d)

def read_queries(request):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.all()
    d = {'contact': contact}
    return render(request, 'read_queries.html', d)


def view_queries(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    contact = Contact.objects.get(id=pid)
    contact.isread = "yes"
    contact.save()
    d = {'contact':contact}
    return render(request, 'view_queries.html', d)


def unapproved_comment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    comment = Comment.objects.all()
    d = {'comment': comment}
    return render(request, 'unapproved_comment.html', d)


def approved_comment(request):
    if not request.user.is_authenticated:
        return redirect('login')
    comment = Comment.objects.all()
    d = {'comment': comment}
    return render(request, 'approved_comment.html', d)





def view_commentdetail(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    error=""
    comment = Comment.objects.filter(id=pid)
    if request.method=="POST":
        comment1 = Comment.objects.get(id=pid)
        s = request.POST['status']
        comment1.status = s
        try:
            comment1.save()
            error="no"
        except:
            error="yes"
    d = {'comment':comment,'error':error}
    return render(request, 'view_commentdetail.html', d)

def delete_comment(request,pid):
    if not request.user.is_authenticated:
        return redirect('login')
    comment = Comment.objects.get(id=pid)
    comment.delete()
    return redirect('unapproved_comment')


