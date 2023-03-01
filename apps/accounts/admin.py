from django.contrib import admin
from django.contrib.auth.models import Group
from .models import User
from .forms import UserChangeForm,UserCreationForm
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin    

@admin.register(User)
class UserModelAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = ('name','email','phone_number','is_admin')
    list_filter = ('is_admin',)

    fieldsets = (
        (None, {'fields': ('name','email','phone_number','password')}),
        ('Permissions', {'fields': ('last_login','is_admin',)}),
    )
    

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('name','email', 'phone_number', 'password1','password2'),
        }),
    )

    search_fields = ('name','phone_number','email')
    ordering = ('name',)


admin.site.unregister(Group)