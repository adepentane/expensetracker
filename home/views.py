from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib.auth.models import User
from .models import Addmoney_info, UserProfile
from django.core.paginator import Paginator


def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'home/login.html')


def index(request):
    if request.user.is_authenticated:
        user = request.user
        addmoney_info = Addmoney_info.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(addmoney_info, 4)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)
        context = {'page_obj': page_obj}
        return render(request, 'home/index.html', context)
    return redirect('home')


def addmoney(request):
    return render(request, 'home/addmoney.html')


def profile(request):
    if request.user.is_authenticated:
        return render(request, 'home/profile.html')
    return redirect('home')


def profile_edit(request, id):
    if request.user.is_authenticated and request.user.id == id:
        user = User.objects.get(id=id)
        return render(request, 'home/profile_edit.html', {'user': user})
    return redirect('home')


def profile_update(request, id):
    if request.user.is_authenticated and request.user.id == id:
        if request.method == "POST":
            user = User.objects.get(id=id)
            user.first_name = request.POST.get("fname")
            user.last_name = request.POST.get("lname")
            user.email = request.POST.get("email")
            profile = user.userprofile
            profile.Savings = request.POST.get("Savings")
            profile.income = request.POST.get("income")
            profile.profession = request.POST.get("profession")
            profile.save()
            user.save()
            return redirect('profile')
    return redirect('home')


def handleSignup(request):
    if request.method == 'POST':
        # handle signup logic
        return redirect('login')


def handlelogin(request):
    if request.method == 'POST':
        # handle login logic
        return redirect('index')


def handleLogout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Successfully logged out")
    return redirect('home')


def addmoney_submission(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            user = request.user
            add_money = request.POST.get("add_money")
            quantity = request.POST.get("quantity")
            Date = request.POST.get("Date")
            Category = request.POST.get("Category")
            add = Addmoney_info(user=user, add_money=add_money, quantity=quantity, Date=Date, Category=Category)
            add.save()
            return redirect('index')
    return redirect('index')
