from django.urls import path
from . import views

app_name = 'smb'

urlpatterns = [
    path('<share_name>', views.share_view, name='share')
]