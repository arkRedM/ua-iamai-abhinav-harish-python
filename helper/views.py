from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from helper.models import UserData, NotesData


@csrf_exempt
@require_http_methods(['POST'])
def signup(request):
    email = request.POST.get('email')
    name = request.POST.get('name')

    password = request.POST.get('password')

    if email is not None and name is not None and password is not None:
        # validate everything
        user_instance = UserData.objects.create(
            email=email,
            name=name,
            password=password
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
        title=title,
        text=text
    )
    note_instance.save()

    return JsonResponse({
        'success': True,
        'message': 'OK'
    })





