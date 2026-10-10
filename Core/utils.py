import requests
from django.conf import settings

def verify_hcaptcha(request):
    hcaptcha_response = request.POST.get('h-captcha-response')

    if not hcaptcha_response:
        return False

    payload = {
        'secret': settings.HCAPTCHA_SECRET,
        'response': hcaptcha_response,
        'remoteip': request.META.get('REMOTE_ADDR'),
    }

    try:
        response = requests.post(
            "https://hcaptcha.com/siteverify",
            data=payload,
            timeout=5
        )
        result = response.json()
        return result.get('success', False)
    except Exception:
        return False
    