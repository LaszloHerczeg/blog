from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect

from .forms import RegisterForm, LoginForm, UserForm
from .models import Post

"""
    def index(request):
        return HttpResponse("Index page")
        """

"""
    def index(request):
        latest_post_list = Post.objects.order_by("-pub_date")[:5]
        template = loader.get_template("blog/index.html")
        context = {"latest_post_list": latest_post_list}
        return HttpResponse(template.render(context, request))
        """

def index(request):
    """
    Index view

    Parameters:
        request: HttpRequest object

    Returns:
        HttpResponse containing a blog/index.html template
    """
    return render(request, "blog/index.html")

def blog(request):
    """
    Index view

    Parameters:
        request: HttpRequest object

    Returns:
        HttpResponse containing the last 5 published posts and a blog/index.html template
    """
    # TODO: Shows not published articles when the number of published posts are less than 5
    latest_post_list = Post.objects.order_by("-published")[:5]
    context = {"latest_post_list": latest_post_list}
    return render(request, "blog/blog.html", context)


"""
def detail(request, post_id):
    try:
        post = Post.objects.get(pk=post_id)
    except Post.DoesNotExist:
        raise Http404("Post does not exist")
    return render(request, "blog/detail.html", {"post": post})
    """

def detail(request, post_id):
    """
    Detail view

    Parameters:
        request: HttpRequest object
        post_id: The id of the post requested

    Returns:
        An HttpResponse object containing the requested post and a blog/detail.html template
    """
    post = get_object_or_404(Post, pk=post_id)
    return render(request, "blog/detail.html", {"post": post})

def projects(request):
    """
    About view

    Parameters:
        request: HttpRequest object

    Returns:
        HttpResponse containing blog/projects.html template
    """
    return render(request, "blog/projects.html")

def about(request):
    """
    About view

    Parameters:
        request: HttpRequest object

    Returns:
        HttpResponse containing blog/about.html template
    """
    return render(request, "blog/about.html")

def registration(request):
    # TODO: checking if the passwords are the same
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data.get("username")
            first_name = form.cleaned_data.get("first_name")
            last_name = form.cleaned_data.get("last_name")
            email = form.cleaned_data.get("email")
            password = form.cleaned_data.get("password")
            password_confirmation = form.cleaned_data.get("password_confirmation")
            try:
                user = User.objects.create_user(
                    username = username,
                    email = email,
                    password = password,
                    first_name=first_name,
                    last_name = last_name,
                )
                login(request, user)
                messages.success(request, f"Successfully logged in, {username}!")
            except IntegrityError:
                form.add_error("username", "Username already exists")
            return redirect("blog:index")

    else:
        form = RegisterForm()

    return render(request, "blog/account/registration.html", {"form": form})

@login_required
def profile(request):
    return render(request, "blog/account/profile.html")

@login_required
def profile_edit(request):
    if request.method == "POST":
        form = UserForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect("blog:profile")
    else:
        form = UserForm(instance=request.user)

    return render(request, "blog/account/profile_edit.html", {"form": form})