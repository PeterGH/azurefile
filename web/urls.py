from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index_view, name='index'),
    path('connect', views.connect_view, name='connect'),
    path('account/<account_name>', views.account_view, name='account'),
    path('account/<account_name>/share/<share_name>', views.share_view, name='share'),
    path('account/<account_name>/share/<share_name>/file/<path:file_path>', views.file_view, name='file'),
    path('account/<account_name>/share/<share_name>/directory/<path:directory_path>', views.directory_view, name='directory'),
    path('mount/', views.mount_view, name='mount')
]