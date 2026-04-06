from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.db.models import Count, Q
from django.db.models.functions import TruncMonth
from django.db.models import Value
from django.db.models.functions import Coalesce
from datetime import datetime, timedelta

from noticias.models import Noticia
from .serializers import ResumenViewSerializer, TendenciaSerializer, TiposViolenciaSerializer


class ResumenView(APIView):
    """
    GET /api/estadisticas/resumen/
    Retorna estadísticas generales de noticias
    """
    
    def get(self, request):
        # Total de noticias
        noticias = Noticia.objects.all()
        total_noticias = noticias.count()
        total_verificadas = noticias.filter(verificada=True).count()
        
        # Conteo por tipo de violencia
        tipos_violencia = {
            'fisica': noticias.filter(violencia_fisica=True).count(),
            'psicologica': noticias.filter(violencia_psicologica=True).count(),
            'sexual': noticias.filter(violencia_sexual=True).count(),
            'economica': noticias.filter(violencia_economica=True).count(),
            'patrimonial': noticias.filter(violencia_patrimonial=True).count(),
            'feminicidio': noticias.filter(feminicidio=True).count(),
        }
        
        # Conteo por ámbito
        ambitos = {
            'familiar': noticias.filter(ambito_violencia='familiar').count(),
            'pareja': noticias.filter(ambito_violencia='pareja').count(),
            'comunitario': noticias.filter(ambito_violencia='comunitario').count(),
            'institucional': noticias.filter(ambito_violencia='institucional').count(),
        }
        
        # Top 10 ciudades
        ciudades_top = list(
            noticias
            .values('ciudad')
            .annotate(count=Count('id'))
            .order_by('-count')[:10]
            .values_list('ciudad', 'count')
        )
        
        data = {
            'total_noticias': total_noticias,
            'total_verificadas': total_verificadas,
            'tipos_violencia': tipos_violencia,
            'ambitos': ambitos,
            'ciudades_top': [{'ciudad': c[0], 'cantidad': c[1]} for c in ciudades_top],
        }
        
        serializer = ResumenViewSerializer(data)
        return Response(serializer.data)


class TendenciaView(APIView):
    """
    GET /api/estadisticas/tendencia/
    Retorna tendencias de noticias por mes
    """
    
    def get(self, request):
        noticias = Noticia.objects.all()
        
        # Agrupar por mes
        tendencias = noticias.annotate(
            mes=TruncMonth('fecha_publicacion')
        ).values('mes').annotate(
            total=Count('id'),
            verificadas=Count('id', filter=Q(verificada=True)),
        ).order_by('mes')
        
        datos = []
        for item in tendencias:
            if item['mes'] is None:
                continue
                
            mes = item['mes']
            mes_str = mes.strftime('%Y-%m')
            
            # Contar tipos de violencia en este mes
            noticias_mes = noticias.filter(
                fecha_publicacion__year=mes.year,
                fecha_publicacion__month=mes.month
            )
            
            tipos_mes = {
                'fisica': noticias_mes.filter(violencia_fisica=True).count(),
                'psicologica': noticias_mes.filter(violencia_psicologica=True).count(),
                'sexual': noticias_mes.filter(violencia_sexual=True).count(),
                'economica': noticias_mes.filter(violencia_economica=True).count(),
                'patrimonial': noticias_mes.filter(violencia_patrimonial=True).count(),
                'feminicidio': noticias_mes.filter(feminicidio=True).count(),
            }
            
            datos.append({
                'mes': mes_str,
                'total': item['total'],
                'verificadas': item['verificadas'],
                'tipos_violencia': tipos_mes,
            })
        
        serializer = TendenciaSerializer(datos, many=True)
        return Response(serializer.data)


class TiposViolenciaView(APIView):
    """
    GET /api/estadisticas/tipos/
    Retorna conteo y porcentaje de cada tipo de violencia
    """
    
    def get(self, request):
        noticias = Noticia.objects.all()
        total = noticias.count()
        
        if total == 0:
            return Response([])
        
        tipos = [
            ('Física', noticias.filter(violencia_fisica=True).count()),
            ('Psicológica', noticias.filter(violencia_psicologica=True).count()),
            ('Sexual', noticias.filter(violencia_sexual=True).count()),
            ('Económica', noticias.filter(violencia_economica=True).count()),
            ('Patrimonial', noticias.filter(violencia_patrimonial=True).count()),
            ('Feminicidio', noticias.filter(feminicidio=True).count()),
        ]
        
        datos = [
            {
                'tipo': tipo,
                'cantidad': cantidad,
                'porcentaje': round((cantidad / total) * 100, 2),
            }
            for tipo, cantidad in tipos
            if cantidad > 0  # Solo retornar tipos con al menos 1 incidencia
        ]
        
        datos.sort(key=lambda x: x['cantidad'], reverse=True)
        
        serializer = TiposViolenciaSerializer(datos, many=True)
        return Response(serializer.data)
