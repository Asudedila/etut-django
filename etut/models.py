from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver


class Etut(models.Model):
    OGRETMEN = 'ogretmen'
    OGRENCI = 'ogrenci'

    STATUS = [
        ('bos', 'Boş'),
        ('rezerve', 'Rezerve'),
        ('iptal', 'İptal Edildi'),
    ]

    ogretmen = models.ForeignKey(User, on_delete=models.CASCADE, related_name='verdigim_etutler')
    ogrenci = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True, related_name='aldigim_etutler')
    tarih = models.DateField()
    saat = models.TimeField()
    durum = models.CharField(max_length=10, choices=STATUS, default='bos')

    def __str__(self):
        return f"{self.tarih} - {self.saat} / {self.ogretmen.username}"


class Profil(models.Model):
    ROLLER = [
        ('ogrenci', 'Öğrenci'),
        ('ogretmen', 'Öğretmen'),
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    rol = models.CharField(max_length=10, choices=ROLLER)

    def __str__(self):
        return f"{self.user.username} ({self.rol})"
    @receiver(post_save, sender=User)
    def profil_olustur(sender, instance, created, **kwargs):
        if created:
            Profil.objects.create(user=instance)