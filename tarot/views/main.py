from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from ..forms import loginForm, signUpForm
from ..data.users import create_user, get_user_by_email, validate_password
from ..data.tarot import getReadingsByUser

class LoginView(APIView):
    def get(self, request):
        form = loginForm()
        return render(request, 'login.html', {'form': form})
    def post(self, request):
        form = loginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            user_result = get_user_by_email(email)
            user = user_result.get('user') if user_result and 'user' in user_result else None
            if user:
                if validate_password(str(user.id), password):
                    request.session['user_id'] = str(user.id)
                    request.session['user_email'] = user.email
                    request.session['user_name'] = user.username if hasattr(user, 'username') else user.name
                    return redirect('home')
            return render(request, 'login.html', {'form': form, 'error': 'Invalid email or password'})
        else:
            return render(request, 'login.html', {'form': form, 'error': 'Invalid form data'})
        
class SignUpView(APIView):
    def get(self, request):
        form = signUpForm()
        return render(request, 'signup.html', {'form': form})
    def post(self, request):
        form = signUpForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']
            username = form.cleaned_data['username']
            dob = form.cleaned_data['dob']
            result = create_user(username, email, dob, password)
            print(result)
            
            # Check if result is an error string or a success dict
            if isinstance(result, str):
                # Error occurred
                return render(request, 'signup.html', {'form': form, 'error': result})
            elif result and 'user' in result:
                user = result['user']
                request.session['user_id'] = str(user.id)
                request.session['user_email'] = user.email
                request.session['user_name'] = user.username
                return redirect('home')
            else:
                return render(request, 'signup.html', {'form': form, 'error': 'Failed to create user'})
        else:
            return render(request, 'signup.html', {'form': form, 'error': 'Invalid form data'}) 
        
class LogoutView(APIView):
    def get(self, request):
        request.session.flush()
        return redirect('login')
    
class HomeView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        user_email = request.session.get('user_email')
        user_name = request.session.get('user_name')
        if user_id:
            readings = getReadingsByUser(user_id, 3)
            readings = [reading.to_dict() for reading in readings]
            return render(request, 'home.html', {'user_id': user_id, 'user_email': user_email, 'user_name': user_name, 'readings': readings})
        else:
            return render(request, 'joinus.html')
        
class ReadingsView(APIView):
    def get(self, request):
        user_id = request.session.get('user_id')
        if user_id:
            readings = getReadingsByUser(user_id)
            readings = [reading.to_dict() for reading in readings]
            return render(request, 'readings.html', {'readings': readings})
        else:
            return redirect('login')