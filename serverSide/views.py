from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt

from . import Core as Core

@csrf_exempt
def register(request):
    data = Core.parse_request(request)
    answer = Core.register_user(data['Username'], data['Password'])
    status = "ERROR" if answer == 403 else "Success"
    resp = Core.prep_response(answer, status)
    return HttpResponse(resp)

@csrf_exempt
def login(request):
    data = Core.parse_request(request)
    answer = Core.login_user(data['Username'], data['Password'])
    status = "ERROR" if answer == 404 or answer == 403 else "Success"
    resp = Core.prep_response(answer, status)
    return HttpResponse(resp)

@csrf_exempt
def logout(request):
    data = Core.parse_request(request)
    answer = Core.logout_user(data['Username'], data['Token'])
    status = "ERROR" if answer == 403 else "Success"
    resp = Core.prep_response(status=status)
    return HttpResponse(resp)

@csrf_exempt
def create_note(request):
    data = Core.parse_request(request)
    answer = Core.add_note(data['Username'], data['Token'], data)
    status = "ERROR" if answer == 403 else "Success"
    resp = Core.prep_response(answer, status)
    return HttpResponse(resp)

@csrf_exempt
def edit_note(request):
    data = Core.parse_request(request)
    answer = Core.edit_note(data['Username'], data['Token'], data)
    status = "ERROR" if answer == 403 else "Success"
    resp = Core.prep_response(answer, status)
    return HttpResponse(resp)

@csrf_exempt
def delete_note(request):
    data = Core.parse_request(request)
    answer = Core.delete_note(data["Username"], data["Token"], data["Id"])
    status = "ERROR" if answer == 403 else "Success"
    resp = Core.prep_response(answer, status)
    return HttpResponse(resp)

@csrf_exempt
def get_all_notes(request):
    data = Core.parse_request(request)
    answer = Core.get_notes(data['Username'], data['Token'])
    status = "ERROR" if answer == 403 else "Success"
    resp = Core.prep_response(answer, status)
    return HttpResponse(resp)


