from pathlib import Path

from pydepcheck.core.conda_management import CondaManagement
from pydepcheck.core.env_file_management import EnvFileManagement
from pydepcheck.core.imports_finder import ImportsFinder
from pydepcheck.utils.utils import file_hash, std_modules


class CLI:
    def __init__(self, env_file: str, env_name: str) -> None:
        self._env_file = Path(env_file)
        self._root_path = Path(".")
        self._conda_manager = CondaManagement(env_name)
        self._imports_finder = ImportsFinder()
        self._env_manager = EnvFileManagement()

    def run(self) -> None:
        """Run the CLI to update the environment file with the external dependencies."""
        initial_hash = file_hash(self._env_file)

        imports = self._imports_finder.get_all_imports(self._root_path)
        external_imports = [
            lib
            for lib in imports
            if lib not in std_modules() and not lib.startswith("_")
        ]
        env_file_extension = self._env_file.suffix

        if env_file_extension == ".txt":
            self._env_manager.txt_file = self._env_file
            self._update_txt_file(external_imports)
        else:
            self._env_manager.yaml_file = self._env_file
            self._update_yaml_file(external_imports)

        final_hash = file_hash(self._env_file)
        if initial_hash != final_hash:
            print("Environment file updated successfully \u2713")
            raise SystemExit(1)
        else:
            print("Environment file is up to date \u2713")

    def _update_txt_file(self, imports: list) -> None:
        """Update the txt file with the external dependencies.

        Args:
            imports (list): List of external dependencies.
        """
        dependencies_to_add = []
        txt_dependencies = self._env_manager.get_txt_dependencies()

        for package in imports:
            if package not in txt_dependencies:
                package_info = self._conda_manager.get_package_info(package)
                if package_info:
                    dependencies_to_add.append(package_info)

        self._env_manager.update_txt_file(dependencies_to_add)

    def _update_yaml_file(self, imports: list) -> None:
        """Update the yaml file with the external dependencies.

        Args:
            imports (list): List of external dependencies.
        """
        dependencies_to_add_yaml = []

        pip_dependencies = self._conda_manager.export_pip_dependencies()
        if pip_dependencies:
            pip_info = self._conda_manager.get_package_info("pip")
            dependencies_to_add_yaml.append(pip_info)

        pip_packages = []
        for imp in imports:
            package_info = self._conda_manager.get_package_info(imp)
            if imp not in pip_dependencies:
                if package_info:
                    dependencies_to_add_yaml.append(package_info)
            else:
                pip_packages.append(package_info)

        self._env_manager.update_yaml_file(dependencies_to_add_yaml, pip_packages)
