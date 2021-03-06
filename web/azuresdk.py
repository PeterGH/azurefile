from azure.storage.fileshare import ShareServiceClient

class AzureStorageAccount:
    def __init__(self, name, key):
        self.name = name
        self.key = key
        self.url = 'https://' + self.name + '.file.core.windows.net'
        self._client = ShareServiceClient(account_url=self.url, credential=self.key)

    def get_share_names(self):
        return [share.name for share in self._client.list_shares()]

    def get_share(self, name):
        share = self._client.get_share_client(name)
        return AzureStorageShare(account=self, name=name, client=share)
    
    def create_share(self, name):
        self._client.create_share(share_name=name)

    def delete_share(self, name):
        self._client.delete_share(share_name=name)

class AzureStorageShare:
    def __init__(self, account, name, client):
        self.account = account
        self.name = name
        self.url = self.account.url + '/' + self.name
        self._client = client

    def get_directories_and_files(self):
        directories = []
        files = []
        for item in self._client.list_directories_and_files():
            if item['is_directory']:
                directories.append(item['name'])
            else:
                files.append(item['name'])
        return directories, files

    def get_directory(self, name):
        directory = self._client.get_directory_client(name)
        return AzureStorageDirectory(share=self, name=name, client=directory)

    def create_directory(self, name):
        self._client.create_directory(directory_name=name)

    def get_file(self, name):
        file = self._client.get_file_client(name)
        return AzureStorageFile(share=self, name=name, client=file)

    def upload_file(self, name, data):
        file = self._client.get_file_client(name)
        file.upload_file(data)

    def mount(self):
        import os
        error_code = os.system('mkdir /mnt/' + self.name)
        if error_code != 0:
            # divide by 256.
            # system returns an error code in the same format as returned by os.wait()
            error_code //= 256
            raise OSError(error_code)

class AzureStorageDirectory:
    def __init__(self, share, name, client):
        self.share = share
        self.name = name
        self.url = self.share.url + '/' + self.name
        self._client = client
        self.directory_path = self._client.directory_path

    def get_directories_and_files(self):
        directories = {}
        files = {}
        for item in self._client.list_directories_and_files():
            if item['is_directory']:
                directories[item['name']] = self._client.directory_path + '/' + item['name']
            else:
                files[item['name']] = self._client.directory_path + '/' + item['name']
        return directories, files

    def create_directory(self, name):
        self._client.create_subdirectory(directory_name=name)

    def delete_directory(self):
        self._client.delete_directory()

    def upload_file(self, name, data):
        file = self._client.get_file_client(name)
        file.upload_file(data)

class AzureStorageFile:
    def __init__(self, share, name, client):
        self.share = share
        self.name = name
        self.url = self.share.url + '/' + self.name
        self._client = client
        self.file_path = self._client.file_path

    def get_content_as_text(self):
        stream = self._client.download_file()
        return stream.content_as_text()

    def get_chunks(self):
        stream = self._client.download_file()
        return stream.chunks()

    def delete_file(self):
        self._client.delete_file()


storageAccountCache = {}

def get_account(name, key=''):
    if name not in storageAccountCache:
        storageAccountCache[name] = AzureStorageAccount(name=name, key=key)
    return storageAccountCache[name]

def get_account_names():
    return list(storageAccountCache)

def get_path_components(path):
    components = path.split('/')
    last_component = { path: components[-1] }
    parent_components = {}
    p = ''
    for component in components[:-1]:
        if not p:
            p = component
        else:
            p = p + '/' + component
        parent_components[p] = component
    return parent_components, last_component

def get_path_parent(path):
    i = path.rfind('/')
    if i == -1:
        return ''
    else:
        return path[:i]

def get_path_last_component(path):
    i = path.rfind('/')
    if i == -1:
        return path
    else:
        return path[i + 1:]

