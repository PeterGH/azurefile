from django.shortcuts import redirect, render
from django.http import HttpResponse
from django import forms
from . import azuresdk

class UploadFileForm(forms.Form):
    file_name = forms.CharField(label='File Name', max_length=255)
    file = forms.FileField()

def index_view(request):
    account_names = azuresdk.get_account_names()
    context = {
        'account_names': account_names
    }
    return render(request, 'web/index.html', context)

def connect_view(request):
    if request.method == 'GET':
        return render(request, 'web/connect.html')
    elif request.method == 'POST':
        azuresdk.get_account(name=request.POST['accountName'], key=request.POST['accountKey'])
        return index_view(request)

def account_view(request, account_name):
    if request.method == 'GET' and request.GET.get('action') == 'create_share':
        context = {
            'account_name': account_name
        }
        return render(request, 'web/create_share.html', context)
    account = azuresdk.get_account(account_name)
    if request.method == 'POST' and request.GET.get('action') == 'create_share':
        try:
            account.create_share(name=request.POST['shareName'])
        except BaseException as error:
            context = {
                'error': error
            }
            return render(request, 'web/error.html', context)
    shares = account.get_share_names()
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_list': shares
    }
    return render(request, 'web/account.html', context)

def share_view(request, account_name, share_name):
    if request.method == 'GET' and request.GET.get('action') == 'create_directory':
        context = {
            'account_name': account_name,
            'share_name': share_name
        }
        return render(request, 'web/create_directory.html', context)
    if request.method == 'GET' and request.GET.get('action') == 'upload_file':
        context = {
            'account_name': account_name,
            'share_name': share_name,
            'form': UploadFileForm()
        }
        return render(request, 'web/upload_file.html', context)
    account = azuresdk.get_account(account_name)
    if request.method == 'GET' and request.GET.get('action') == 'delete':
        try:
            account.delete_share(name=share_name)
            return account_view(request, account_name)
        except BaseException as error:
            context = {
                'error': error
            }
            return render(request, 'web/error.html', context)
    share = account.get_share(share_name)
    if request.method == 'POST' and request.GET.get('action') == 'create_directory':
        try:
            share.create_directory(name=request.POST['directoryName'])
        except BaseException as error:
            context = {
                'error': error
            }
            return render(request, 'web/error.html', context)
    if request.method == 'POST' and request.GET.get('action') == 'upload_file':
        print(request.POST)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            share.upload_file(form.cleaned_data['file_name'], request.FILES['file'])
        else:
            context = {
                'error': 'Invalid file upload'
            }
            return render(request, 'web/error.html', context)
    directories, files = share.get_directories_and_files()
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_name': share.name,
        'directory_list': directories,
        'file_list': files
    }
    return render(request, 'web/share.html', context)

def file_view(request, account_name, share_name, file_path):
    account = azuresdk.get_account(account_name)
    share = account.get_share(share_name)
    parent_components, last_component = azuresdk.get_path_components(file_path)
    file = share.get_file(file_path)
    try:
        file_content = file.get_content_as_text()
    except BaseException as error:
        context = {
            'error': error
        }
        return render(request, 'web/error.html', context)
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_name': share.name,
        'parent_components': parent_components,
        'last_component': last_component,
        'file_content': file_content
    }
    return render(request, 'web/file.html', context)

def directory_view(request, account_name, share_name, directory_path):
    if request.method == 'GET' and request.GET.get('action') == 'create_directory':
        context = {
            'account_name': account_name,
            'share_name': share_name,
            'directory_path': directory_path
        }
        return render(request, 'web/create_directory.html', context)
    if request.method == 'GET' and request.GET.get('action') == 'upload_file':
        context = {
            'account_name': account_name,
            'share_name': share_name,
            'directory_path': directory_path,
            'form': UploadFileForm()
        }
        return render(request, 'web/upload_file.html', context)
    account = azuresdk.get_account(account_name)
    share = account.get_share(share_name)
    directory = share.get_directory(directory_path)
    if request.method == 'GET' and request.GET.get('action') == 'delete':
        try:
            directory.delete_directory()
            directory_path = azuresdk.get_path_parent(directory_path)
            if directory_path == '':
                # Cannot remove ?action=delete from request by
                # calling request.GET.pop('action') because request.GET is immutable
                # so cannot call share_view directly
                return redirect('web:share', account_name=account_name, share_name=share_name)
            else:
                directory = share.get_directory(directory_path)
        except BaseException as error:
            context = {
                'error': error
            }
            return render(request, 'web/error.html', context)
    if request.method == 'POST' and request.GET.get('action') == 'create_directory':
        try:
            directory.create_directory(name=request.POST['directoryName'])
        except BaseException as error:
            context = {
                'error': error
            }
            return render(request, 'web/error.html', context)
    if request.method == 'POST' and request.GET.get('action') == 'upload_file':
        print(request.POST)
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            directory.upload_file(form.cleaned_data['file_name'], request.FILES['file'])
        else:
            context = {
                'error': 'Invalid file upload'
            }
            return render(request, 'web/error.html', context)
    parent_components, last_component = azuresdk.get_path_components(directory_path)
    directories, files = directory.get_directories_and_files()
    context = {
        'account_name': account.name,
        'account_url': account.url,
        'share_name': share.name,
        'directory_path': directory.directory_path,
        'parent_components': parent_components,
        'last_component': last_component,
        'directory_dict': directories,
        'file_dict': files
    }
    return render(request, 'web/directory.html', context)

def mount_view(request):
    return render(request, 'web/mount.html')