def fast_intent(text: str):
    t = text.lower()
    if "เวลา" in t or "time" in t:
        return "intent:get_time"
    if "นัด" in t or "appointment" in t:
        return "intent:get_appointments"
    return None
