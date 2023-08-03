from random import randint
from django.shortcuts import render
from .models import tarotCard
from . import forms
import random
import requests

# Create your views here.
def randomCard(request):
    queryset = tarotCard.objects.all()
    names = [card.name for card in queryset]
    int = random.randint(0,78)
    card = tarotCard.objects.get(name=names[int])
    return render(request, 'tarot/random_card.html', context={'card':card})

def pastPresentFuture(request):
    cards = requests.get("https://tarot-api-3hv5.onrender.com/api/v1/cards/random?n=3")
    cards = cards.json()
    context = {"past": cards["cards"][0],
                   "present": cards["cards"][1], 
                   "future": cards["cards"][2]}
    context['past_reversed'] = random.randint(0,1)
    context['present_reversed'] = random.randint(0,1)
    context['future_reversed'] = random.randint(0,1)
    context['past']['image'] = f"/media/tarot/cards/{context['past']['name'].replace(' ','_')}.jpg"
    context['present']['image'] = f"/media/tarot/cards/{context['present']['name'].replace(' ','_')}.jpg"
    context['future']['image'] = f"/media/tarot/cards/{context['future']['name'].replace(' ','_')}.jpg"

    return render(request, 'tarot/past_present_future.html', context=context)

def home(request):
    form = forms.readingForm()
    return render(request,'tarot/home.html', {'form':form})