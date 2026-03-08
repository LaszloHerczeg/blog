from django.urls import path
from . import views

app_name = 'blogs'
urlpatterns = [
    # ex:/blogs/
    path("", views.index, name="index"),
    # ex:/blogs/1
    path("<int:post_id>/", views.detail, name="detail"),
]