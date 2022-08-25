from random import randint
from django.shortcuts import render
from .models import tarotCard
from . import forms
import random

# Create your views here.
def randomCard(request):
    queryset = tarotCard.objects.all()
    names = [card.name for card in queryset]
    int = random.randint(0,78)
    card = tarotCard.objects.get(name=names[int])
    return render(request, 'tarot/random_card.html', context={'card':card})

def pastPresentFuture(request):
    queryset = tarotCard.objects.all()
    names = [card.name for card in queryset]
    context = {}
    context['name'] = request.POST.get('name')
    context['question'] = request.POST.get('question')
    cards_drawn = random.sample(range(0,len(names)),3)
    positions = ['past','present','future']
    for card,position in zip(cards_drawn,positions):
        context[position] = tarotCard.objects.get(name=names[card])
        context[position+"_reversed"] = round(random.random())
        
    return render(request, 'tarot/past_present_future.html', context=context)

def home(request):
    form = forms.readingForm()
    return render(request,'tarot/home.html', {'form':form})