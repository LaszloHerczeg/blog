from django.conf import settings
from django.conf.urls.static import static
from django.urls import path
from . import views

app_name = 'blog'
urlpatterns = [
    # ex:/
    path("", views.index, name="index"),
    # ex:/blog
    path("blog/", views.blog, name="blog"),
    # ex:/blog/1
    path("blog/<int:post_id>/", views.detail, name="detail"),
    # ex:/projects
    path("projects/", views.projects, name="projects"),
    # ex:/blog/about/
    path("about/", views.about, name="about"),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)