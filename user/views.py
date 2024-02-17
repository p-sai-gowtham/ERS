from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from .models import User
from django.contrib import messages
from django.contrib.auth.hashers import make_password, check_password
from django.shortcuts import render
from django.shortcuts import render
from datetime import datetime, timedelta

from .models import Counter

def days_counter(request):
    # Retrieve the Counter object
    counter = Counter.objects.first()
    
    # Calculate the time difference since the start date
    if counter:
        start_datetime = counter.start_datetime
        now = datetime.now()
        time_passed = now - start_datetime
        days_passed = time_passed.days
        hours_passed, remainder = divmod(time_passed.seconds, 3600)
        minutes_passed, seconds_passed = divmod(remainder, 60)
    else:
        days_passed = None
        hours_passed = None
        minutes_passed = None
        seconds_passed = None

    return render(request, 'counter/days_counter.html', {
        'days_passed': days_passed,
        'hours_passed': hours_passed,
        'minutes_passed': minutes_passed,
        'seconds_passed': seconds_passed
    })


    

def signin(request):
    if request.method == "POST":
        email = request.POST["email"]
        password = request.POST["password"]
        # Check if the user exists
        if not User.objects.filter(email=email).exists():
            messages.error(request, "User doesn't exist.")
            return render(
                request,
                "user/login.html",
                {"message": "User doesn't exist. Please sign up"},
            )

        user = User.objects.get(email=email)

        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user is not None:
            # Check the password using check_password
            if check_password(password, authenticated_user.password):
                request.session["email"] = email
                request.session.save()
                login(request, authenticated_user)
                messages.success(request, "Login Successful")
                return redirect("/")

        messages.error(request, "Incorrect email or password")
        return render(
            request, "user/login.html", {"message": "Incorrect email or password"}
        )

    return render(request, "user/login.html")


def logout_view(request):
    if request.session.get("email", ""):
        del request.session["email"]
    request.session.save()
    logout(request)
    messages.success(request, "Logout Successful")
    return redirect("/")


def add_user(request):
    if request.method == "POST":
        email = request.POST.get("email")
        username = request.POST.get("username")
        if User.objects.filter(email=email).exists():
            messages.error(request, "User with this email already exists!")
            return redirect("/user/add_user")
        password = request.POST.get("password")
        conformpassword = request.POST.get("conformpassword")
        if password != conformpassword:
            messages.error(request, "Password and conform password do not match")
            return redirect("/user/add_user")

        hashed_password = make_password(password)
        user = User.objects.create(
            username=username,
            email=email,
            password=hashed_password,
        )
        authenticated_user = authenticate(email=email, password=password)
        if authenticated_user is not None:
            # Check the password using check_password
            if check_password(password, authenticated_user.password):
                request.session["email"] = email
                request.session.save()
                login(request, authenticated_user)
                messages.success(request, "User added successfully!")
                return redirect("/")
        messages.error(request, "Incorrect email or password")
        return render(
            request, "user/login.html", {"message": "Incorrect email or password"}
        )
    return render(request, "user/login.html", {"page": "signup"})
