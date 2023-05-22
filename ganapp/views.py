import tempfile
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect
from django import forms
from django.core.files.base import ContentFile
from ganapp.forms import ImageUploadForm
from ganapp.generator import Cartoonize
from ganapp.models import UserImage
import os
import matplotlib.pyplot as plt
import numpy as np
import time

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from .models import UserImage
from django.contrib.auth.decorators import login_required

from django.shortcuts import get_object_or_404
from django.http import JsonResponse

from django.shortcuts import render
from .models import UserImage
from ganapp.signup import signup


def login_view(request):
    if request.method == "POST":
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            if user.is_superuser:
                return redirect("admin:index")
            else:
                return redirect("home")
        else:
            # Invalid login
            return render(
                request, "login.html", {"error": "Invalid username or password"}
            )
    else:
        return render(request, "login.html")


from django.contrib.auth.decorators import login_required

from django import forms


class ImageUploadForm(forms.Form):
    image = forms.ImageField(label="Upload Image")


@login_required
def home_view(request):
    if request.method == "POST":
        form = ImageUploadForm(request.POST, request.FILES)
        if form.is_valid():
            cartoonizer = Cartoonize()
            with tempfile.NamedTemporaryFile(delete=False, suffix=".png") as temp:
                temp.write(request.FILES["image"].read())
                cartoon_image = cartoonizer.forward(temp.name)
                # Save the original image and the cartoonized image to the database
                user_image = UserImage(
                    user=request.user,
                    image=request.FILES["image"],
                    output_image=cartoon_image,
                )
                user_image.save()
                # Add delay to simulate AI processing time
                time.sleep(5)  # Adjust the delay duration as needed
                return JsonResponse({"success": True})
    else:
        form = ImageUploadForm()

    user_images = UserImage.objects.filter(user=request.user).last()
    return render(request, "home.html", {"form": form, "user_images": user_images})


def logout_view(request):
    logout(request)
    return redirect("login")




@login_required
def archive_view(request):
    # Retrieve all the generated images for the current user
    user_images = UserImage.objects.filter(user=request.user)
    return render(request, "archive.html", {"user_images": user_images})


def delete_image(request, image_id):
    if request.method == "POST":
        image = get_object_or_404(UserImage, id=image_id)
        image.delete()
        return JsonResponse({"success": True})
    else:
        return JsonResponse({"success": False})
