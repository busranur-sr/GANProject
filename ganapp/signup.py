from base64 import urlsafe_b64encode
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth.models import User
from django.contrib.auth import login
from django.shortcuts import redirect
from django.contrib import messages
from django.shortcuts import render
from django.contrib.auth.tokens import default_token_generator
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

class SignUpForm(UserCreationForm):
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ("username", "email", "password1", "password2")


def signup(request):
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()
            
            print(user.pk)
            token = default_token_generator.make_token(user)
            print(token)
            mail_subject = 'Activate your account.'
            message = render_to_string('account/email/email_confirmation_signup.html', {
                'user': user,
                'domain': "localhost:8000",
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': token,
            })

            email = EmailMessage(
                mail_subject, message, to=[user.email]
            )
            email.send()
            context = {"form": form}
            return render(request, "account/email_sent.html", context)
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

def activate(request, uidb64, token):
    try:
        print( "yes")
        uid = force_str(urlsafe_base64_decode(uidb64))
        print(uid)
        user = User.objects.get(pk=uid)
        print(user)
        print(token)
        return render(request, "account/activation_success.html")

        if default_token_generator.check_token(user, token):
            user.is_active = True
            user.save()
            login(request, user)
            return render(request, "account/activation_success.html")
        else:
            return render(request, "account/activation_invalid.html")
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        return render(request, "account/activation_invalid.html")
