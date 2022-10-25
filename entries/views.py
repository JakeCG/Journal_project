from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Journal
from django.utils import timezone


# Create your views here.

def home(request):
    entries = Journal.objects
    return render(request, 'entries/home.html', {'entries': entries})


@login_required(login_url="/accounts/signup")  # forces the user to be logged in.
def create(request):
    if request.method == 'POST':
        if request.POST['title'] and request.POST['body'] and request.POST['url'] and request.FILES['icon']:
            # big check to make sure all entries are actually filled in.
            entry = Journal()
            entry.title = request.POST['title']
            entry.body = request.POST['body']
            if request.POST['url'].startswith('http://') or request.POST['url'].startswith('https://'):
                # Check to make sure that the url begins with the correct formatting.
                entry.url = request.POST['url']
            else:
                # Auto formats the url if it isn't correct.
                entry.url = 'http://' + request.POST['url']
            entry.icon = request.FILES['icon']
            entry.pub_date = timezone.now()
            entry.author = request.user
            entry.save()
            return redirect('/entries/' + str(entry.id))  # TODO redirect to home

    else:
        return render(request, 'entries/create.html', {'error': 'All fields are required!'})


def detail(request, entry_id):
    entry = get_object_or_404(Journal, pk=entry_id)
    return render(request, 'entries/detail.html', {'entry': entry})

@login_required(login_url="/accounts/signup")
def upvote(request, entry_id):
    if request.method == 'POST':
        entry = get_object_or_404(Journal, pk=entry_id)
        entry.votes_total += 1
        entry.save()
        return redirect('/entries/' + str(entry.id))
