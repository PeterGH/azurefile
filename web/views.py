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
        'account_url': account.url,
        'share_name': share.name,
        'directory_list': directories,
        'file_list': files
    }
    return render(request, 'web/share.html', context)

def file(request, account_name, share_name, file_path):
    account = azuresdk.get_account(account_name)
    share = account.get_share(share_name)
    parent_components, last_component = azuresdk.get_path_components(file_path)
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_name': share.name,
        'parent_components': parent_components,
        'last_component': last_component
    }
    return render(request, 'web/file.html', context)

def directory(request, account_name, share_name, directory_path):
    account = azuresdk.get_account(account_name)
    share = account.get_share(share_name)
    parent_components, last_component = azuresdk.get_path_components(directory_path)
    directory = share.get_directory(directory_path)
    directories, files = directory.get_directories_and_files()
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_name': share.name,
        'parent_components': parent_components,
        'last_component': last_component,
        'directory_dict': directories,
        'file_dict': files
    }
    return render(request, 'web/directory.html', context)

def mount(request):
    return render(request, 'web/mount.html')