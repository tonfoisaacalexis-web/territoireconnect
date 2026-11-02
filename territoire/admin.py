from django.contrib import admin
from django.utils.html import format_html
from .models import Mairie, Region, Departement, DocumentMunicipal, DeclarationEtatCivil

admin.site.site_header = "TERRITOIRECONNECT Admin"
admin.site.index_title = "Gestion Centrale des Communes"

admin.site.register(Region)
admin.site.register(Departement)
admin.site.register(DocumentMunicipal)

@admin.register(Mairie)
class MairieAdmin(admin.ModelAdmin):
    """Panneau de configuration et d'octroi d'espace pour chaque maire engagé"""
    list_display = ('nom', 'nom_du_maire', 'est_premium', 'bouton_edition_vitrine')
    prepopulated_fields = {'slug': ('nom',)}
    list_filter = ('est_premium',)
    search_fields = ('nom', 'nom_du_maire')

    def bouton_edition_vitrine(self, obj):
        # Lien direct personnalisé par commune : /commune/ambam/admin/
        return format_html(
            '<a class="button" href="/commune/{}/admin/" style="background-color: #059669; color: white; padding: 4px 10px; border-radius: 4px; font-weight: bold; text-decoration: none;">✍️ Éditer la Vitrine</a>',
            obj.slug
        )
    bouton_edition_vitrine.short_description = "Espace Publication"

@admin.register(DeclarationEtatCivil)
class DeclarationEtatCivilAdmin(admin.ModelAdmin):
    list_display = ('nom_concerne', 'type_acte', 'mairie', 'statut_dossier', 'numero_registre_futur')
    list_filter = ('mairie', 'statut_dossier')