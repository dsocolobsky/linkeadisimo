from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from django.shortcuts import get_object_or_404, render

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
