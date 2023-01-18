from http import HTTPStatus

from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from website.forms import RegisterForm


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

        logged_user = authenticate(request, username=username, password=password)
        if logged_user:
            login(request, logged_user)
            response = HttpResponse()
            response["HX-Redirect"] = "/"
            return response
        else:
            form.add_error("username", "Unknown error. Please try logging in manually.")
            return render(request, "website/pages/register.html", {"form": form})
