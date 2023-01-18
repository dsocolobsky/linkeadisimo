from http import HTTPStatus

from django.contrib.auth import authenticate, login
from django.http import HttpResponseBadRequest, HttpResponse
from django.shortcuts import render
from django.views import View

from website.forms import LoginForm


class Login(View):
    def get(self, request):
        return render(request, "website/pages/login.html", {"form": LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        form.full_clean()
        if not form.is_valid():
            return HttpResponseBadRequest("<p>Login was invalid (server issue)</p>")

        logged_user = authenticate(
            request,
            username=form.cleaned_data["username"],
            password=form.cleaned_data["password"],
        )
        if logged_user:
            login(request, logged_user)
            response = HttpResponse()
            response["HX-Redirect"] = "/"
            return response
        else:
            form.add_error("username", "invalid username or password")
            return render(
                request,
                "website/components/login_form.html",
                {"form": form},
                status=HTTPStatus.UNPROCESSABLE_ENTITY,
            )
