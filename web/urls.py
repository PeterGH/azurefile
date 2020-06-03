from django.urls import path
from . import views

app_name = 'web'

urlpatterns = [
    path('', views.index, name='index'),
    path('connect', views.connect, name='connect'),
    path('account/<account_name>', views.account, name='account'),
    path('account/<account_name>/share/<share_name>', views.share, name='share'),
    path('account/<account_name>/share/<share_name>/<path:item_name>', views.item, name='item'),
    path('mount/', views.mount, name='mount')
]