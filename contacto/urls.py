from django.urls import path
from .views import contactenos

urlpatterns = [
    path('contactenos/', contactenos, name='contactenos'),
]