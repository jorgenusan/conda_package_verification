from pathlib import Path

from package_verification.core.env_file_management import EnvFileManagement
from package_verification.core.imports_finder import ImportsFinder
from package_verification.core.package_management import PackageManagement


def main():
    package_manager = PackageManagement()
    imports_finder = ImportsFinder()
    env_manager = EnvFileManagement()

    root_path = Path(".")
    imports = imports_finder.get_all_imports(root_path)

    conda_packages = []
    for package in imports:
        if package_manager.check_package(package):
            package_info = package_manager.get_package_info(
                package, "package_verification"
            )
            if package_info:
                conda_packages.append(package_info)

    env_manager.find_env_file(root_path)
    env_manager.update_txt_file(conda_packages)
    env_manager.update_yaml_file(conda_packages)


if __name__ == "__main__":
    main()
