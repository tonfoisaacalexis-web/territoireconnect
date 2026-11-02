from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
# Ajout de Region dans les imports pour la page d'accueil
from .models import Mairie, DocumentMunicipal, Region

def accueil_portail(request):
    """Affiche la page d'accueil nationale (liste des mairies du Cameroun classées par région)"""
    regions = Region.objects.all()
    mairies = Mairie.objects.all()
    return render(request, 'territoire/accueil.html', {
        'regions': regions,
        'mairies': mairies
    })

def detail_mairie(request, slug):
    """Affiche la page de détails et la vitrine publique d'une commune"""
    mairie = get_object_or_404(Mairie, slug=slug)
    return render(request, 'territoire/detail.html', {'mairie': mairie})

def modifier_vitrine_communale(request, slug):
    """Espace privé sécurisé par code secret unique pour l'équipe de communication"""
    mairie_cible = get_object_or_404(Mairie, slug=slug)
    
    # Si la mairie n'a pas de code secret configuré dans le panel Django Admin, on bloque par sécurité
    if not mairie_cible.code_secret_admin:
        messages.error(request, "L'accès à cet espace n'est pas encore configuré. Contactez l'administrateur système.")
        return redirect('detail_mairie', slug=mairie_cible.slug)

    # Vérification du code secret soumis par session ou par POST
    code_authentifie = request.session.get(f'auth_mairie_{mairie_cible.id}', False)

    if request.method == "POST":
        # Cas 1 : Tentative de connexion avec le code secret
        if 'soumettre_code_secret' in request.POST:
            code_saisi = request.POST.get('code_secret')
            if code_saisi == mairie_cible.code_secret_admin:
                request.session[f'auth_mairie_{mairie_cible.id}'] = True
                messages.success(request, "Connexion réussie à l'espace de publication !")
                return redirect('modifier_vitrine_prive', slug=mairie_cible.slug)
            else:
                messages.error(request, "Code secret incorrect. Veuillez réessayer.")
                return render(request, 'territoire/connexion_prive.html', {'mairie': mairie_cible})

        # Cas 2 : Soumission des modifications (Seulement si déjà authentifié)
        elif code_authentifie:
            mairie_cible.nom_du_maire = request.POST.get('nom_du_maire')
            mairie_cible.mot_du_maire = request.POST.get('mot_du_maire')
            mairie_cible.histoire = request.POST.get('histoire')
            mairie_cible.geographie = request.POST.get('geographie')
            mairie_cible.vision_mairie = request.POST.get('vision_mairie')
            mairie_cible.projets_court_terme = request.POST.get('projets_court_terme')
            mairie_cible.projets_long_terme = request.POST.get('projets_long_terme')
            
            if request.FILES.get('photo_du_maire'):
                mairie_cible.photo_du_maire = request.FILES.get('photo_du_maire')
                
            mairie_cible.save()
            messages.success(request, f"✨ Les publications de la Mairie de {mairie_cible.nom} ont été mises à jour !")
            return redirect('detail_mairie', slug=mairie_cible.slug)

    # Si l'utilisateur n'est pas authentifié par session, on affiche la page de verrouillage
    if not code_authentifie:
        return render(request, 'territoire/connexion_prive.html', {'mairie': mairie_cible})
        
    return render(request, 'territoire/publier_vitrine.html', {'mairie': mairie_cible})