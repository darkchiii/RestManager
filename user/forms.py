from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .utils import is_valid_business_code

class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    business_code = forms.CharField(required=False)
    role = forms.ChoiceField(choices=[('EMPLOYEE', 'Employee'), ('EMPLOYER', 'Employer')], widget=forms.RadioSelect)

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"]

    def clean_business_code(self):
        business_code = self.cleaned_data.get('business_code')

        if not is_valid_business_code(business_code):
            raise ValidationError('Kod jest nieprawidłowy.')
        return business_code