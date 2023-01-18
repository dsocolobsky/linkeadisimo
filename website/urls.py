from django.urls import path

from .views.comment import CommentView, edit_comment
from .views.login import Login
from .views.register import Register
from .views.submit import Submit
from .views.views import health, index, publication, user, logout_view

urlpatterns = [
    path("", index, name="index"),
    path("health", health, name="health"),
    path("pub/<int:pub_id>/", publication, name="publication"),
    path("user/<int:user_id>/", user, name="user"),
    path("submit", Submit.as_view(), name="submit"),
    path("logout_view", logout_view, name="logout_view"),
    path("login", Login.as_view(), name="login"),
    path("comment", CommentView.as_view(), name="comment"),
    path(
        "comment/<int:comment_id>/", CommentView.as_view(), name="comment_delete"
    ),
    path("comment/<int:comment_id>/edit/", edit_comment, name="comment_edit"),
    path("register", Register.as_view(), name="register"),
]
