"""Views: register, login, logout."""

from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.utils.http import url_has_allowed_host_and_scheme

from .forms import StudentLoginForm, StudentRegistrationForm


def register_view(request):
    """Create a new student account and log them in."""
    if request.user.is_authenticated:
        return redirect("results:dashboard")

    if request.method == "POST":
        form = StudentRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful. Welcome!")
            return redirect("results:dashboard")
    else:
        form = StudentRegistrationForm()

    return render(request, "accounts/register.html", {"form": form})


def login_view(request):
    """Authenticate student by registration number and password."""
    if request.user.is_authenticated:
        return redirect("results:dashboard")

    if request.method == "POST":
        form = StudentLoginForm(request.POST)
        if form.is_valid():
            reg = form.cleaned_data["registration_number"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=reg, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, "Logged in successfully.")
                next_url = request.POST.get("next") or request.GET.get("next")
                if next_url and url_has_allowed_host_and_scheme(
                    url=next_url,
                    allowed_hosts={request.get_host()},
                    require_https=request.is_secure(),
                ):
                    return redirect(next_url)
                return redirect("results:dashboard")
            messages.error(request, "Invalid registration number or password.")
    else:
        form = StudentLoginForm()

    return render(request, "accounts/login.html", {"form": form})


@login_required
def logout_view(request):
    """Log out the current user."""
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect("accounts:login")
