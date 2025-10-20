from django import forms
from about.models import About

class AboutForm(forms.ModelForm):
    class Meta:
        model = About
        fields = ['s_title', 's_description', 'n_istatus']
        labels = {
            's_title': 'Judul About',
            's_description': 'Deskripsi About',
            'n_istatus': 'Status About',
        }
        widgets = {
            's_description': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis deskripsi About di sini...',
                'rows': 3
            }),
            's_title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Tulis Judul About di sini...',
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
                'required': "Silakan pilih status About.",
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
    
    # Validasi gabungan antar field
    def clean(self):
        cleaned_data = super().clean()
        desc = cleaned_data.get('s_description')
        status = cleaned_data.get('n_istatus')
        # Contoh validasi antar field
        if status == '1' and not desc:
            raise forms.ValidationError("Kalau status aktif, deskripsi harus diisi!")

        return cleaned_data