from django.db import models
from django.db.models import SET_NULL
from django.utils import timezone
import datetime
from django.conf import settings

# Create your models here.

class Category(models.Model):
    """
    This model is the categories used for posts

    Parameters:
        name
        slug
    """
    name = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)

class Tag(models.Model):
    """
    Stores tags used for posts

    Parameters:
        name
        slug
    """
    name = models.CharField(max_length=10)
    slug = models.CharField(max_length=10)

class Post(models.Model):
    """
    This model represents the blog posts.

    Related models:
    - :model:`auth.User`
    - :model:`blogs.Category`
    - :model:`blogs.Tag`

    Parameters
    ----------
    id:
    post_title : str
        The title of the post.
    post_body : str
        The main content of the post.
    pub_date : date
        The publication date.
    author : User
        The user who wrote the post.
    slug : str
        URL-friendly identifier for the post.
    category : Category
        The category this post belongs to.
    tags : Tags
        The tags assigned to this post.
    feature_image : Image
        Featured image for the post.
    excerpt : str
        Short summary or preview of the post.
    status : str
        Draft/Published/Archived status of the post.
    """

    post_title = models.CharField(max_length=200, blank=True, null=True, help_text="A short title, max 200 characters")
    post_body = models.CharField(max_length=1000, help_text="The body of the post")
    pub_date = models.DateTimeField("date published", help_text="The date of the publication")
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, help_text="The author of the post, Foreign key")
    slug = models.CharField(max_length=100, blank=True, null=True, help_text="A short slug")
    category = models.ForeignKey(Category, blank=True, null=True, on_delete=SET_NULL, help_text="The category of the post, 1 can be used maximum to 1 post, Foreign key")
    tags = models.ManyToManyField(Tag, blank=True, help_text="The tags of the post, multiple can be used for a post, ManyToManyField")
    featured_image = models.ImageField(upload_to="featured_images/", blank=True, null=True, help_text="Path to the featured image")
    excerpt = models.CharField(max_length=100, blank=True, null=True, help_text="The content of the body in a short form")
    status = models.CharField(choices= [("draft", "Draft"), ("published", "Published"), ("archived", "Archived")], blank=True, null=True, help_text="The status of the post. Can be: draft,published or archived")
    # comments
    # reviews
    # reading time
    # view count
    # related posts


    def __str__(self):
        return f'Title: {self.post_title} - Text: {self.post_body}'

    def is_recently_published(self):
        pass