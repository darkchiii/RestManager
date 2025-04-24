from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    business_code = forms.CharField(required=False)
    role = forms.ChoiceField(choices=[('EMPLOYEE', 'Employee'), ('EMPLOYER', 'Employer')], widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]