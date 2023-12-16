from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login as dj_login, logout
from django.contrib import messages
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from .models import AddmoneyInfo, UserProfile
import datetime


# Other views as they were...

def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('login')  # Replace 'login' with the name of your login URL pattern
    else:
        form = UserCreationForm()
    return render(request, 'home/register.html', {'form': form})


def home(request):
    if request.user.is_authenticated:
        return redirect('index')
    return render(request, 'home/login.html')


def index(request):
    if request.user.is_authenticated:
        user = request.user
        add_money_info = AddmoneyInfo.objects.filter(user=user).order_by('-Date')
        paginator = Paginator(add_money_info, 4)
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
            add = AddmoneyInfo(user=user, add_money=add_money, quantity=quantity, Date=Date, Category=Category)
            add.save()
            return redirect('index')
    return redirect('index')


def expense_edit(request, id):
    if request.user.is_authenticated:
        try:
            AddmoneyInfo = AddmoneyInfo.objects.get(id=id)
            user_id = request.user.id
            user = User.objects.get(id=user_id)
            return render(request, 'home/expense_edit.html', {'AddmoneyInfo': AddmoneyInfo})
        except AddmoneyInfo.DoesNotExist:
            pass  # Handle if expense with given ID doesn't exist
    return redirect('home')  # Redirect to home if not logged in or expense not found


def expense_delete(request, id):
    if request.user.is_authenticated:
        try:
            AddmoneyInfo = AddmoneyInfo.objects.get(id=id)
            AddmoneyInfo.delete()
        except AddmoneyInfo.DoesNotExist:
            pass  # Handle if expense with given ID doesn't exist
    return redirect('index')  # Redirect to index after deleting expense or if not logged in


def expense_month(request):
    if request.user.is_authenticated:
        todays_date = datetime.date.today()
        one_month_ago = todays_date - datetime.timedelta(days=30)
        user = User.objects.get(id=request.user.id)
        addmoney = AddmoneyInfo.objects.filter(user=user, Date__range=(one_month_ago, todays_date))

        finalrep = {}
        categories = set([item.Category for item in addmoney])

        def get_expense_category_amount(Category):
            return sum(item.quantity for item in addmoney if item.Category == Category)

        for category in categories:
            finalrep[category] = get_expense_category_amount(category)

        return JsonResponse({'expense_category_data': finalrep}, safe=False)
    return redirect('home')


# Define similar views for other functionalities (expense_week, stats, weekly, check, info_year, info)
# Ensure proper indentation and handling of user authentication, fetching data, and rendering responses.


def charts(request):
    # Your logic for the charts view here
    return HttpResponse("Charts view")


def tables(request):
    # Your logic for the tables view here
    return HttpResponse("Tables view")

def weekly(request):
    # Your view logic here
    return HttpResponse("Weekly view")

def check(request):
    # Your view logic here
    return HttpResponse("Check view")