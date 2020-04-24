from django.shortcuts import render, redirect
from .models import User, UserManager, Trip, TripManager
import bcrypt
from django.contrib import messages
from time import strftime, gmtime


def index(request):
    request.session['log_email'] = []
    request.session['log_password'] = []
    request.session['log_first_name'] = []
    request.session['log_last_name'] = []
    return render(request, "index.html")


def registration(request):
    errors = User.objects.user_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            first_name = request.POST['first_name']
            last_name = request.POST['last_name']
            email = request.POST['email']
            pw = request.POST['password']
            confirm_pw = request.POST['confirm_pw']
            pw_hash = bcrypt.hashpw(pw.encode(), bcrypt.gensalt()).decode()
            # confirm password stuff here
            if bcrypt.checkpw(confirm_pw.encode(), pw_hash.encode()) == True:
                User.objects.create(first_name=first_name, last_name=last_name,
                                    email=email, password=pw_hash)
                request.session['log_email'] = email
                request.session['log_password'] = pw_hash
                request.session['log_first_name'] = first_name
                request.session['log_last_name'] = last_name
            else:
                errors['pwconfirm'] = "Passwords did not match!"
                if len(errors) > 0:
                    for key, value in errors.items():
                        messages.error(request, value)
                    return redirect('/')
    return redirect("/dashboard")


def log_in(request):
    errors = User.objects.log_in_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/')
    else:
        if request.method == "POST":
            log_email = request.POST['log_email']
            log_pw = request.POST['log_pw']
            if User.objects.filter(email=log_email):
                request.session['log_email'] = log_email
                request.session['log_pw'] = log_pw
                return redirect("/dashboard")


def success_log_in(request):
    if request.session['log_email'] == []:
        return redirect('/')
    else:
        logged_user = User.objects.filter(email=request.session['log_email'])
        logged_user_first_name = logged_user[0].first_name
        logged_user_last_name = logged_user[0].last_name
        user_id = logged_user[0].id
        current_user = User.objects.get(id=user_id)
        logged_user_trips = current_user.trips.all()
        request.session['id'] = user_id
        all_trips = Trip.objects.all()
        all_trips_without_user = Trip.objects.exclude(users=user_id)
        creator = 0
        newlist = []
        for trip in logged_user_trips:
            people = trip.users.all()
            newlist += people
            creator = people[0]
        lol = newlist[0]
        user_creator = logged_user_trips[0]
        context = {
            "first_name": logged_user_first_name,
            "time": strftime("%m-%d-%y"),
            "user_id": user_id,
            "session_id": request.session['id'],
            "user_all_trips": logged_user_trips,
            "user_creator": logged_user_trips[0],
            "all_trips": all_trips,
            "all_trips_without_user": all_trips_without_user,
            "logged_user": logged_user[0],
            "creator": creator.email,
            "session_email": request.session['log_email'],
            "newlist": lol,
        }
        return render(request, "dashboard.html", context)


def new_trip_page(request):
    logged_user = User.objects.filter(email=request.session['log_email'])
    logged_user_first_name = logged_user[0].first_name
    logged_user_last_name = logged_user[0].last_name
    user_id = logged_user[0].id
    context = {
        "first_name": logged_user_first_name,
        "time": strftime("%m-%d-%y"),
    }
    return render(request, "newtrip.html", context)


def create_trip(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/trips/new')
    else:
        if request.method == "POST":
            logged_user = User.objects.filter(
                email=request.session['log_email'])
            logged_user_first_name = logged_user[0].first_name
            logged_user_last_name = logged_user[0].last_name
            user_id = logged_user[0].id
            destination = request.POST['destination']
            start_date = request.POST['start_date']
            end_date = request.POST['end_date']
            plan = request.POST['plan']
            new_trip = Trip.objects.create(
                destination=destination, start_date=start_date, end_date=end_date, plan=plan)
            new_trip.users.add(user_id)
        return redirect('/dashboard')


def remove_trip(request, trip_id):
    trip = Trip.objects.get(id=trip_id)
    trip.delete()
    return redirect('/dashboard')


def edit_trip_page(request, trip_id):
    logged_user = User.objects.filter(
        email=request.session['log_email'])
    logged_user_first_name = logged_user[0].first_name
    logged_user_last_name = logged_user[0].last_name
    user_id = logged_user[0].id
    trip = Trip.objects.get(id=trip_id)
    context = {
        "first_name": logged_user_first_name,
        "time": strftime("%m-%d-%y"),
        "trip": trip,
    }
    return render(request, "edittrip.html", context)


def edit_trip(request, trip_id):
    errors = Trip.objects.edit_trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/trips/edit/{trip_id}")
    else:
        new_destination = request.POST['edit_destination']
        new_start_date = request.POST['edit_start_date']
        new_end_date = request.POST['edit_end_date']
        new_plan = request.POST['edit_plan']
        trip = Trip.objects.get(id=trip_id)
        trip.destination = new_destination
        trip.start_date = new_start_date
        trip.end_date = new_end_date
        trip.plan = new_plan
        trip.save()
    return redirect('/dashboard')


def trip_page(request, trip_id):
    logged_user = User.objects.filter(
        email=request.session['log_email'])
    logged_user_first_name = logged_user[0].first_name
    logged_user_last_name = logged_user[0].last_name
    user_id = logged_user[0].id
    trip = Trip.objects.get(id=trip_id)
    creators = trip.users.all()
    creator_name = creators[0].first_name
    creator_id = creators[0].id
    not_creator = Trip.objects.exclude(id=creator_id)
    context = {
        "first_name": logged_user_first_name,
        "time": strftime("%m-%d-%y"),
        "trip": trip,
        "creator_name": creator_name,
        "not_creator": not_creator,
        "creator_id": creator_id,
        "creators": creators,
    }
    return render(request, "trippage.html", context)


def join(request, trip_id):
    logged_user = User.objects.filter(
        email=request.session['log_email'])
    logged_user_first_name = logged_user[0].first_name
    logged_user_last_name = logged_user[0].last_name
    user_id = logged_user[0].id
    trip = Trip.objects.get(id=trip_id)
    trip.users.add(user_id)
    return redirect('/dashboard')


def cancel(request, trip_id):
    logged_user = User.objects.filter(
        email=request.session['log_email'])
    logged_user_first_name = logged_user[0].first_name
    logged_user_last_name = logged_user[0].last_name
    user_id = logged_user[0].id
    trip = Trip.objects.get(id=trip_id)
    trip.users.remove(user_id)
    return redirect('/dashboard')


def log_out(request):
    request.session['log_email'] = []
    request.session['log_pw'] = []
    return redirect('/')
