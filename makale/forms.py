from django import forms
from django.contrib.auth.models import User
from .models import Profil

class KullaniciKayitForm(forms.ModelForm):
    sifre = forms.CharField(widget=forms.PasswordInput)
    sifre_tekrar = forms.CharField(widget=forms.PasswordInput)
    rol = forms.ChoiceField(choices=Profil.ROLLER)

    class Meta:
        model = User
        fields = ['username', 'email', 'sifre', 'sifre_tekrar', 'rol']

    def clean(self):
        cleaned_data = super().clean()
        sifre = cleaned_data.get("sifre")
        sifre_tekrar = cleaned_data.get("sifre_tekrar")

        if sifre != sifre_tekrar:
            raise forms.ValidationError("Şifreler eşleşmiyor!")

        return cleaned_data
