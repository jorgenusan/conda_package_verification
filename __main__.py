from pathlib import Path

from package_verification.core.env_file_management import EnvFileManagement
from package_verification.core.imports_finder import ImportsFinder
from package_verification.core.conda_management import CondaManagement
from package_verification.utils.dicts import format_dependencies


def main():
    conda_manager = CondaManagement()
    imports_finder = ImportsFinder()
    env_manager = EnvFileManagement()

    root_path = Path(".")
    imports = imports_finder.get_all_imports(root_path)

    # Get conda dependencies
    conda_packages = []
    pip_packages = {"pip": []}
    conda_dependencies = conda_manager.export_env_dependencies("conda_package_verification")
    conda_dependencies = format_dependencies(conda_dependencies)
    pip_dependencies = conda_manager.export_pip_dependencies("conda_package_verification")
    pip_dependencies = format_dependencies(pip_dependencies)
    
    # Get file dependencies
    dependencies_to_add = []
    dependencies_to_add_yaml = []
    
    env_manager.find_env_file(root_path)
    txt_dependencies = env_manager.get_txt_dependencies()
    yaml_dependencies = env_manager.get_yaml_dependencies()
    
    # Check if dependencies are in the txt file
    for package in imports:
        if package not in txt_dependencies:
            package_info = conda_manager.get_package_info(package, "conda_package_verification")
            if package_info:
                dependencies_to_add.append(package_info)
            
    # Check if dependencies are in the yaml file
    for dependency in conda_dependencies.keys():
        if dependency not in yaml_dependencies and dependency in imports:
            package_info = conda_manager.get_package_info(dependency, "conda_package_verification")
            if package_info:
                dependencies_to_add_yaml.append(package_info)
    
    for dependency in pip_dependencies.keys():
        if dependency not in yaml_dependencies and dependency in imports:
            package_info = conda_manager.get_package_info(dependency, "conda_package_verification")
            if package_info:
                dependencies_to_add_yaml.append(package_info)

    # Update files
    env_manager.update_txt_file(dependencies_to_add)
    env_manager.update_yaml_file(dependencies_to_add_yaml)


if __name__ == "__main__":
    main()
