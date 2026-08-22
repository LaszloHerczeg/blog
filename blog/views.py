from django.http import HttpResponse, Http404
from django.template import loader
from django.shortcuts import get_object_or_404, render
from .models import Post

# Create your views here.

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