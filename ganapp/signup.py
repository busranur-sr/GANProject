from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect("home")
        else:
            error_occurred = False
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, error)
                    error_occurred = True
                    break
                if error_occurred:
                    break
            # If there's an error in the form, display the filled form to the user
            context = {"form": form}
    else:
        form = SignUpForm()

    context = {"form": form}
    return render(request, "account/signup.html", context)
