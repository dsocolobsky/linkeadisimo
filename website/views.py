from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest, HttpResponseNotFound
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views import View
from django.contrib.auth import logout
from django.contrib.auth.models import Permission, User
from .models import Publication

# Create your views here.
def index(request):
    publications = Publication.objects.order_by('-date')
    if request.user.is_authenticated:
        context = {
            'publications': publications,
            'authenticated': True,
            'user': request.user
        }
    else:
        context = {
            'publications': publications,
            'authenticated': False,
        }
    return render(request, 'website/index.html', context)

def publication(request, pub_id):
    pub = get_object_or_404(Publication, pk=pub_id)
    context = {
        'publication': pub
    }
    return render(request, 'website/publication.html', context)

def user(request, user_id):
    return HttpResponse('user')

class Submit(View):
    def get(self, request):
        return render(request, 'website/submit.html')

    def post(self, request):
        title = request.POST['title']
        text = request.POST['text']
        url  = request.POST['url']
        user = User.objects.get(pk=1)

        if text != '' and url != '':
            return HttpResponseBadRequest('<p>You must only submit EITHER url OR text</p>')

        if text == '':
            pub = Publication(is_text=False, title=title, link=url, created_by=user)
        else:
            pub = Publication(is_text=True, title=title, text=text, created_by=user)

        pub.save()
        return HttpResponseRedirect(reverse('publication', args=(pub.id,)))

def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')

class Login(View):
    def get(self, request):
        return render(request, 'website/login.html')

    def post(self, request):
        return HttpResponseBadRequest('<p>Not yet implemented</p>')