from django.urls import path
from . import views

urlpatterns = [
    path("blog/<slug:slug>/", views.blogpost, name="blogpost"),
    path("", views.landing_page, name="landing"),
    path("new_blog/", views.new_blog, name="new_blog"),
    path("all_posts/", views.all_posts, name="all_posts"),
]
