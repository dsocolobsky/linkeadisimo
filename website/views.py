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

from .forms import SubmitForm, LoginForm, CommentForm, RegisterForm, EditCommentForm
from .models import Publication, Comment


# Create your views here.
def index(request):
    publications = Publication.objects.order_by("-created_at")
    if request.user.is_authenticated:
        context = {
            "publications": publications,
            "authenticated": True,
            "user": request.user,
        }
    else:
        context = {
            "publications": publications,
            "authenticated": False,
        }
    return render(request, "website/pages/index.html", context)


def health(request):
    return HttpResponse(status=HTTPStatus.OK)

def publication(request, pub_id):
    pub = get_object_or_404(Publication, pk=pub_id)
    context = {"publication": pub, "form": CommentForm()}
    return render(request, "website/pages/publication.html", context)


class CommentView(View):
    @method_decorator(login_required)
    def post(self, request):
        form = CommentForm(request.POST)

        if not form.is_valid():
            return HttpResponseBadRequest("<p>Form was invalid</p>")

        pubid = request.POST["pubid"]
        text = form.cleaned_data["text"]
        parentid = request.POST["parent"]
        parent = Comment.objects.get(pk=parentid) if parentid != "" else None
        level = parent.level + 1 if parent is not None else 0
        pub = get_object_or_404(Publication, pk=pubid)

        print(f"Saving comment with parent {parentid}")
        the_comment = Comment(
            text=text,
            publication=pub,
            created_by=request.user,
            parent_comment=parent,
            level=level,
        )
        the_comment.save()
        return render(
            request, "website/components/comment/comment.html", {"com": the_comment, "pub": pub}
        )

    @method_decorator(login_required)
    def delete(self, request, comment_id):
        comment = Comment.objects.get(pk=comment_id)
        if comment.created_by.id != request.user.id:
            return HttpResponseBadRequest("Unauthorized")
        comment.delete_comment()
        return HttpResponse(comment.text)  # Will return 'Deleted Comment'


def edit_comment(request, comment_id):
    # TODO very inefficient, we should avoid a DB hit for this GET. Solve in frontend
    if request.method == "GET":
        comment = Comment.objects.get(pk=comment_id)
        context = {
            "comment_id": comment_id,
            "form": EditCommentForm(initial={"text": comment.text}),
        }
        return render(request, "website/components/comment/comment_edit.html", context)
    elif request.method == "POST":
        form = EditCommentForm(request.POST)
        if form.is_valid():
            new_text = form.cleaned_data["text"]
            comment = Comment.objects.get(pk=comment_id)
            if comment.created_by.id != request.user.id:
                return HttpResponseBadRequest("Unauthorized")
            comment.text = new_text
            comment.save()
            return render(request, "website/components/comment/comment_text.html", {"com": comment})
        else:
            return HttpResponseBadRequest("Invalid Method")


def user(request, user_id):
    return HttpResponse("user")


class Submit(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, "website/pages/submit.html", {"form": SubmitForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = SubmitForm(request.POST)

        # TODO this probably should be checked in the frontend
        if not form.is_valid():
            return HttpResponseBadRequest("<p>Form was invalid</p>")

        link = form.cleaned_data["url"]
        domain = urlparse(link).netloc
        pub = Publication(
            title=form.cleaned_data["title"],
            link=link,
            domain=domain,
            text=form.cleaned_data["text"],
            created_by=request.user,
        )

        pub.save()
        return HttpResponseRedirect(reverse("publication", args=(pub.id,)))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")


class Login(View):
    def get(self, request):
        return render(request, "website/pages/login.html", {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        form.full_clean()
        if not form.is_valid():
            return HttpResponseBadRequest("<p>Login was invalid (server issue)</p>")

        user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if user is None:
            form.add_error("username", "invalid username or password")
            return render(
                request,
                "website/components/login_form.html",
                {"form": form},
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )
        else:
            login(request, user)
            response = HttpResponse()
            response["HX-Redirect"] = "/"
            return response


class Register(View):
    def get(self, request):
        return render(request, "website/pages/register.html", {"form": RegisterForm()})

    def post(self, request):
        form = RegisterForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest("<p>Login was invalid (server issue)</p>")

        username = form.cleaned_data["username"]
        password = form.cleaned_data["password"]

        if User.objects.filter(username=username).exists():
            form.add_error("username", "Username already exists")
            return render(
                request,
                "website/components/register_form.html",
                {"form": form},
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )

        usr = User.objects.create_user(username=username, password=password)
        if usr is None:
            form.add_error("username", "Unknown error. Please try again.")
            return render(request, "website/pages/register.html", {"form": form})

        usr.save()

        usr_login = authenticate(request, username=username, password=password)
        if usr_login is None:
            form.add_error("username", "Unknown error. Please try logging in manually.")
            return render(request, "website/pages/register.html", {"form": form})
        else:
            login(request, usr_login)
            response = HttpResponse()
            response["HX-Redirect"] = "/"
            return response
