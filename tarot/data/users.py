import datetime
from django.contrib.auth.hashers import make_password, check_password
from ..utils import handle_errors
from ..models import User, UserPassword

@handle_errors
def create_user(username, email, dob, password):
    now = datetime.datetime.now().date()
    age = (now - dob).days // 365
    if age < 18:
        raise ValueError("User must be at least 18 years old")
    if age > 120:
        raise ValueError("Please enter a valid date of birth")
    
    user = User(
        username=username, 
        email=email, 
        dob=dob,
        age=age)
    user.save()

    # Create a new UserPassword document
    password_hash = make_password(password)
    user_password = UserPassword(user_id=str(user.id), password_hash=password_hash)
    user_password.save()

    return {"message": "User created successfully", "user": user}

@handle_errors   
def validate_password(user_id, password):
    user_password = UserPassword.objects.get(user_id=user_id)
    return check_password(password, user_password.password_hash)

@handle_errors
def update_password(user_id, new_password):
    user_password = UserPassword.objects.get(user_id=user_id)
    user_password.password_hash = make_password(new_password)
    user_password.save()
    return {"message": "Password updated successfully"}

@handle_errors
def update_username(user_id, new_username):
    user = User.objects.get(id=user_id)
    user.username = new_username
    user.save()
    return {"message": "Username updated successfully", "user": user}

@handle_errors
def update_email(user_id, new_email):
    user = User.objects.get(id=user_id)
    user.email = new_email
    user.save()
    return {"message": "Email updated successfully", "user": user}

@handle_errors
def update_dob(user_id, new_dob):
    user = User.objects.get(id=user_id)
    user.dob = new_dob
    user.save()
    return {"message": "Date of birth updated successfully", "user": user}

@handle_errors
def delete_user(user_id):
    user = User.objects.get(id=user_id)
    user.delete()
    return {"message": "User deleted successfully"}

@handle_errors
def get_user_by_email(email):
    try:
        user = User.objects.get(email=email)
        return {"user": user}
    except User.DoesNotExist:
        return {"message": "User not found"}