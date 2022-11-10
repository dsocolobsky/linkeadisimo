from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views import View
from django.views.decorators.csrf import csrf_protect, csrf_exempt
import json as json

from .forms import SubmitForm, LoginForm, CommentForm, RegisterForm
from .models import Publication, Comment


# Create your views here.
def index(request):
    publications = Publication.objects.order_by('-created_at')
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
        'publication': pub,
        'form': CommentForm()
    }
    return render(request, 'website/publication.html', context)


# POST method for posting a comment to a certain publication
@login_required
def comment(request):
    form = CommentForm(request.POST)

    if not form.is_valid():
        return HttpResponseBadRequest('<p>Form was invalid</p>')

    pubid = request.POST['pubid']
    text = form.cleaned_data['text']
    parentid = request.POST['parent']
    parent = Comment.objects.get(pk=parentid) if parentid != '' else None
    level = parent.level + 1 if parent is not None else 0
    pub = get_object_or_404(Publication, pk=pubid)

    print(f'Saving comment with parent {parentid}')
    the_comment = Comment(text=text, publication=pub, created_by=request.user, parent_comment=parent, level=level)
    the_comment.save()

    return HttpResponseRedirect(reverse('publication', args=(pubid,)))


def user(request, user_id):
    return HttpResponse('user')


class Submit(View):
    @method_decorator(login_required)
    def get(self, request):
        return render(request, 'website/submit.html', {'form': SubmitForm()})

    @method_decorator(login_required)
    def post(self, request):
        form = SubmitForm(request.POST)

        # TODO this probably should be checked in the frontend
        if not form.is_valid():
            return HttpResponseBadRequest('<p>Form was invalid</p>')

        pub = Publication(title=form.cleaned_data['title'], link=form.cleaned_data['url'],
                          text=form.cleaned_data['text'], created_by=request.user)

        pub.save()
        return HttpResponseRedirect(reverse('publication', args=(pub.id,)))


def logout_view(request):
    logout(request)
    return HttpResponseRedirect('/')


class Login(View):
    def get(self, request):
        return render(request, 'website/login.html', {'form': LoginForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        form.full_clean()
        if not form.is_valid():
            return HttpResponseBadRequest('<p>Login was invalid (server issue)</p>')

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        user = authenticate(request, username=username, password=password)

        if user is None:
            return HttpResponseBadRequest('<p>Login invalid</p>')
        else:
            login(request, user)
            return HttpResponseRedirect('/')


@login_required
@csrf_protect
def upvote(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')

    postdata = json.loads(request.body.decode('utf-8'))

    pub = Publication.objects.get(pk=postdata['id'])
    if pub is None:
        return HttpResponseBadRequest('<p>Upvote invalid</p>')

    pub.votes += 1
    pub.voters.add(request.user)
    pub.save()

    return HttpResponseRedirect('/')


@login_required
@csrf_protect
def upvote_comment(request):
    if request.method != "POST":
        return HttpResponseRedirect('/')

    postdata = json.loads(request.body.decode('utf-8'))

    com = Comment.objects.get(pk=postdata['id'])
    if com is None:
        return HttpResponseBadRequest('<p>Upvote invalid</p>')

    pub = com.publication
    if pub is None:
        return HttpResponseBadRequest('<p>Upvote invalid</p>')

    com.votes += 1
    com.voters.add(request.user)
    com.save()

    Comment.objects.rebuild()

    return HttpResponseRedirect(reverse('publication', args=(pub.id,)))


class Register(View):
    def get(self, request):
        return render(request, 'website/register.html', {'form': RegisterForm()})

    def post(self, request):
        form = LoginForm(request.POST)
        if not form.is_valid():
            return HttpResponseBadRequest('<p>Login was invalid (server issue)</p>')

        username = form.cleaned_data['username']
        password = form.cleaned_data['password']

        if User.objects.filter(username=username).exists():
            return HttpResponseBadRequest('<p>Username already exists!</p>')

        usr = User.objects.create_user(username=username, password=password)
        if usr is None:
            return HttpResponseBadRequest('<p>Error creating user somehow</p>')

        usr.save()

        usr_login = authenticate(request, username=username, password=password)
        if usr_login is None:
            return HttpResponseBadRequest('<p>Login invalid</p>')
        else:
            login(request, usr_login)
            return HttpResponseRedirect('/')
