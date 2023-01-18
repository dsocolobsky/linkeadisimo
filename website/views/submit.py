from urllib.parse import urlparse

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View

from website.forms import SubmitForm
from website.models import Publication


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
