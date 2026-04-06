from django.contrib import admin, messages
from django.http import HttpResponseRedirect
from django.urls import path, reverse

from .models import Noticia
from .services.rss_importer import run


@admin.register(Noticia)
class NoticiaAdmin(admin.ModelAdmin):
    change_list_template = "admin/noticias/noticia/change_list.html"
    list_display = (
        "titulo",
        "fuente",
        "ciudad",
        "tipo_violencia",
        "ambito_violencia",
        "nivel_riesgo",
        "verificada",
        "es_prueba",
        "fecha_publicacion",
    )
    list_filter = (
        "ambito_violencia",
        "nivel_riesgo",
        "verificada",
        "es_prueba",
        "ciudad",
        "fecha_publicacion",
        "violencia_fisica",
        "violencia_psicologica",
        "violencia_sexual",
        "violencia_economica",
        "violencia_patrimonial",
        "feminicidio",
    )
    search_fields = ("titulo", "descripcion", "fuente", "ciudad")

    def get_urls(self):
        urls = super().get_urls()
        custom_urls = [
            path(
                "ejecutar-scraping/",
                self.admin_site.admin_view(self.ejecutar_scraping_view),
                name="noticias_noticia_ejecutar_scraping",
            ),
        ]
        return custom_urls + urls

    def changelist_view(self, request, extra_context=None):
        extra_context = extra_context or {}
        extra_context["scrape_url"] = reverse("admin:noticias_noticia_ejecutar_scraping")
        return super().changelist_view(request, extra_context=extra_context)

    def ejecutar_scraping_view(self, request):
        if request.method != "POST":
            return HttpResponseRedirect(reverse("admin:noticias_noticia_changelist"))

        summary = run()
        messages.success(
            request,
            (
                "Scraping ejecutado. "
                f"Guardadas: {summary['saved']}, duplicadas: {summary['duplicates']}, "
                f"filtradas: {summary['filtered']}, errores: {summary['errors']}."
            ),
        )
        return HttpResponseRedirect(reverse("admin:noticias_noticia_changelist"))
