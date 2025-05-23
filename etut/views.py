from django.shortcuts import render, redirect, get_object_or_404
from .models import Etut
from django.contrib.auth.decorators import login_required
from .forms import KullaniciKayitForm
from django.contrib.auth import login
from django.contrib.auth.models import User
from datetime import date


def kayit(request):
    if request.method == "POST":
        form = KullaniciKayitForm(request.POST)
        if form.is_valid():
            user = User.objects.create_user(
                username=form.cleaned_data["username"],
                email=form.cleaned_data["email"],
                password=form.cleaned_data["sifre"]
            )
            user.save()
            user.profil.rol = form.cleaned_data["rol"]
            user.profil.save()

            login(request, user)  
            return redirect("anasayfa")
    else:
        form = KullaniciKayitForm()

    return render(request, "kayit.html", {"form": form})

@login_required
def anasayfa(request):
    etutler = Etut.objects.all()

    gelecek_etutler = []
    gecmis_etutler = []

    if request.user.profil.rol == 'ogrenci':
        bugun = date.today()
        rezerve_etutler = Etut.objects.filter(ogrenci=request.user).order_by('tarih', 'saat')
        gelecek_etutler = rezerve_etutler.filter(tarih__gte=bugun)
        gecmis_etutler = rezerve_etutler.filter(tarih__lt=bugun)

    return render(request, 'anasayfa.html', {
        'etutler': etutler,
        'gelecek_etutler': gelecek_etutler,
        'gecmis_etutler': gecmis_etutler,
    })
@login_required
def etut_ekle(request):
    if request.user.profil.rol != "ogretmen":
        return HttpResponse("Yetkisiz erişim!")

    if request.method == 'POST':
        tarih = request.POST.get('tarih')
        saat = request.POST.get('saat')
        Etut.objects.create(ogretmen=request.user, tarih=tarih, saat=saat)
        return redirect('anasayfa')
    return render(request, 'etut_ekle.html')

@login_required
def etut_rezerve(request, id):
    etut = get_object_or_404(Etut, id=id)
    if etut.durum == 'bos':
        etut.ogrenci = request.user
        etut.durum = 'rezerve'
        etut.save()
    return redirect('anasayfa')

@login_required
def etut_iptal(request, id):
    etut = get_object_or_404(Etut, id=id)
    if etut.ogrenci == request.user:
        etut.ogrenci = None
        etut.durum = 'bos'
        etut.save()
    return redirect('anasayfa')
from django.contrib.auth.decorators import login_required
from .models import Etut

