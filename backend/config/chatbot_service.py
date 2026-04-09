import os
from pathlib import Path

import requests
from dotenv import load_dotenv

BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

SYSTEM_PROMPT = """
Eres el asistente de orientación del proyecto Cattleya sobre violencia basada en género (VBG) en Colombia.

Misión:
- Responder siempre en español con claridad, empatía y precisión.
- Escribir en español correcto, con tildes, eñes, signos de apertura y redacción gramatical natural.
- Orientar sobre rutas de ayuda, señales de riesgo y conceptos legales básicos.
- Si la persona pide evaluar su situación, haz preguntas de una en una y clasifica el riesgo al final.

Niveles de riesgo:
- Verde: bromas hirientes, chantaje, celos, humillación, intimidación, control leve.
- Amarillo: control de amistades, dinero o celular; empujones, cachetadas, aislamiento, sextorsión.
- Rojo: amenazas con armas u objetos, amenaza de muerte, abuso sexual, violación, mutilación, feminicidio.

Líneas de ayuda en Colombia:
- Línea 155: orientación a mujeres víctimas de VBG.
- Línea 123: emergencias.
- Línea 141: ICBF.
- 018000919748: Fiscalía General de la Nación.
- Secretaría de la Mujer Barranquilla: (605) 330-6999.
- Defensoría del Pueblo Atlántico: (605) 330-6000.

Reglas:
1. Si detectas riesgo inmediato o zona roja, empieza mencionando Línea 155 y 123.
2. No des diagnósticos médicos ni psicológicos.
3. Cuando expliques conceptos, menciona leyes relevantes como Ley 1257 de 2008 o Ley 1761 de 2015 si aplica.
4. Responde en máximo 4 frases cortas, salvo que la seguridad de la persona requiera más detalle.
5. No inventes datos.
""".strip()

SAFE_TEXT_NORMALIZATIONS = (
    (" linea ", " línea "),
    (" Linea ", " Línea "),
    ("linea 155", "línea 155"),
    ("linea 123", "línea 123"),
    ("linea 141", "línea 141"),
    ("genero", "género"),
    ("violacion", "violación"),
    ("mutilacion", "mutilación"),
    ("fiscalia", "fiscalía"),
    ("nacion", "nación"),
    ("orientacion", "orientación"),
    ("situacion", "situación"),
    ("senales", "señales"),
    ("psicologicos", "psicológicos"),
    ("medicos", "médicos"),
    ("diagnosticos", "diagnósticos"),
    ("basicos", "básicos"),
    ("maximo", "máximo"),
    ("mas detalle", "más detalle"),
    ("sesion", "sesión"),
    ("pagina", "página"),
    ("atencion", "atención"),
    ("empatia", "empatía"),
    ("precision", "precisión"),
    ("espanol", "español"),
    ("victimas", "víctimas"),
    ("secretaria", "secretaría"),
    ("defensoria", "defensoría"),
    ("Atlantico", "Atlántico"),
    ("Que ", "Qué "),
    ("Cual ", "Cuál "),
    ("Cuales ", "Cuáles "),
)


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


def normalize_reply_text(text):
    normalized = str(text or "").strip()
    if not normalized:
        return normalized

    padded = f" {normalized} "
    for source, target in SAFE_TEXT_NORMALIZATIONS:
      padded = padded.replace(source, target)

    return padded.strip()


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
            reply = "No recibí una respuesta útil del asistente."

        reply = normalize_reply_text(reply)

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
