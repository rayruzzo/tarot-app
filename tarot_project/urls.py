"""tarot_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.shortcuts import render
from django.conf import settings
from django.urls import path
from django.conf.urls.static import static
from django.urls import path
from tarot.views import (
    NewReadingView, ReadingView, 
    LoginView, SignUpView, LogoutView,
    HomeView, InterpretationAPIView,
    UserJournalView, CreateJournalEntryView, JournalEntryView,
    EditJournalEntryView, ReadingsView
)

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('joinus/', lambda request: render(request, 'joinus.html'), name='joinus'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('readings/', ReadingsView.as_view(), name='user_readings'),
    path('readings/new/', NewReadingView.as_view(), name='new_reading'),
    path('readings/<str:reading_id>/', ReadingView.as_view(), name='reading'),
    path('readings/<str:reading_id>/journal/new/', CreateJournalEntryView.as_view(), name='create_journal_entry'),
    path('readings/<str:reading_id>/journal/', JournalEntryView.as_view(), name='user_journal'),
    path('readings/<str:reading_id>/journal/<str:entry_id>/edit/', EditJournalEntryView.as_view(), name='edit_journal_entry'),
    path('api/interpret/', InterpretationAPIView.as_view(), name='interpretation_api'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
