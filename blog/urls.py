from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include, reverse_lazy
from . import views
from django.contrib.auth import views as auth_views

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

    # ex:/about/
    path("about/", views.about, name="about"),

    # ex:/account/registration/
    path("account/registration/", views.registration, name="registration"),

    # ex:/account/login
    path("account/login/", auth_views.LoginView.as_view(template_name="blog/account/login.html"), name="login"),

    # ex:/account/logout
    path("account/logout/",
         auth_views.LogoutView.as_view(
             template_name="blog/account/logged_out.html",
         ), name="logout"),

    # ex:/account/profile
    path("account/profile/", views.profile, name="profile"),

    # ex:/account/profile-edit
    path("account/profile-edit/", views.profile_edit, name="profile_edit"),

    # ex:/account/password-reset/
    path("account/password-reset/",
        auth_views.PasswordResetView.as_view(
            template_name="blog/account/password_reset_form.html",
            email_template_name="blog/account/password_reset_email.html",
            success_url=reverse_lazy("blog:password_reset_done"),
        ),
        name="password_reset"),

    # ex:/account/password-reset/done/
    path("account/password-reset/done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="blog/account/password_reset_done.html",
        ),
        name="password_reset_done"),

    # ex:/account/reset/<uidb64>/<token>/
    path("account/reset/<uidb64>/<token>/",
        auth_views.PasswordResetConfirmView.as_view(
        template_name="blog/account/password_reset_confirm.html",
        success_url=reverse_lazy("blog:password_reset_complete"),
     ),
     name="password_reset_confirm"),

    # ex:/account/reset/done
    path("account/reset/done/",
        auth_views.PasswordResetCompleteView.as_view(
        template_name="blog/account/password_reset_complete.html",
     ),
    name="password_reset_complete"),

    # ex:/account/password-change
    path("account/password-change/",
         auth_views.PasswordChangeView.as_view(
             template_name="blog/account/password_change_form.html",
             success_url=reverse_lazy("blog:password_change_done"),                                  ),
         name="password_change"),

    # ex:/account/password-change-done
    path("account/password-change/done/",
         auth_views.PasswordChangeDoneView.as_view(
             template_name="blog/account/password_change_done.html",
         ),
         name="password_change_done"),

    # path("account/", include("django.contrib.auth.urls")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)