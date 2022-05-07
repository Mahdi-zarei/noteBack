import datetime
import json
import random

from django.db import models


class User(models.Model):
    username = models.CharField(max_length=30)
    password = models.CharField(max_length=30)
    date_joined = models.DateTimeField(default=datetime.date.today())
    auth_token = models.CharField(max_length=100, default=-1)

    @staticmethod
    def exists(username):
        return User.objects.filter(username=username).count() == 1

    @staticmethod
    def can_create(username):
        return not (User.exists(username) and len(username) >= 5)

    @staticmethod
    def create(username, password):
        if User.can_create(username):
            tmp = User(username=username, password=password)
            tmp.save()

    @staticmethod
    def generate_token():
        import string
        token = ''.join(random.SystemRandom().choice(string.ascii_uppercase + string.digits) for _ in range(50))
        return token

    def check_pass(self, password):
        return self.password == password

    def check_token(self, token):
        return self.auth_token == token

    def login(self):
        tmp_token = User.generate_token()
        self.auth_token = tmp_token
        self.save()
        return tmp_token

    def logout(self):
        self.auth_token = -1

    def is_logged(self):
        return self.auth_token == -1

    def __str__(self):
        return self.username

class Note(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    subject = models.CharField(max_length=200)
    content = models.TextField(default="")
    unique_id = models.CharField(max_length=50, unique=True)
    date_created = models.DateTimeField(default=datetime.date.today)

    @staticmethod
    def exists(id):
        return Note.objects.filter(unique_id=id).count() == 1

    def make_edit(self, new_subject, new_content):
        self.subject = new_subject
        self.content = new_content

    def wrap(self):
        data = {"Subject": self.subject, "Content": self.content, "Id": self.unique_id, "Date": str(self.date_created)}
        wrapped = json.dumps(data)
        return wrapped

    def __str__(self):
        return self.subject
