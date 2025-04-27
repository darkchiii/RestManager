from .models import Business

def is_valid_business_code(business_code):
    if not business_code:
        return False
    try:
        if not Business.objects.filter(code=business_code).exists():
            return False
    except Exception as e:
        print(f"Błąd w trakcie sprawdzania kodu: {e}")
        return False
    return True