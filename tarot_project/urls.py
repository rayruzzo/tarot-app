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
from tarot.views import NewReadingView, ReadingView, LoginView, SignUpView, HomeView, LogoutView
import uuid

def dev_session_user(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if 'dev_session_id' not in request.session:
            request.session['dev_session_id'] = str(uuid.uuid4())
        return view_func(request, *args, **kwargs)
    return _wrapped_view

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('joinus/', lambda request: render(request, 'joinus.html'), name='joinus'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('signup/', SignUpView.as_view(), name='signup'),
    path('readings/new/', dev_session_user(NewReadingView.as_view()), name='new_reading'),
    path('readings/<int:reading_id>/', dev_session_user(ReadingView.as_view()), name='reading'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
