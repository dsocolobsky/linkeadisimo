from http import HTTPStatus
from urllib.parse import urlparse

from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.http import require_http_methods, require_safe

from website.forms import (
    SubmitForm,
    LoginForm,
    CommentForm,
    RegisterForm,
    EditCommentForm,
)
from website.models import Publication, Comment


@require_safe
def index(request):
    publications = Publication.objects.order_by("-created_at")
    context = {
        "publications": publications,
        "user": (request.user if request.user.is_authenticated else None),
        "authenticated": request.user.is_authenticated,
    }
    return render(request, "website/pages/index.html", context)


@require_safe
def health(request):
    return HttpResponse(status=HTTPStatus.OK)


@require_safe
def publication(request, pub_id):
    pub = get_object_or_404(Publication, pk=pub_id)
    context = {"publication": pub, "form": CommentForm()}
    return render(request, "website/pages/publication.html", context)


@require_safe
def user(request, user_id):
    return HttpResponse("user")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
