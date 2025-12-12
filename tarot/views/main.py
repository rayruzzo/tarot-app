from rest_framework.decorators import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import render, redirect
from ..forms import loginForm, signUpForm
from ..data.users import create_user, check_password, get_user_by_email

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
                from ..data.users import validate_password
                if validate_password(str(user.id), password):
                    request.session['user_id'] = str(user.id)
                    request.session['user_email'] = user.email
                    request.session['user_name'] = user.username if hasattr(user, 'username') else user.name
                    return redirect('home')
            return Response({'error': 'Invalid email or password'}, status=status.HTTP_401_UNAUTHORIZED)
        else:
            return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST)
        
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
            user = result['user']
            if user:
                request.session['user_id'] = str(user.id)
                request.session['user_email'] = user.email
                request.session['user_name'] = user.username
                return redirect('home')
            else:
                return Response({'error': 'Failed to create user'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            return Response({'error': 'Invalid form data'}, status=status.HTTP_400_BAD_REQUEST) 
        
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
            return render(request, 'home.html', {'user_id': user_id, 'user_email': user_email, 'user_name': user_name})
        else:
            return render(request, 'joinus.html')