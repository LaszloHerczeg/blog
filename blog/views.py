from django.contrib import messages
from django.contrib.auth import login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.db.models import Q
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.views import generic

from .forms import RegisterForm, LoginForm, UserForm, SearchForm
from .models import Post

class PostListView(generic.ListView):
    paginate_by = 6
    model = Post
    context_object_name = "post_list"
    template_name = "blog/blog.html"

    def get_queryset(self):
        queryset = Post.objects.filter(status__exact="published").order_by("-published")
        form = SearchForm(self.request.GET)
        if form.is_valid():
            query = form.cleaned_data.get("query")
            field = form.cleaned_data.get("field")

            if query:
                if field == "all":
                    queryset = (queryset.filter(Q(title__icontains=query) |
                                               Q(body__icontains=query) |
                                               Q(tags__name__icontains=query) |
                                               Q(category__name__icontains=query))
                                    .distinct())
                elif field == "title":
                    queryset = queryset.filter(title__icontains=query)

                elif field == "content":
                    queryset = queryset.filter(body__icontains=query)

                elif field == "title and content":
                    queryset = queryset.filter(
                        Q(title__icontains=query) | Q(body__icontains=query)
                    )

                elif field == "tags":
                    queryset = queryset.filter(tags__name__icontains=query)

                elif field == "category":
                    queryset = queryset.filter(category__name__icontains=query)

        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["form"] = SearchForm(self.request.GET)
        return context

class PostDetailView(generic.DetailView):
    model = Post
    template_name = "blog/detail.html"
    context_object_name = "post"

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
            messages.success(request, "Your details have been saved.")
            return redirect("blog:profile")
    else:
        form = UserForm(instance=request.user)

    return render(request, "blog/account/profile_edit.html", {"form": form})