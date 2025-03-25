# Django Workshop Steps

- add common django junk to gitignore:
```
# .gitignore
# django stuff
*.sqlite3
migrations/
```
- `django-admin startproject django_tutorial .`
---
- `python manage.py startapp core`
```python
# settings.py
INSTALLED_APPS = [
    "core",
    # ...
]
```
# landing page
- make landing page tempalte:
```html
<!-- templates/base.html -->
<!DOCTYPE html>
<html lang="en">
	<head>
		<meta charset="UTF-8" />
		<meta name="viewport" content="width=device-width, initial-scale=1.0" />
		<title>{% block title %}My Site{% endblock %}</title>
	</head>
	<body>
		<header>
			<nav>
				{% comment %} TODO: we'll add these later... {% endcomment %}
			</nav>
		</header>
		<div class="content">{% block content %} {% endblock %}</div>
		<footer>
			<p>&copy; 2023 My Site</p>
		</footer>
	</body>
</html>
```

```html
<!-- templates/landing.html -->
{% extends "base.html" %} 

{% block title %}
	Landing Page
{% endblock %} 

{% block content %}
	<h1>Welcome to this Django Blog Tutorial!</h1>
{% endblock %}
```
- add views:
```python
from django.shortcuts import render
from django.shortcuts import render, get_object_or_404


def landing_page(request):
    return render(request, "landing.html")
```
- add urls
```python
from django.urls import path
from . import views

urlpatterns = [
    path("", views.landing_page, name="landing"),
]
```
- add this to the main `urls.py`:
``` python
from django.urls import path, include

urlpatterns = [
	# ...
    path("", include("core.urls")),
]
```
# new blog page
- make the model
```python
# core/models.py
class Blog(models.Model):
    title = models.CharField(max_length=200)
    slug = models.SlugField(unique=True) # explain this
    content = models.TextField()
    author = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
```
- make the form (forms.py)
```python
from django import forms
from .models import Blog


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = "__all__"
```
- make the template: `newpost.html`
```html
{% extends "base.html" %} 

{% block title %}
	New Blog Entry
{% endblock %} 

{% block content %}
	<h1>Create a New Blog Entry</h1>
	<form method='POST'>
	    {% csrf_token %}
	
		{% for field in form %}
	    <div>
	        {{ field.label_tag }}
	        {{ field }}
	        <div style="color: red;">
	            {{ field.errors }}  <!-- This ensures errors are shown -->
	        </div>
	    </div>
	    {% endfor %}
	
	    <button type="submit">Submit</button>
	</form>
{% endblock %}
```
- make view:
```python
# new imports!!
from django.http import HttpResponseRedirect
from django.urls import reverse
from .forms import BlogForm
from .models import Blog

# new view
def new_blog(request):
    if request.method == "POST":
        form = BlogForm(request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse("landing"))
    else:
        print("request was get...")
        form = BlogForm()
    return render(request, "newpost.html", {"form": form})
```
- add url mapping:
```python
urlpatterns = [
	# ...
    path("new_blog/", views.new_blog, name="new_blog")
]
```
- **every time you change your models, you have to "migrate"**
	- `python manage.py makemigrations`
	- `python manage.py migrate`
- now, try adding a blogpost
- then, try doing it again!!! - django handles errors for you.
# showing a single blog
- make the django templates
```html
<!-- templates/blogpost.html -->
{% extends 'base.html' %} 
{% block title %}
	{{ blog.title }}
{% endblock %} 

{% block content %}
	<article>
		<h1>{{ blog.title }}</h1>
		<p><strong>Author:</strong> {{ blog.author }}</p>
		<p><strong>Published on:</strong> {{ blog.created_at|date:"F j, Y" }}</p>
		<div>{{ blog.content|linebreaks }}</div>
	</article>
{% endblock %}
```
- add view
```python
# views.py
def blogpost(request, slug):
    blog = get_object_or_404(Blog, slug=slug)
    return render(request, "blogpost.html", {"blog": blog})
```
- add url
```python
# urls.py
path("blog/<slug:slug>/", views.blogpost, name="blogpost"),
```
# blog list page
- template in `allposts.html`
```html
{% extends "base.html" %} 

{% block title %}
	All Blog Posts
{% endblock %} 

{% block content %}
	<h1>All Blog Posts</h1>
	<ul>
		{% for blog in blogs %}
		<li onclick="location.href='{% url 'blogpost' blog.slug %}'" style="cursor: pointer">
			<h2>{{ blog.title }}</h2>
			<p>By {{ blog.author }} on {{ blog.created_at|date:"F j, Y" }}</p>
			<p>{{ blog.content|truncatewords:30 }}</p>
		</li>
		{% endfor %}
	</ul>
{% endblock %}
```
- make the view in views.py:
```python
def all_posts(request):
    blogs = Blog.objects.all()
    return render(request, "allposts.html", {"blogs": blogs})
```
- add to urls.py:
```python
urlpatterns = [
	# ...
    path("all_posts/", views.all_posts, name="all_posts"),
]
```
# add links to base
- add these under "nav" in the base template:
``` html
<a href="{% url 'all_posts' %}">All Posts</a>
<a href="{% url 'landing' %}">Home</a>
```
