from django import forms
from django.contrib.auth import get_user_model
import datetime

from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import Permission


class RegistrateUserForm(UserCreationForm):
    this_year = datetime.date.today().year
    date_birth = forms.DateField(widget=forms.SelectDateWidget(attrs={'class': 'form-control'},
                                                               years=tuple(range(this_year - 100, this_year - 5))))

    password1 = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))
    password2 = forms.CharField(label='Повтор паролю', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = [
            'first_name', 'last_name', 'email', 'username', 'password1', 'password2',
            'photo', 'date_birth'
        ]
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'password1': forms.PasswordInput(attrs={'class': 'form-control'}),
            'password2': forms.PasswordInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такий E-mail вже зайнят!")
        return email

    def save(self, commit=True):
        user = super().save(commit=False)
        user.save()
        add_post_permission = Permission.objects.get(codename='add_post')
        user.user_permissions.add(add_post_permission)

        return user


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label='Логін', widget=forms.TextInput(
        attrs={"class": 'form-control'})
                               )

    password = forms.CharField(label='Пароль', widget=forms.PasswordInput(
        attrs={'class': 'form-control'}
    ))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RedactProfileForm(forms.ModelForm):
    class Meta:
        model = get_user_model()
        fields = ['first_name', 'last_name', 'photo']
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'photo': forms.ClearableFileInput(attrs={'class': 'form-control'}),
        }
