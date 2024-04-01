import subprocess

class PackageManagement:
    def check_package(self, package_name):
        try:
            output = subprocess.run(['conda', 'search', package_name], capture_output=True)
            if'No match' in output.stdout.decode():
                return False
            return True
        except subprocess.CalledProcessError:
            return False
    
    def get_package_info(self, package_name, env_name=None):
        try:
            output = subprocess.check_output(['conda', 'list', package_name, '-n', env_name], stderr=subprocess.STDOUT)
            output = output.decode('utf-8')
            last_line = output.strip().split('\n')
            if len(last_line) < 4 or not last_line[3]:
                return False
            name, version = last_line[3].split()[:2]
            return {'name': name, 'version': version}
        except subprocess.CalledProcessError:
            return False
