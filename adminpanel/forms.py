from django import forms
from .models import TmUser
from blog.models import SliderBanner, Artikel1
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

class SliderBannerForm(forms.ModelForm):
    class Meta:
        model = SliderBanner
        fields = ['s_nama_gambar', 's_description', 'n_istatus']
        labels = {
            's_nama_gambar': 'Gambar Banner',
            's_description': 'Deskripsi Banner',
            'n_istatus': 'Status Banner',
        }
        widgets = {
            's_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis deskripsi banner di sini...',
                'rows': 3
            }),
            'n_istatus': forms.Select(attrs={
                'class': 'form-control'
            }),
        }
        error_messages = {
            's_description': {
                'required': "Deskripsi tidak boleh kosong.",
                'max_length': "Deskripsi terlalu panjang, maksimal 255 karakter.",
            },
            'n_istatus': {
                'required': "Silakan pilih status banner.",
            },
        }

    # Validasi khusus untuk s_description
    def clean_s_description(self):
        desc = self.cleaned_data.get('s_description', '').strip()
        if not desc:
            raise forms.ValidationError("Kamu belum mengisi deskripsi banner.")
        if len(desc) < 10:
            raise forms.ValidationError("Deskripsi harus minimal 10 karakter.")
        return desc

    # Validasi khusus untuk gambar
    def clean_s_nama_gambar(self):
        image = self.cleaned_data.get('s_nama_gambar')
        if not image:
            raise forms.ValidationError("Kamu belum memilih file gambar.")
        if hasattr(image, 'size') and image.size > 2 * 1024 * 1024:
            raise forms.ValidationError("Ukuran gambar maksimal 2MB.")
        if image:
            if not image.name.lower().endswith(('.jpg', '.jpeg', '.png')):
                raise forms.ValidationError("Hanya boleh upload file JPG atau PNG")
        return image

    # Validasi gabungan antar field
    def clean(self):
        cleaned_data = super().clean()
        desc = cleaned_data.get('s_description')
        status = cleaned_data.get('n_istatus')
        #validasi gambar
        errors_s_nama_gambar = self._errors.get('s_nama_gambar')
        if errors_s_nama_gambar and any("Upload a valid image" in e for e in errors_s_nama_gambar):
            # 🔹 Hapus validasi error bawaan Django
            self._errors['s_nama_gambar'].clear()
            self.add_error('s_nama_gambar', "File yang kamu upload bukan gambar valid. Hanya JPG atau PNG diperbolehkan.")
        # Contoh validasi antar field
        if status == '1' and not desc:
            raise forms.ValidationError("Kalau status aktif, deskripsi harus diisi!")

        return cleaned_data
    
class Artikel1Form(forms.ModelForm):
    class Meta:
        model = Artikel1
        fields = ['s_title', 's_description', 'n_istatus']
        labels = {
            's_title': 'Judul Artikel',
            's_description': 'Deskripsi Artikel',
            'n_istatus': 'Status Artikel',
        }
        widgets = {
            's_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis deskripsi artikel di sini...',
                'rows': 3
            }),
            's_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis Judul Artikel di sini...',
                'rows': 3
            }),
            'n_istatus': forms.Select(attrs={
                'class': 'form-control'
            }),
        }

        error_messages = {
            's_title': {
                'required': "Judul tidak boleh kosong.",
                'max_length': "Judul terlalu panjang, maksimal 100 karakter.",
            },
            's_description': {
                'required': "Deskripsi tidak boleh kosong.",
                'max_length': "Deskripsi terlalu panjang, maksimal 255 karakter.",
            },
            'n_istatus': {
                'required': "Silakan pilih status artikel.",
            },
        }

    # Validasi khusus untuk s_description
    def clean_s_description(self):
        desc = self.cleaned_data.get('s_description', '').strip()
        if not desc:
            raise forms.ValidationError("Kamu belum mengisi deskripsi artikel.")
        if len(desc) < 10:
            raise forms.ValidationError("Deskripsi harus minimal 10 karakter.")
        return desc
    
    # Validasi gabungan antar field
    def clean(self):
        cleaned_data = super().clean()
        desc = cleaned_data.get('s_description')
        status = cleaned_data.get('n_istatus')
        # Contoh validasi antar field
        if status == '1' and not desc:
            raise forms.ValidationError("Kalau status aktif, deskripsi harus diisi!")

        return cleaned_data


    
