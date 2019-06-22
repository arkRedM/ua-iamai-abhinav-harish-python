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

    email_enc, validity = is_valid_email(email)
    name_enc = idna.encode(name).decode('utf-8')
    password_enc = idna.encode(password).decode('utf-8')

    print(email_enc)

    if email_enc is not None and name is not None and password is not None:
        # validate everything
        user_instance = UserData.objects.create(
            email=email_enc,
            name=name_enc,
            password=password_enc
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
        title=idna.encode(title),
        text=str(idna.encode(text))
    )
    note_instance.save()

    return JsonResponse({
        'success': True,
        'message': 'OK'
    })


@require_http_methods(['GET'])
def email_list(request):
    email_list = []
    for user_ins in UserData.objects.all():
        temp_json = {
            'email': get_decoded_email(user_ins.email)
        }
        email_list.append(temp_json)

    return JsonResponse(email_list, safe=False)


def is_valid_email(email):
    if email:
        try:
            name_part = email.split('@')[0]
            domain_part = email.split('@')[1]
            domain_name = domain_part.split('.')[0]
            domain_tld = domain_part.split('.')[1]

            print('a', idna.encode(name_part).decode('utf-8') + '@' + idna.encode(domain_name).decode('utf-8') + '.' + idna.encode(domain_tld).decode('utf-8'))

            return idna.encode(name_part).decode('utf-8') + '@' + idna.encode(domain_name).decode('utf-8') + '.' + idna.encode(domain_tld).decode('utf-8'), True
        except:
            return None, False
    else:
        return None, False


def get_decoded_email(email_encoded):
    print(email_encoded)
    name_part = email_encoded.split('@')[0]
    domain_part = email_encoded.split('@')[1]
    domain_name = domain_part.split('.')[0]
    domain_tld = domain_part.split('.')[1]

    return idna.decode(name_part) + '@' + idna.decode(domain_name) + '.' + \
           idna.decode(domain_tld)

