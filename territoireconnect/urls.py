from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
# Importation d'une vue hypothétique pour la page d'accueil (ex: liste_mairies)
from territoire.views import detail_mairie, modifier_vitrine_communale, accueil_portail

urlpatterns = [
    # 🏠 PORTAIL NATIONAL / PAGE D'ACCUEIL (Recherche de commune, sélection par région)
    path('', accueil_portail, name='accueil_portail'),

    # ACCÈS PORTAIL MAÎTRE (Django Admin)
    path('admin/', admin.site.urls),
    
    # 🏙️ ADRESSE PUBLIQUE DU CITOYEN (Ex: /commune/ambam/)
    path('commune/<slug:slug>/', detail_mairie, name='detail_mairie'),
    
    # 🔐 ADRESSE ADMIN DE PUBLICATION DU MAIRE (Ex: /commune/ambam/admin/)
    path('commune/<slug:slug>/admin/', modifier_vitrine_communale, name='modifier_vitrine_prive'),
]

# Prise en charge des fichiers médias ET statiques en mode développement
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)