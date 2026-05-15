"""Forms for student registration and login."""

from django import forms
from django.contrib.auth.forms import UserCreationForm

from .models import Student


class StudentRegistrationForm(UserCreationForm):
    """
    Public registration: name, registration number, pass-out year, password.

    Inherits password validation from UserCreationForm.
    """

    name = forms.CharField(
        max_length=120,
        label="Full name",
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "name"}),
    )
    pass_out_year = forms.IntegerField(
        min_value=1990,
        max_value=2100,
        label="Pass out year",
        help_text="Your graduation year — results are shown for this year.",
        widget=forms.NumberInput(attrs={"class": "form-control", "min": 1990, "max": 2100}),
    )

    class Meta:
        model = Student
        fields = ("registration_number", "name", "pass_out_year", "password1", "password2")

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Bootstrap styling for fields provided by UserCreationForm + our extras
        self.fields["registration_number"].widget.attrs.update(
            {"class": "form-control", "autocomplete": "username"}
        )
        self.fields["password1"].widget.attrs.update({"class": "form-control", "autocomplete": "new-password"})
        self.fields["password2"].widget.attrs.update({"class": "form-control", "autocomplete": "new-password"})

    def clean_registration_number(self):
        """Normalize registration number to uppercase without leading/trailing spaces."""
        reg = self.cleaned_data.get("registration_number", "")
        return str(reg).strip().upper()


class StudentLoginForm(forms.Form):
    """Login with registration number + password."""

    registration_number = forms.CharField(
        max_length=30,
        label="Registration number",
        widget=forms.TextInput(attrs={"class": "form-control", "autocomplete": "username"}),
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={"class": "form-control", "autocomplete": "current-password"}),
    )

    def clean_registration_number(self):
        reg = self.cleaned_data.get("registration_number", "")
        return str(reg).strip().upper()
