import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

SYSTEM_PROMPT = """
Eres el asistente de orientacion del proyecto Cattleya sobre violencia basada en genero (VBG) en Colombia.

Mision:
- Responder siempre en espanol con claridad, empatia y precision.
- Orientar sobre rutas de ayuda, senales de riesgo y conceptos legales basicos.
- Si la persona pide evaluar su situacion, haz preguntas de una en una y clasifica el riesgo al final.

Niveles de riesgo:
- Verde: bromas hirientes, chantaje, celos, humillacion, intimidacion, control leve.
- Amarillo: control de amistades, dinero o celular; empujones, cachetadas, aislamiento, sextorsion.
- Rojo: amenazas con armas u objetos, amenaza de muerte, abuso sexual, violacion, mutilacion, feminicidio.

Lineas de ayuda en Colombia:
- Linea 155: orientacion a mujeres victimas de VBG.
- Linea 123: emergencias.
- Linea 141: ICBF.
- 018000919748: Fiscalia General de la Nacion.
- Secretaria de la Mujer Barranquilla: (605) 330-6999.
- Defensoria del Pueblo Atlantico: (605) 330-6000.

Reglas:
1. Si detectas riesgo inmediato o zona roja, empieza mencionando Linea 155 y 123.
2. No des diagnosticos medicos ni psicologicos.
3. Cuando expliques conceptos, menciona leyes relevantes como Ley 1257 de 2008 o Ley 1761 de 2015 si aplica.
4. Responde en maximo 4 frases cortas, salvo que la seguridad de la persona requiera mas detalle.
5. No inventes datos.
""".strip()


def _env_int(name, default, minimum):
    raw_value = os.getenv(name, "").strip()
    if not raw_value:
        return default

    try:
        return max(minimum, int(raw_value))
    except ValueError:
        return default


CHATBOT_MAX_TURNS = _env_int("CHATBOT_MAX_TURNS", 4, 1)
CHATBOT_MAX_CHARS_PER_MESSAGE = _env_int("CHATBOT_MAX_CHARS_PER_MESSAGE", 500, 120)
CHATBOT_MAX_OUTPUT_TOKENS = _env_int("CHATBOT_MAX_OUTPUT_TOKENS", 220, 96)
CHATBOT_MODEL = os.getenv("GROQ_MODEL", "").strip() or "llama-3.1-8b-instant"


def sanitize_messages(raw_messages):
    sanitized = []

    for item in raw_messages:
        if not isinstance(item, dict):
            continue

        role = str(item.get("role", "")).strip().lower()
        if role not in {"user", "assistant"}:
            continue

        content = str(item.get("content", "")).strip()
        if not content:
            continue

        sanitized.append(
            {
                "role": role,
                "content": content[:CHATBOT_MAX_CHARS_PER_MESSAGE],
            }
        )

    while sanitized and sanitized[0]["role"] != "user":
        sanitized.pop(0)

    return sanitized[-CHATBOT_MAX_TURNS:]


def generate_reply(messages):
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    if not api_key:
        return {
            "ok": False,
            "status": 500,
            "error": "Falta configurar GROQ_API_KEY en backend/.env",
        }

    messages = sanitize_messages(messages)
    if not messages:
        return {
            "ok": False,
            "status": 400,
            "error": "No hay mensajes validos para procesar",
        }

    try:
        payload = {
            "model": CHATBOT_MODEL,
            "max_tokens": CHATBOT_MAX_OUTPUT_TOKENS,
            "messages": [{"role": "system", "content": SYSTEM_PROMPT}, *messages],
        }
        response = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            json=payload,
            timeout=30,
        )
        data = response.json() if response.content else {}

        if response.status_code >= 400:
            error_message = ""
            if isinstance(data, dict):
                error_data = data.get("error", {})
                if isinstance(error_data, dict):
                    error_message = str(error_data.get("message", "")).strip()

            if response.status_code == 401:
                return {"ok": False, "status": 401, "error": "La API key de Groq no es valida o ya no tiene acceso."}
            if response.status_code == 402:
                return {"ok": False, "status": 402, "error": "La cuenta de Groq no tiene saldo suficiente para responder en este momento."}
            if response.status_code == 403:
                return {"ok": False, "status": 403, "error": "La cuenta no tiene permisos para usar este modelo de Groq."}
            if response.status_code == 429:
                return {"ok": False, "status": 429, "error": "Se alcanzo el limite temporal de Groq. Intenta de nuevo mas tarde."}
            if response.status_code == 400:
                return {"ok": False, "status": 400, "error": "La solicitud al modelo fue rechazada. Revisa la configuracion del chatbot."}
            return {"ok": False, "status": response.status_code, "error": error_message or "Error de la API del proveedor"}

        choices = data.get("choices", []) if isinstance(data, dict) else []
        first_choice = choices[0] if choices else {}
        message = first_choice.get("message", {}) if isinstance(first_choice, dict) else {}
        reply = str(message.get("content", "")).strip()
        if not reply:
            reply = "No recibi una respuesta util del asistente."

        return {"ok": True, "status": 200, "reply": reply, "model": CHATBOT_MODEL}
    except requests.Timeout:
        return {"ok": False, "status": 504, "error": "El proveedor tardo demasiado en responder."}
    except requests.RequestException:
        return {"ok": False, "status": 503, "error": "No fue posible conectarse con Groq desde el servidor del chatbot."}
    except ValueError:
        return {"ok": False, "status": 502, "error": "La respuesta del proveedor no tiene un formato valido."}
    except Exception:
        return {"ok": False, "status": 500, "error": "Error interno del servidor"}


def get_health():
    api_key = os.getenv("GROQ_API_KEY", "").strip()
    return {
        "status": "ok",
        "provider": "groq" if api_key else "missing_api_key",
        "model": CHATBOT_MODEL,
        "max_turns": CHATBOT_MAX_TURNS,
        "max_output_tokens": CHATBOT_MAX_OUTPUT_TOKENS,
        "project": "Cattleya VBG Atlantico",
    }
