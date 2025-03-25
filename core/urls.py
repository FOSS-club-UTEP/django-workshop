from django.urls import path
from . import views

urlpatterns = [
    path("blog/<slug:slug>/", views.blog_detail, name="blog_detail"),
    path("", views.landing_page, name="landing"),
    path("new_blog/", views.new_blog, name="new_blog")
]
