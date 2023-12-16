from django.contrib import admin
from django.contrib.sessions.models import Session
from .models import AddmoneyInfo, UserProfile

# Register your models here.
@admin.register(AddmoneyInfo)
class AddmoneyInfoAdmin(admin.ModelAdmin):
    list_display = ("user", "quantity", "Date", "Category", "add_money")

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ("user", "profession", "Savings", "income")

admin.site.register(Session)  # Registering Session model