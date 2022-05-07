from django.urls import path, include
from . import views

urlpatterns = [
    path('Register/', views.register),
    path('Login/', views.login),
    path('AddNote/', views.create_note),
    path('EditNote/', views.edit_note),
    path('GetNotes/', views.get_all_notes),
    path('DeleteNote/', views.delete_note),
    path('Logout/', views.logout),
]