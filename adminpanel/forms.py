from django import forms
from .models import TmUser
from django.contrib.auth.hashers import make_password

class RegisterTmUser(forms.ModelForm):

    password1 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Enter Password',
                'type':'password',
                'id':'exampleInputPassword',
            }
        ),
        label='Password'
    )

    password2 = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Repeat Password',
                'type':'password',
                'id':'exampleRepeatPassword',
            }
        ),
        label='Konfirmasi Password'
    )

    class Meta:
        model = TmUser
        fields = ['s_first_name','s_last_name','s_email']
        widgets = {
            's_first_name': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Enter First Name',
                }
            ),
            's_last_name': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Enter Last Name',
                }
            ),
            's_email': forms.EmailInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Enter Email Address',
                    'type':'email',
                    'id':'exampleInputEmail',
                }
            ),
        }
    
    def clean(self):
        cleaned_data = super().clean()
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')

        if password1 and password2 and password1 != password2:
            raise forms.ValidationError("Passwords don't match")
        cleaned_data['s_password'] = make_password(password1)
        return cleaned_data

    def save(self, commit=True):
        TmUser = super().save(commit=False)
        TmUser.s_password = self.cleaned_data['s_password']
        if commit:
            TmUser.save()
        return TmUser


class LoginTmUser(forms.Form):
    s_email = forms.EmailField(
        widget=forms.EmailInput(
            attrs={
                'class':'form-control form-control-user',
                'placeholder':'Enter Email Address',
                'type':'email',
                'id':'exampleInputEmail',
            }
        ),
        label='Email'
    )
    s_password = forms.CharField(
        widget=forms.PasswordInput(
            attrs={
                'class':'form-control form-control-user',
                'placeholder': 'Enter Password',
                'type':'password',
                'id':'exampleInputPassword',
            }
        ),
        label='Password'
    )

    class Meta:
        model = TmUser
        fields = ['s_email','s_password']
        widgets = {
            's_password': forms.TextInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Enter Password',
                    'type':'password',
                    'id':'exampleInputPassword',
                }
            ),
            's_email': forms.EmailInput(
                attrs={
                    'class':'form-control form-control-user',
                    'placeholder':'Enter Email Address',
                    'type':'email',
                    'id':'exampleInputEmail',
                }
            ),
        }