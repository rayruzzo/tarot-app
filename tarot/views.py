
from django.shortcuts import render
from . import forms
from django.conf import settings
from .utils import get_tarot_cards, generate_interpretation
from django.shortcuts import redirect

def reading_router(request):
    """
    Route the form submission to the correct reading view
    based on the dropdown selection, without losing POST data.
    """
    if request.method == "POST":
        form = forms.readingForm(request.POST)
        if form.is_valid():
            reading_type = form.cleaned_data["reading_type"]
            
            if reading_type == "past_present_future":
                # Call the view directly, passing the request
                return past_present_future(request)
            elif reading_type == "safe_passage":
                return lilias_safe_passage(request)
    # fallback to home if GET or invalid form
    form = forms.readingForm()
    return render(request, "tarot/home.html", {"form": form})


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

def lilias_safe_passage(request):
    """
    Handles Lilia's Safe Passage 7-card tarot reading.
    Assigns each card a position and random reversed status is already handled in get_tarot_cards.
    Generates a textual interpretation for the full spread.
    """
    if request.method == "POST":
        form = forms.readingForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data["name"]
            question = form.cleaned_data["question"]

            # Get 7 cards for the Safe Passage spread
            cards = get_tarot_cards(7)


            # Assign the positions
            positions = [
                "Traveler",
                "What's Missing",
                "Path Behind",
                "Path Ahead",
                "Obstacles",
                "Windfall",
                "Destination"
            ]
            for i, card in enumerate(cards):
                card["position"] = positions[i]

            # Generate interpretation
            interpretation = generate_interpretation(cards, name, question)
            print(cards)

            context = {
                "name": name,
                "form": form,
                "cards": cards,
                "interpretation": interpretation,
            }

            return render(request, "tarot/lilias_safe_passage.html", context)

    else:
        form = forms.readingForm()

    return render(request, "tarot/home.html", {"form": form})

def home(request):
    form = forms.readingForm()
    return render(request,'tarot/home.html', {'form':form})