from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('connect', views.connect, name='connect'),
    path('account/<account_name>', views.get_account, name='account'),
    path('account/<account_name>/create_share', views.create_share, name='create_share'),
    path('account/<account_name>/share/<share_name>', views.get_share, name='share'),
    path('account/<account_name>/share/<share_name>/file/<path:file_path>', views.get_file, name='file'),
    path('account/<account_name>/share/<share_name>/directory/<path:directory_path>', views.get_directory, name='directory'),
    path('mount/', views.mount, name='mount')
]