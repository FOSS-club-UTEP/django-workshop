from django.shortcuts import render, get_object_or_404
from .models import Blog
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BlogForm


def blogpost(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, "blogpost.html", {"blog": blog})


def landing_page(request):
    return render(request, "landing.html")


def new_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("landing"))
    else:
        print("request was get...")
        form = BlogForm()
    return render(request, "newblog.html", {"form": form})


def all_posts(request):
    blogs = Blog.objects.all()
    return render(request, "allposts.html", {"blogs": blogs})
