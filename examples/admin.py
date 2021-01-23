from django.contrib import admin
from .models import User

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'type', 'is_staff', 'is_superuser')
    ordering = ('id',)
    search_fields = ('username',)

admin.site.register(User, UserAdmin)