from noticias.models import Noticia


def cattleya_admin_context(request):
    if not request.path.startswith("/admin/"):
        return {}

    total_noticias = Noticia.objects.count()
    verificadas = Noticia.objects.filter(verificada=True).count()
    riesgo_alto = Noticia.objects.filter(nivel_riesgo__in=["alto", "critico"]).count()
    fuentes_activas = (
        Noticia.objects.exclude(fuente__isnull=True)
        .exclude(fuente__exact="")
        .values("fuente")
        .distinct()
        .count()
    )

    return {
        "cattleya_admin_metrics": [
            {
                "label": "Noticias registradas",
                "value": total_noticias,
                "accent": "magenta",
            },
            {
                "label": "Casos verificados",
                "value": verificadas,
                "accent": "orange",
            },
            {
                "label": "Riesgo alto",
                "value": riesgo_alto,
                "accent": "plum",
            },
            {
                "label": "Fuentes activas",
                "value": fuentes_activas,
                "accent": "gold",
            },
        ],
        "cattleya_admin_summary": {
            "total_noticias": total_noticias,
            "verificadas": verificadas,
        },
    }
