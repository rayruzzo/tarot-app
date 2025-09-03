
from django.shortcuts import render
from . import forms
from django.conf import settings
from .utils import get_tarot_cards, generate_interpretation

def past_present_future(request):
    if request.method == "POST":
        form = forms.readingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            print(name)
            question = form.cleaned_data["question"]
            cards = get_tarot_cards(3)
            positions = ["Past", "Present", "Future"]
            for i, card in enumerate(cards):
                card["position"] = positions[i]
            print(cards)
            interpretation = generate_interpretation(cards, name, question)
            context = {
                "name": name,
                "form": form,
                "cards": cards,
                "interpretation": interpretation,
            }
            return render(request, "tarot/past_present_future.html", context)
    else:
        form = forms.readingForm()
    return render(request, "tarot/home.html", {"form": form})

def home(request):
    form = forms.readingForm()
    return render(request,'tarot/home.html', {'form':form})