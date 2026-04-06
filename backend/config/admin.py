from django.contrib import admin, messages
from django.urls import path
from django.template.response import TemplateResponse
from django.core.management import call_command
from django.shortcuts import redirect


def monitor_view(request):
    from noticias.models import Noticia
    from analisis.models import ResultadoAnalisis

    if request.method == "POST":
        try:
            call_command("cargar_analisis")
            messages.success(request, "cargar_analisis ejecutado correctamente.")
        except Exception as exc:
            messages.error(request, f"Error al ejecutar cargar_analisis: {exc}")
        return redirect("admin:monitor")

    total_analisis = ResultadoAnalisis.objects.count()
    ultima_actualizacion = (
        ResultadoAnalisis.objects.order_by("-actualizado")
        .values_list("actualizado", flat=True)
        .first()
    )
    total_noticias = Noticia.objects.count()
    distribucion_riesgo = {
        "bajo": Noticia.objects.filter(nivel_riesgo="bajo").count(),
        "medio": Noticia.objects.filter(nivel_riesgo="medio").count(),
        "alto": Noticia.objects.filter(nivel_riesgo="alto").count(),
        "critico": Noticia.objects.filter(nivel_riesgo="critico").count(),
    }
    distribucion_ambito = {
        "familiar": Noticia.objects.filter(ambito_violencia="familiar").count(),
        "pareja": Noticia.objects.filter(ambito_violencia="pareja").count(),
        "comunitario": Noticia.objects.filter(ambito_violencia="comunitario").count(),
        "institucional": Noticia.objects.filter(ambito_violencia="institucional").count(),
        "otro": Noticia.objects.filter(ambito_violencia="otro").count(),
    }

    context = {
        "title": "Panel técnico",
        "total_analisis": total_analisis,
        "ultima_actualizacion": ultima_actualizacion,
        "total_noticias": total_noticias,
        "distribucion_riesgo": distribucion_riesgo,
        "distribucion_ambito": distribucion_ambito,
    }

    return TemplateResponse(request, "admin/monitor.html", context)


def get_admin_urls(urls):
    def get_urls():
        custom_urls = [
            path("monitor/", admin.site.admin_view(monitor_view), name="monitor"),
        ]
        return custom_urls + urls()

    return get_urls


admin.site.get_urls = get_admin_urls(admin.site.get_urls)
