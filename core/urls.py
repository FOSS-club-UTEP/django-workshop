from django.urls import path
from . import views

urlpatterns = [
    path("post/<slug:slug>/", views.blogpost, name="blogpost"),
    path("", views.landing_page, name="landing"),
    path("new_post/", views.new_post, name="new_post"),
    path("all_posts/", views.all_posts, name="all_posts"),
]
