import json


def parse_gemini_response(text: str):
    try:
        data = json.loads(text)

        return {
            "action": data.get("action", "chat"),
            "reply": data.get("reply", ""),
            "booking": data.get("booking"),
            "phone": data.get("phone"),
        }

    except Exception:
        return {
            "action": "chat",
            "reply": text,
            "booking": None,
            "phone": None,
        }