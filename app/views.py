from django.shortcuts import render

# Create your views here.
from django.shortcuts import render, get_object_or_404, redirect
from django.utils import timezone
from .models import Blog, Comment
from django.core.paginator import Paginator
from .forms import BlogPost, CommentForm

def blog(request):
    blogs = Blog.objects
    blog_list = Blog.objects.all()
    paginator = Paginator(blog_list,3)
    page = request.GET.get('page')
    posts = paginator.get_page(page)
    return render(request, 'blog.html',{'blogs' : blogs, 'posts': posts})

def detail(request, blog_id):
        blog_detail = get_object_or_404(Blog,pk=blog_id)
        return render(request,'app/detail.html',{'blog':blog_detail})

def new(request):
    return render(request,'app/new.html')

def create(request):
    blog = BLog()
    blog.title = request.GET['title']
    blog.body = request.GET['body']
    blog.pub_date = timezone.now()
    blog.save()
    return redirect('/blog/'+str(blog.id))

def blogpost(request):
    if request.method == 'POST':
        form = BlogPost(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.pub_date = timezone.datetime.now()
            post.save()
            return redirect ('blog')
    else:
        form = BlogPost()
        return render(request,'app/new.html',{'form':form})

def comment(request, blog_id):
        post = get_object_or_404(Blog, pk=blog_id)
        if request.method == 'POST':
           form = CommentForm(request.POST)
           if form.is_valid():
                comment = form.save(commit=False)
                comment.post = post
                #comment.created_date = timezone.datetime.now()
                comment.save()
                return redirect ('/' + str(post.id))   
        else:
            form = CommentForm()
        return render(request,'app/comment.html',{ 'form':form})