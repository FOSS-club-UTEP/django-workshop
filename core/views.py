from django.shortcuts import render, get_object_or_404
from .models import BlogPost
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import NewBlogpostForm


def blogpost(request, slug):
    post = get_object_or_404(BlogPost, slug=slug)
    return render(request, "blogpost.html", {"post": post})


def landing_page(request):
    return render(request, "landing.html")


def new_post(request):
    if request.method == "POST":
        form = NewBlogpostForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("landing"))
    else:
        print("request was get...")
        form = NewBlogpostForm()
    return render(request, "newpost.html", {"form": form})


def all_posts(request):
    posts = BlogPost.objects.all()
    return render(request, "allposts.html", {"posts": posts})
