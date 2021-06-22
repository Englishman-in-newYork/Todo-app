from django import forms
from django.contrib.auth.models import User
from django.forms import ModelForm, TextInput, Textarea, HiddenInput
from .models import *



class LoginForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Loggin"
        self.fields["password"].label = "Password"

    def clean(self):
        username = self.cleaned_data["username"]
        password = self.cleaned_data["password"]
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f"User {username} not found")
        user = User.objects.filter(username=username).first()
        if user:
            if not user.check_password(password):
                raise forms.ValidationError("Invalid password")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ["username", "password"]


class RegistrationForm(forms.ModelForm):

    confirm_password = forms.CharField(widget=forms.PasswordInput)
    password = forms.CharField(widget=forms.PasswordInput)
    phone = forms.CharField(required=False)
    address = forms.CharField(required=False)
    email = forms.EmailField(required=True)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["username"].label = "Loggin"
        self.fields["password"].label = "Password"
        self.fields["confirm_password"].label = "Confirm password"
        self.fields["email"].label = "Email"

    def clean_email(self):
        email = self.cleaned_data["email"]
        if User.objects.filter(email = email).exists():
            raise forms.ValidationError (f"This email address is already registered")
        return email

    def clean_username(self):
        username = self.cleaned_data["username"]
        if User.objects.filter(username = username).exists():
            raise forms.ValidationError (f"Name {username} is already exist")
        return username

    def clean(self):
        password = self.cleaned_data["password"]
        confirm_password = self.cleaned_data["confirm_password"]
        if password != confirm_password:
            raise forms.ValidationError("Passwords don't match")
        return self.cleaned_data

    class Meta:
        model = User
        fields = ["username", "password", "confirm_password", "email"]



class AddNewProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ["title"]

        widgets = {
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder" : "Project name"
            })
        }

class AddNewTaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "project"]

        widgets = {
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder" : "Task title"
            }),
            "description": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Task description"}),
            "project": HiddenInput(attrs={
                "class": "form-control",
                "placeholder": "project relate"}),
        }

class UpdateTaskForm(ModelForm):
    class Meta:
        model = Tasks
        fields = ["title", "description", "status_task"]

        widgets = {
            "title": TextInput(attrs={
                "class": "form-control",
                "placeholder" : "Task title"
            }),
            "description": Textarea(attrs={
                "class": "form-control",
                "placeholder": "Task description"}),
        }

