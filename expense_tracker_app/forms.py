from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import AuthenticationForm
from .models import Expense
from datetime import date


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Confirm password'})
    )

    class Meta:
        model = User
        fields = ['username', 'email']
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Enter email'}),
        }

    def clean(self):
        cleaned_data = super().clean()

        username = cleaned_data.get("username")
        email = cleaned_data.get("email")
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if username and User.objects.filter(username=username).exists():
            self.add_error("username", "Username already exists.")
            return cleaned_data 

        if email and User.objects.filter(email=email).exists():
            self.add_error("email", "Email already registered.")
            return cleaned_data  

        if password and confirm_password and password != confirm_password:
            self.add_error("confirm_password", "Passwords do not match.")

        return cleaned_data






# Login Form
class UserLoginForm(AuthenticationForm):
    username = forms.CharField(
        widget=forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Enter username'})
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Enter password'})
    )


#Expense Form
class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ["date", "category", "amount", "description"]

        widgets = {
            "date": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "category": forms.Select(attrs={"class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control", "min": "1"}),
            "description": forms.Textarea(attrs={"class": "form-control", "rows": 3}),
        }





    # 👇 Add this function
    def clean_date(self):
        selected_date = self.cleaned_data.get("date")
        if selected_date and selected_date > date.today():
            raise ValidationError("Future dates are not allowed.")
        return selected_date



#Expense FilterForm
class ExpenseFilterForm(forms.Form):
    CATEGORY_CHOICES = [
        ("", "All Categories"),  # Default option
        ("Food", "Food"),
        ("Travel", "Travel"),
        ("Shopping", "Shopping"),
        ("Bills", "Bills"),
        ("Health", "Health"),
        ("Other", "Other"),
    ]
    category = forms.ChoiceField(choices=CATEGORY_CHOICES, required=False, widget=forms.Select(attrs={
        "class": "form-control"
    }))
