from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from . import models
from .forms import clubRegisterationForm, SignUpForm, adventureEventform


# Create your views here.

def index(request):
    cities = models.AdventureClub.objects.values('city')
    clubs = ''
    featuredClubs = models.AdventureClub.objects.filter(featured=True)
    featuredEvents = models.AdventureEvent.objects.filter(featured=True)
    if request.method == 'POST':
        query = request.POST.get('city')
        clubs = models.AdventureClub.objects.filter(city=query)
    context = {'user': request.user, 'city': cities, 'club': clubs, 'FC': featuredClubs, 'FE': featuredEvents}
    return render(request, 'AdventureClubs/index.html', context)


def signup(request):

    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('club:signIn')
    else:
        form = SignUpForm()
    context = {'form': form}
    return render(request, 'AdventureClubs/signUp.html', context)


def signIn(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request=request, data=request.POST)
            if form.is_valid():
                username = form.cleaned_data['username']
                password = form.cleaned_data['password']
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user, backend=None)
                    messages.info(request, f"You are now logged in as {username}")
                    return HttpResponseRedirect('/club/')
            else:
                form = AuthenticationForm()
                msg = "Incorrect username or password!!!"
                return render(request, 'AdventureClubs/SignIn.html', context={'msg': msg, 'form': form})
                # return redirect('club:signIn')
        else:
            form = AuthenticationForm()
            return render(request, 'AdventureClubs/SignIn.html', context={'form': form})
    else:
        return HttpResponseRedirect('/club/index/')


def signOut(request):
    logout(request)
    return redirect('club:signIn')


def RegisterClub(request):

    if request.method == 'POST':
        form = clubRegisterationForm(request.POST, request.FILES)
        if form.is_valid():
            form = form.save(commit=False)
            form.owner = request.user
            form.save()
            messages.success(request, 'Adventure Club Registered successfully!!!')
    form = clubRegisterationForm()
    return render(request, 'AdventureClubs/registerClub.html', context={'form': form, })


def createEvent(request):
    clubs = models.AdventureClub.objects.filter(owner=request.user)
    if request.method == 'POST':
        form = adventureEventform(request.POST, request.FILES)
        print(form.errors)
        if form.is_valid():
            club = request.POST.get('club')
            # club_rec = models.AdventureClub.objects.filter(club_name=club).values(models.AdventureClub.pk)
            # club_rec = models.AdventureClub.objects.get(club_name=club)
            # print("Club Id", club_rec.pk)
            # form = form.save(commit=False)
            # form.event_by = club_rec.pk
            # form.save()
            # ev_by = club
            # club_ref = models.AdventureClub.objects.get(id=models.AdventureClub.objects.filter(club_name=club))
            # print(club_ref)
            # models.AdventureEvent.event_by = club_rec.pk
            title = form.cleaned_data['title']
            overview = form.cleaned_data['overview']
            image = form.cleaned_data['image']
            event_start_date = form.cleaned_data['event_start_date']
            event_end_date = form.cleaned_data['event_end_date']
            eventmodelobj = models.AdventureEvent(event_by=models.AdventureClub.objects.get(club_name=club), title=title
                                                  , overview=overview, image=image
                                                  , event_start_date=event_start_date, event_end_date=event_end_date)
            eventmodelobj.save()
            messages.success(request, 'Event Created successfully!!!')
    form = adventureEventform()
    return render(request, 'AdventureClubs/adventureevent_form.html', context={'form': form, 'clubs': clubs, })


def home(request):
    return render(request, 'AdventureClubs/home.html')


def myClubs(request):
    userClub = models.AdventureClub.objects.filter(owner=request.user)
    return render(request, "AdventureClubs/myClubs.html", context={'clubs': userClub})


def onGoingEvents(request):
    events = models.AdventureEvent.objects.all()
    return render(request, "AdventureClubs/events.html", context={'event': events})
