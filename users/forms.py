import datetime

from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, PasswordChangeForm


class LoginUserForm(AuthenticationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password = forms.CharField(label="Пароль",
                               widget=forms.PasswordInput(
                                   attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'password']


class RegisterUserForm(UserCreationForm):
    username = forms.CharField(label="Логин",
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    password1 = forms.CharField(label="Пароль",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))
    password2 = forms.CharField(label="Повтор пароля",
                                widget=forms.PasswordInput(
                                    attrs={'class': 'form-control'}))

    class Meta:
        model = get_user_model()
        fields = ['username', 'email', 'first_name', 'last_name',
                  'password1', 'password2']
        labels = {
            'email': 'E-mail',
            'first_name': "Имя",
            'last_name': "Фамилия",
        }
        widgets = {
            'email': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }

    def clean_email(self):
        email = self.cleaned_data['email']
        if get_user_model().objects.filter(email=email).exists():
            raise forms.ValidationError("Такой E-mail уже существует!")
        return email


class ProfileUserForm(forms.ModelForm):
    username = forms.CharField(disabled=True, label='Логин',
                               widget=forms.TextInput(
                                   attrs={'class': 'form-control'}))
    email = forms.CharField(disabled=True, label='E-mail',
                            widget=forms.TextInput(
                                attrs={'class': 'form-control'}))
    this_year = datetime.date.today().year
    date_birth = forms.DateField(label='День рождения',
                                 widget=forms.SelectDateWidget(
                                     attrs={'class': 'form-control'},
                                     years=tuple(range(this_year-100,
                                                       this_year-5))))

    class Meta:
        model = get_user_model()
        fields = ['photo', 'username', 'email',
                  'date_birth', 'first_name', 'last_name']
        labels = {
            'first_name': 'Имя',
            'last_name': 'Фамилия',
        }
        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
        }


class UserPasswordChangeForm(PasswordChangeForm):
    old_password = forms.CharField(label="Старый пароль",
                                   widget=forms.PasswordInput(
                                       attrs={'class': 'form-control'}))
    new_password1 = forms.CharField(label="Новый пароль",
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
    new_password2 = forms.CharField(label="Подтверждение пароля",
                                    widget=forms.PasswordInput(
                                        attrs={'class': 'form-control'}))
