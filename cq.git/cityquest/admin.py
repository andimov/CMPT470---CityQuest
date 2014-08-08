from django.contrib import admin
from cityquest.models import Event, Attendee, Comment
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model
from django.contrib.auth import forms

# Register your models here.

class newUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = get_user_model()

class newUserCreateForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()

class newUserAdmin(UserAdmin):
    form = newUserCreateForm

    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('about_me', 'ph_number', 'age', 'sex', 'location')}),
    )


admin.site.register(Event)
admin.site.register(get_user_model(), newUserAdmin)
admin.site.register(Attendee)
admin.site.register(Comment)
