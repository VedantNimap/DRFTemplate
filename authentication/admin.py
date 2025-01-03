from django import forms
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.contrib.auth.models import Group
from authentication import models




admin.site.unregister(Group)


class UserCreationForm(forms.ModelForm):
    password1 = forms.CharField(
        label="Password",
        widget=forms.PasswordInput,
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput,
    )

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "is_staff",
            "is_superuser",
            "is_active",
        )

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("Passwords don't match")
        return password2

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user

    def save_model(self, request, obj, form, change):
        user = form.save(commit=False)
        if not user.pk:  # If the user is being created
            user.set_password(form.cleaned_data["password1"])

        user.save()
        groups = form.cleaned_data.get("groups")
        if groups:
            user.groups.set(groups)

        return user


class UserChangeForm(forms.ModelForm):
    password = ReadOnlyPasswordHashField()

    class Meta:
        model = models.User
        fields = (
            "first_name",
            "last_name",
            "email",
            "profile_picture",
            "is_staff",
            "is_superuser",
            "is_active",
        )


class UserAdmin(BaseUserAdmin):
    form = UserChangeForm
    add_form = UserCreationForm

    list_display = (
        "id",
        "first_name",
        "last_name",
        "email",
        "is_staff",
        "is_superuser",
        "is_active",
    )
    fieldsets = (
        (None, {"fields": ("email", "password")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        # ("Permissions", {"fields": ("groups",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            },
        ),
    )
    add_fieldsets = (
        (None, {"fields": ("email", "password1", "password2")}),
        (
            "Personal info",
            {
                "fields": (
                    "first_name",
                    "last_name",
                )
            },
        ),
        # ("Permissions", {"fields": ("groups",)}),
        (
            "Permissions",
            {
                "fields": (
                    "is_staff",
                    "is_superuser",
                    "is_active",
                )
            },
        ),
    )
    search_fields = (
        "email",
        "first_name",
        "last_name",
    )
    ordering = ("created_at",)
    filter_horizontal = ()


admin.site.register(models.User, UserAdmin)


class SessionAdmin(admin.ModelAdmin):
    list_display = ("user", "start_time", "end_time")
    readonly_fields = ("start_time",)


admin.site.register(models.Session, SessionAdmin)

