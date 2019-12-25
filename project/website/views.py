from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, HttpResponseBadRequest
from django.template import loader
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import User, Publication

# Create your views here.
def index(request):
    publications = Publication.objects.order_by('-date')
    context = {
        'publications': publications
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

def submit(request):
    if request.method == 'POST':
        print("it's a post")
        return submitPOST(request)
    else:
        return render(request, 'website/submit.html')

def submitPOST(request):
    text = request.POST['text']
    url  = request.POST['url']
    user = User.objects.get(pk=1)

    if text != '' and url != '':
        return HttpResponseBadRequest('<p>You must only submit EITHER url OR text</p>')

    if text == '':
        print("It's text")
        # We have to submit an URL
        pub = Publication(is_text = False, link = url, created_by = user)
    else:
        print("It's url")
        # We have to submit the text
        pub = Publication(is_text = True, text = text, created_by = user)

    pub.save()
    return HttpResponseRedirect(reverse('publication', args=(pub.id,)))