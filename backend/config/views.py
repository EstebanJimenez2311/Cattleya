import json

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

from .chatbot_service import generate_reply, get_health


def healthcheck(request):
    return JsonResponse({"status": "ok", "service": "cattleya-backend"})


def chatbot_healthcheck(request):
    return JsonResponse(get_health())


@csrf_exempt
def chatbot_chat(request):
    if request.method != "POST":
        return JsonResponse({"error": "Metodo no permitido"}, status=405)

    try:
        data = json.loads(request.body.decode("utf-8"))
    except (json.JSONDecodeError, UnicodeDecodeError):
        return JsonResponse({"error": "JSON invalido"}, status=400)

    messages = data.get("messages")
    if not isinstance(messages, list) or not messages:
        return JsonResponse({"error": "Se requiere el campo 'messages'"}, status=400)

    result = generate_reply(messages)
    if result["ok"]:
        return JsonResponse({"reply": result["reply"], "model": result["model"]}, status=result["status"])

    return JsonResponse({"error": result["error"]}, status=result["status"])
