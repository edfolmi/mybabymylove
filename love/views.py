import uuid
import requests
import logging

from django.conf import settings
from django.shortcuts import render
from django.http import JsonResponse
from django.views.decorators.http import require_POST

from .utils import get_access_token


logger = logging.getLogger("django")

# Create your views here.
def page(request):
    return render(request, 'love/page.html')


def page1(request):
    return render(request, 'love/page1.html')


def page2(request):
    return render(request, 'love/page2.html')


def page3(request):
    return render(request, 'love/page3.html')


def page4(request):
    return render(request, 'love/page4.html')


def intro(request):
    return render(request, 'love/intro.html')


API_BASE_URL = settings.FLUTTERWAVE_API_BASE_URL_SECRET

@require_POST
def send_gift(request):
    try:
        account_number = request.POST.get('account_number')
        if not account_number:
            return JsonResponse({'status': 'info', 'message': 'Enter your account number joor! 😏'}, status=400)

        # Bank code
        bank_code = "305"

        # Headers
        flutterwave_secret_key = get_access_token()
        headers = {
            "Authorization": f"Bearer {flutterwave_secret_key}",
            "Content-Type": "application/json",
            "X-Trace-Id": str(uuid.uuid4()),
            "X-Idempotency-Key": str(uuid.uuid4())
        }

        # Prepare body
        payload = {
            "action": "instant",
            "payment_instruction": {
                "source_currency": "NGN",
                "amount": {
                    "applies_to": "destination_currency",
                    "value": 100  # ₦50,000 — adjust as needed
                },
                "recipient": {
                    "bank": {
                        "account_number": account_number,
                        "code": bank_code
                    }
                },
                "destination_currency": "NGN"
            },
            "type": "bank",
            "reference": str(uuid.uuid4())
        }

        # Send request to Flutterwave
        response = requests.post(
            f'{API_BASE_URL}/direct-transfers',
            headers=headers,
            json=payload,
            timeout=10
        )
        
        logger.info(f"Response: {response.status_code}, {response.text}")

        # Handle API response
        if response.status_code == 200 or response.status_code == 201:
            data = response.json()
            if data.get("status") == "success":
                return JsonResponse({
                    'status': 200,
                    'message': 'Gift sent successfully! 🎁',
                    'data': data.get("data")
                })
            else:
                return JsonResponse({
                    'status': False,
                    'message': f"Flutterwave error: {data.get('message', 'Unknown error')}, Remarks: {response.text}"
                }, status=400)
        else:
            return JsonResponse({
                'status': False,
                'message': f"Transfer failed with HTTP {response.status_code}, Remarks: {response.text}"
            }, status=response.status_code)

    except Exception as e:
        return JsonResponse({'status': False, 'message': f"Error: {str(e)}"}, status=500)
