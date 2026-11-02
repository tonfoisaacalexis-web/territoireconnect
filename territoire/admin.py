from django.contrib import admin
from .models import Region, Departement, Mairie, DocumentMunicipal, DeclarationEtatCivil

@admin.register(Region)
class RegionAdmin(admin.ModelAdmin):
    list_display = ('nom', 'slug')
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(Departement)
class DepartementAdmin(admin.ModelAdmin):
    list_display = ('nom', 'region', 'slug')
    list_filter = ('region',)
    search_fields = ('nom',)
    prepopulated_fields = {'slug': ('nom',)}

@admin.register(Mairie)
class MairieAdmin(admin.ModelAdmin):
    list_display = ('nom', 'departement', 'est_premium', 'code_secret_admin')
    list_filter = ('est_premium', 'departement__region')
    search_fields = ('nom', 'nom_du_maire')
    # Regroupement par section pour une interface claire
    fieldsets = (
        ('Localisation Administrative', {
            'fields': ('departement', 'nom', 'slug')
        }),
        ('Sécurité & Droits d\'accès', {
            'fields': ('est_premium', 'code_secret_admin'),
            'description': 'Configurez le code unique pour permettre à l\'équipe de communication de publier.'
        }),
        ('Identité de la Mairie', {
            'fields': ('nom_du_maire', 'photo_du_maire', 'armoiries', 'mot_du_maire')
        }),
        ('Contenu Éditorial (Vitrine)', {
            'classes': ('collapse',), # Section repliable
            'fields': ('histoire', 'geographie', 'aspect_socio_economique', 'vision_mairie', 'projets_court_terme', 'projets_long_terme')
        }),
        ('Coordonnées de Contact', {
            'fields': ('email_contact', 'telephone', 'adresse_physique')
        }),
    )

@admin.register(DocumentMunicipal)
class DocumentMunicipalAdmin(admin.ModelAdmin):
    list_display = ('titre', 'mairie', 'type_document', 'date_publication')
    list_filter = ('type_document', 'date_publication')
    search_fields = ('titre', 'mairie__nom')

@admin.register(DeclarationEtatCivil)
class DeclarationEtatCivilAdmin(admin.ModelAdmin):
    list_display = ('type_acte', 'nom_concerne', 'mairie', 'statut_dossier', 'date_depot')
    list_filter = ('statut_dossier', 'type_acte', 'date_depot')
    search_fields = ('nom_concerne', 'nom_declarant', 'numero_registre_futur')
    actions = ['marquer_comme_valide', 'marquer_comme_rejete']

    def marquer_comme_valide(self, request, queryset):
        queryset.update(statut_dossier='VALIDE')
    marquer_comme_valide.short_description = "Valider et signer les dossiers sélectionnés"

    def marquer_comme_rejete(self, request, queryset):
        queryset.update(statut_dossier='REJETE')
    marquer_comme_rejete.short_description = "Marquer comme Incomplet / Rejeté"