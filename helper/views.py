import re

import idna
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper.models import UserData, NotesData

EMAIL_REGEX = '^[a-z0-9-]+(\.[_a-z0-9-]+)*@[a-z0-9-]+(\.[a-z0-9-]+)*(\.[a-z]{2,4})$'


@csrf_exempt
@require_http_methods(['POST'])
def signup(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    password = request.POST.get('password')

    if email is not None and name is not None and password is not None:
        # validate everything
        user_instance = UserData.objects.create(
            email=str(idna.encode(email)),
            name=str(idna.encode(name)),
            password=str(idna.encode(password))
        )
        user_instance.save()

        return JsonResponse({
            'success': True,
            'message': 'OK'
        })
    else:
        return JsonResponse({
            'success': False,
            'message': 'Data not valid'
        })


@csrf_exempt
@require_http_methods(['POST'])
def take_notes(request):
    title = request.POST.get('title')
    text = request.POST.get('text')

    # validate everything
    note_instance = NotesData.objects.create(
        title=str(idna.encode(title)),
        text=str(idna.encode(text))
    )
    note_instance.save()

    return JsonResponse({
        'success': True,
        'message': 'OK'
    })


def is_valid_email(email):
    if email:
        match = re.match(EMAIL_REGEX, email)
        if match is None:
            return False
    else:
        return False



