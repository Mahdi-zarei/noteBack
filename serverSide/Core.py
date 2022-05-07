import json

from serverSide.models import User, Note
import uuid

def prep_response(answer="", status="200"):
    raw = {"Response": answer, "Status": status}
    jsoned = json.dumps(raw)
    return jsoned

def parse_request(request):
    return eval(str(request.body)[2:-1])

def login_user(username, password):
    if not User.exists(username):
        return 404
    user = User.objects.get(username=username)
    if not user.check_pass(password):
        return 403
    token = user.login()
    return token

def logout_user(username, token):
    if not auth_user(username, token):
        return 403
    user = User.objects.get(username=username)
    user.logout()
    return "200"

def auth_user(username, token):
    if not User.exists(username):
        return False
    user = User.objects.get(username=username)
    if not user.check_token(token):
        return False
    return True

def register_user(username, password):
    if User.exists(username):
        print(User.objects.get(username=username))
        return 403
    user = User(username=username, password=password)
    user.save()
    return "200"

def generate_id():
    return str(uuid.uuid4())

def add_note(username, token, data):
    if not auth_user(username, token):
        return 403
    user = User.objects.get(username=username)
    id = generate_id()
    note = Note(subject=data['Subject'], content=data['Content'], user=user, unique_id=id)
    note.save()
    return note.wrap()

def edit_note(username, token, data):
    if not auth_user(username, token) or not Note.exists(data['Id']):
        return 403
    note = Note.objects.get(unique_id=data['Id'])
    note.make_edit(data['Subject'], data['Content'])
    note.save()
    return note.wrap()

def delete_note(username, token, id):
    if not auth_user(username, token) or not Note.exists(id):
        return 403
    note = Note.objects.get(unique_id=id)
    note.delete()
    return id

def get_notes(username, token):
    if not auth_user(username, token):
        return 403
    note_list = []
    user = User.objects.get(username=username)
    notes = Note.objects.filter(user=user)
    for x in notes:
        note_list.append(x.wrap())
    return note_list

