from django.db import models
from django.utils.text import slugify

class Region(models.Model):
    """Les 10 régions du Cameroun (ex: Sud, Centre...)"""
    nom = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nom)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nom

    class Meta:
        verbose_name = "Région"
        verbose_name_plural = "Régions"


class Departement(models.Model):
    """Les 58 départements du Cameroun (ex: Vallée du Ntem...)"""
    region = models.ForeignKey(Region, on_delete=models.CASCADE, related_name='departements')
    nom = models.CharField(max_length=100)
    slug = models.SlugField(max_length=150, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            # Sécurisation du slug en incluant la région pour éviter les doublons
            self.slug = slugify(f"{self.nom}-{self.region.nom}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nom} ({self.region.nom})"

    class Meta:
        verbose_name = "Département"
        verbose_name_plural = "Départements"
        unique_together = ('region', 'nom')


class Mairie(models.Model):
    """Table unique, centrale et clonable pour chaque commune abonnée"""
    departement = models.ForeignKey(Departement, on_delete=models.CASCADE, related_name='mairies')
    nom = models.CharField(max_length=150)
    slug = models.SlugField(max_length=250, unique=True, blank=True)
    
    # Données exclusives de la vitrine annuelle du Maire engagé
    nom_du_maire = models.CharField(max_length=200, blank=True, null=True, verbose_name="Nom complet du Maire")
    mot_du_maire = models.TextField(blank=True, null=True, verbose_name="Mot de l'Exécutif Municipal")
    photo_du_maire = models.ImageField(upload_to='maires/', blank=True, null=True, verbose_name="Photo officielle")
    armoiries = models.ImageField(upload_to='armoiries/', blank=True, null=True, verbose_name="Armoiries de la ville")
    
    est_premium = models.BooleanField(default=False, help_text="Cochez pour activer l'espace vitrine de la commune")
    
    # Sécurité d'accès pour l'équipe de communication de la mairie
    code_secret_admin = models.CharField(max_length=50, blank=True, null=True, verbose_name="Code secret d'accès Admin", help_text="Code unique requis pour modifier la vitrine")
    
    # Blocs de publication annuelle autonome
    histoire = models.TextField(blank=True, null=True, verbose_name="Histoire de la commune")
    geographie = models.TextField(blank=True, null=True, verbose_name="Géographie et Climat")
    aspect_socio_economique = models.TextField(blank=True, null=True, verbose_name="Aspect Socio-Économique")
    vision_mairie = models.TextField(blank=True, null=True, verbose_name="Vision stratégique de la Commune")
    projets_court_terme = models.TextField(blank=True, null=True, verbose_name="Chantiers à Court Terme")
    projets_long_terme = models.TextField(blank=True, null=True, verbose_name="Grands Projets à Long Terme")
    
    email_contact = models.EmailField(blank=True, null=True, verbose_name="E-mail de contact")
    telephone = models.CharField(max_length=50, blank=True, null=True, verbose_name="Téléphone Secrétariat")
    adresse_physique = models.CharField(max_length=255, blank=True, null=True, verbose_name="Adresse physique")

    def save(self, *args, **kwargs):
        if not self.slug:
            # Sécurisation du slug en incluant le département pour éviter tout conflit d'homonyme
            self.slug = slugify(f"{self.nom}-{self.departement.nom}")
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Mairie de {self.nom}"

    class Meta:
        verbose_name = "Mairie"
        verbose_name_plural = "Mairies"
        unique_together = ('departement', 'nom')


class DocumentMunicipal(models.Model):
    """Téléversement autonome de documents (Appels d'offres / Bulletins municipaux)"""
    TYPE_CHOICES = [
        ('APPEL_OFFRE', "Appel d'Offres / Marché Public"),
        ('BULLETIN', 'Bulletin / Journal Municipal'),
    ]
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='documents')
    titre = models.CharField(max_length=200)
    type_document = models.CharField(max_length=20, choices=TYPE_CHOICES, default='BULLETIN')
    fichier_pdf = models.FileField(upload_to='documents_mairies/')
    date_publication = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.titre} - {self.mairie.nom}"

    class Meta:
        verbose_name = "Document Municipal"
        verbose_name_plural = "Documents Municipaux"


class DeclarationEtatCivil(models.Model):
    """Registre de traitement d'état civil rattaché par commune"""
    STATUT_CHOICES = [
        ('RECU', 'Dossier Reçu / En attente'),
        ('VALIDE', 'Validé & Signé / Registre Ouvert'),
        ('REJETE', 'Dossier Incomplet / Rejeté'),
    ]
    mairie = models.ForeignKey(Mairie, on_delete=models.CASCADE, related_name='actes')
    type_acte = models.CharField(max_length=20, verbose_name="Nature de l'acte")
    nom_concerne = models.CharField(max_length=200, verbose_name="Nom du Citoyen concerné")
    nom_declarant = models.CharField(max_length=200, verbose_name="Nom du déclarant")
    telephone_declarant = models.CharField(max_length=50, verbose_name="Contact WhatsApp")
    statut_dossier = models.CharField(max_length=20, choices=STATUT_CHOICES, default='RECU')
    numero_registre_futur = models.CharField(max_length=50, blank=True, null=True, verbose_name="Numéro de Registre")
    date_depot = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type_acte} - {self.nom_concerne} ({self.mairie.nom})"

    class Meta:
        verbose_name = "Déclaration État Civil"
        verbose_name_plural = "Mairies : État Civil en ligne"