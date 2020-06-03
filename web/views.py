from django.shortcuts import render
from django.http import HttpResponse
from . import azuresdk

def index(request):
    account_names = azuresdk.get_account_names()
    context = {
        'account_names': account_names
    }
    return render(request, 'web/index.html', context)

def connect(request):
    if request.method == 'GET':
        return render(request, 'web/connect.html')
    elif request.method == 'POST':
        azuresdk.get_account(name=request.POST['accountName'], key=request.POST['accountKey'])
        return index(request)

def account(request, account_name):
    account = azuresdk.get_account(account_name)
    shares = account.get_share_names()
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_list': shares
    }
    return render(request, 'web/account.html', context)

def share(request, account_name, share_name):
    account = azuresdk.get_account(account_name)
    share = account.get_share(share_name)
    directories, files = share.get_directories_and_files()
    context = {
        'account_name': account.name,
        'share_name': share.name,
        'share_url': share.url,
        'directory_list': directories,
        'file_list': files
    }
    return render(request, 'web/share.html', context)

def item(request, account_name, share_name, item_name):
    context = {
        'account_name': account_name,
        'share_name': share_name,
        'item_name': item_name
    }
    return render(request, 'web/item.html', context)

def mount(request):
    return render(request, 'web/mount.html')