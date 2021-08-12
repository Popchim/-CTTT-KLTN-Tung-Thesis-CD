import os, gc
from Http import HttpClient
import network
import uasyncio
from Credential import PASSWORD
class MITM(BaseException):
    pass
class OTAUpdater:
    def __init__(self, github_repo, github_src_dir='', module='', main_dir='main', new_version_dir='next', secrets_file=None, headers={}):
        self.http_client = HttpClient(headers=headers)
        self.github_repo = github_repo.rstrip('/').replace('https://github.com/', '')
        self.github_src_dir = '' if len(github_src_dir) < 1 else github_src_dir.rstrip('/') + '/'
        self.module = module.rstrip('/')
        self.main_dir = main_dir
        self.new_version_dir = new_version_dir
        self.secrets_file = secrets_file
    def __del__(self):
        self.http_client = None
    def check_update(self) -> bool:
	print('Checking for a new version...')
        try:
            (current_version, latest_version) = self._check_for_new_version()
            if latest_version > current_version:
                print('New version available')
                self._create_new_version_file(latest_version)
                return True
            else:
                print('Current version is the latest')
                return False
	except MITM:
            print('MITM attack!!!')
            return False
        except:
            print('Failed to check for a new version')
            return False
    def install_update(self) -> bool:
        print('Checking for a new update')
        if self.new_version_dir in os.listdir(self.module):
            if '.version' in os.listdir(self.modulepath(self.new_version_dir)):
                latest_version = self.get_version(self.modulepath(self.new_version_dir), '.version')
                print('New update found, updating to version {}...'.format(latest_version))
                try:
                    self._download_new_version(latest_version)
                    self._copy_secrets_file()
                    self._delete_old_version()
                    self._install_new_version()
                    print('Finished installing the new version, reset for the update to take effect')
                    return True
                except MITM:
                    print('MITM attack!!!')
                    return False
                except:
                    print('Failed to install the new version, will retry on next reboot', latest_version)
                    return False
        else:
            print('No new updates found...')
            return False
    def check_and_install_update(self) -> bool:
        print('Check for a new version and update')
        return self.check_update() and self.install_update()
    def _check_for_new_version(self):
        latest_version = self.get_latest_version()
        current_version = self.get_version(self.modulepath(self.main_dir))
        print('\tCurrent version: ', current_version)
        print('\tLatest version: ', latest_version)
        return (current_version, latest_version)
    def _create_new_version_file(self, latest_version):
        try:
            self.mkdir(self.modulepath(self.new_version_dir))
        except:
            pass
        with open(self.modulepath(self.new_version_dir + '/.version'), 'w') as versionfile:
            versionfile.write(latest_version)
            versionfile.close()
    def get_version(self, directory, version_file_name='.version'):
        if version_file_name in os.listdir(directory):
            with open(directory + '/' + version_file_name) as f:
                version = f.read()
                return version
        return '0.0'
    async def _get_latest_version(self):
        return self.http_client.get('https://api.github.com/repos/{}/releases/latest'.format(self.github_repo))
    async def _get_latest_version_wrapper(self):
        return await uasyncio.wait_for(self._get_latest_version(), 10)
    def get_latest_version(self):
        gc.collect()
        latest_release = uasyncio.run(self._get_latest_version_wrapper())
        gc.collect()
        latest_json = latest_release.json()
        latest_release.close()
        gc.collect()
        try:
            if latest_json['assets'][0]['name'] != PASSWORD:
                raise MITM
        except:
            raise MITM
        version = latest_json['tag_name']
        return version
    def _download_new_version(self, version):
        print('Downloading version {}'.format(version))
        self._download_all_files(version)
        print('Version {} downloaded to {}'.format(version, self.modulepath(self.new_version_dir)))
    def _download_all_files(self, version, sub_dir=''):
        gc.collect() 
        url = 'https://api.github.com/repos/{}/contents{}{}{}?ref=refs/tags/{}'.format(self.github_repo, self.github_src_dir, self.main_dir, sub_dir, version)
        gc.collect() 
        file_list = self.http_client.get(url)
        file_list_json = file_list.json()
        file_list.close()
        gc.collect() 
        try:
            if file_list_json.pop(0)['name'] != PASSWORD:
                raise MITM
        except:
            raise MITM
        for file in file_list_json:
            path = self.modulepath(self.new_version_dir + '/' + file['path'].replace(self.main_dir + '/', '').replace(self.github_src_dir, ''))
            if file['type'] == 'file':
                gitPath = file['path']
                print('\tDownloading: ', gitPath, 'to', path)
                self._download_file(version, gitPath, path)
            elif file['type'] == 'dir':
                print('Creating dir', path)
                self.mkdir(path)
                self._download_all_files(version, sub_dir + '/' + file['name'])
            gc.collect()
    async def download_file(self, version, gitPath):
        return self.http_client.get('https://raw.githubusercontent.com/{}/{}/{}'.format(self.github_repo, version, gitPath)).text
    async def download_file_wrapper(self, version, gitPath):
        return await uasyncio.wait_for(self.download_file(version, gitPath), 10)
    def _download_file(self, version, gitPath, path):
        file_content = uasyncio.run(self.download_file_wrapper(version, gitPath))
        if file_content[1:9] != PASSWORD:
            raise MITM
        with open(path, 'w') as f:
            f.write(file_content)
            f.close()
    def _copy_secrets_file(self):
        if self.secrets_file:
            fromPath = self.modulepath(self.main_dir + '/' + self.secrets_file)
            toPath = self.modulepath(self.new_version_dir + '/' + self.secrets_file)
            print('Copying secrets file from {} to {}'.format(fromPath, toPath))
            self._copy_file(fromPath, toPath)
            print('Copied secrets file from {} to {}'.format(fromPath, toPath))
    def _delete_old_version(self):
        print('Deleting old version at {} ...'.format(self.modulepath(self.main_dir)))
        self._rmtree(self.modulepath(self.main_dir))
        print('Deleted old version at {} ...'.format(self.modulepath(self.main_dir)))
    def _install_new_version(self):
        print('Installing new version at {} ...'.format(self.modulepath(self.main_dir)))
        if self._os_supports_rename():
            os.rename(self.modulepath(self.new_version_dir), self.modulepath(self.main_dir))
        else:
            self._copy_directory(self.modulepath(self.new_version_dir), self.modulepath(self.main_dir))
            self._rmtree(self.modulepath(self.new_version_dir))
        print('Update installed, please reboot now')
    def _rmtree(self, directory):
        for entry in os.ilistdir(directory):
            is_dir = entry[1] == 0x4000
            if is_dir:
                self._rmtree(directory + '/' + entry[0])
            else:
                os.remove(directory + '/' + entry[0])
        os.rmdir(directory)
    def _os_supports_rename(self) -> bool:
        self._mk_dirs('otaUpdater/osRenameTest')
        os.rename('otaUpdater', 'otaUpdated')
        result = len(os.listdir('otaUpdated')) > 0
        self._rmtree('otaUpdated')
        return result
    def _copy_directory(self, fromPath, toPath):
        if not self._exists_dir(toPath):
            self._mk_dirs(toPath)
        for entry in os.ilistdir(fromPath):
            is_dir = entry[1] == 0x4000
            if is_dir:
                self._copy_directory(fromPath + '/' + entry[0], toPath + '/' + entry[0])
            else:
                self._copy_file(fromPath + '/' + entry[0], toPath + '/' + entry[0])
    def _copy_file(self, fromPath, toPath):
        with open(fromPath) as fromFile:
            with open(toPath, 'w') as toFile:
                CHUNK_SIZE = 512 # bytes
                data = fromFile.read(CHUNK_SIZE)
                while data:
                    toFile.write(data)
                    data = fromFile.read(CHUNK_SIZE)
            toFile.close()
        fromFile.close()
    def _exists_dir(self, path) -> bool:
        try:
            os.listdir(path)
            return True
        except:
            return False
    def _mk_dirs(self, path:str):
        paths = path.split('/')

        pathToCreate = ''
        for x in paths:
            self.mkdir(pathToCreate + x)
            pathToCreate = pathToCreate + x + '/'
    def mkdir(self, path:str):
        try:
            os.mkdir(path)
        except OSError as exc:
            if exc.args[0] == 17: 
                pass
    def modulepath(self, path):
        return self.module + '/' + path if self.module else path
