import yaml

from pydepcheck.utils.utils import check_if_dict_in_list


class EnvFileManagement:
    def __init__(self) -> None:
        self._txt_file = None
        self._yaml_file = None

    @property
    def txt_file(self):
        return self._txt_file

    @txt_file.setter
    def txt_file(self, value):
        self._txt_file = value

    @property
    def yaml_file(self):
        return self._yaml_file

    @yaml_file.setter
    def yaml_file(self, value):
        self._yaml_file = value

    def get_txt_dependencies(self) -> dict:
        """Get the dependencies from the txt file.

        Returns:
            dict: Dependencies from the txt file.
        """
        if not self._txt_file:
            return None
        dependencies = {}
        with open(self._txt_file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if "==" in line:
                    name, version = line.split("==")
                    dependencies[name] = version
        return dependencies

    def get_yaml_dependencies(self) -> dict:
        """Get the dependencies from the yaml file.

        Returns:
            dict: Dependencies from the yaml file.
        """
        if not self._yaml_file:
            return None
        dependencies = {}
        with open(self._yaml_file, "r") as f:
            data = yaml.safe_load(f)
            dict_in_list = check_if_dict_in_list(data["dependencies"])
            for dependency in data["dependencies"]:
                if "=" in dependency:
                    name, version = dependency.split("=")[:2]
                    dependencies[name] = version
            if dict_in_list:
                for pip_dependency in dict_in_list["pip"]:
                    name, version = pip_dependency.split("==")
                    dependencies[name] = version
        return dependencies

    def update_txt_file(self, packages: list) -> None:
        """Update the txt file with the external dependencies.

        Args:
            packages (list): List of external dependencies.
        """
        if not self._txt_file:
            return
        with open(self._txt_file, "r") as f:
            lines = f.readlines()

        if lines and not lines[-1].endswith("\n"):
            lines.append("\n")

        for package in packages:
            package_to_add = package["name"] + "==" + package["version"] + "\n"
            if package_to_add not in lines:
                lines.append(package_to_add)

        with open(self._txt_file, "w") as f:
            f.writelines(lines)

    def update_yaml_file(self, conda_packages: list, pip_packages: list) -> None:
        """Update the yaml file with the external dependencies.

        Args:
            conda_packages (list): Conda packages to add.
            pip_packages (list): Pip packages to add.
        """
        if not self._yaml_file:
            return
        with open(self._yaml_file, "r") as f:
            data = yaml.safe_load(f)
            data_pip_packages = check_if_dict_in_list(data["dependencies"])

        for package in conda_packages:
            package_to_add = package["name"] + "=" + package["version"]
            if package_to_add not in data["dependencies"]:
                if not data_pip_packages:
                    data["dependencies"].append(package_to_add)
                else:
                    data["dependencies"].insert(-1, package_to_add)

        if pip_packages:
            if not data_pip_packages:
                data["dependencies"].append(
                    {
                        "pip": [
                            pip_package["name"] + "==" + pip_package["version"]
                            for pip_package in pip_packages
                        ]
                    }
                )
            else:
                for pip_package in pip_packages:
                    package_to_add = pip_package["name"] + "==" + pip_package["version"]
                    if package_to_add not in data_pip_packages["pip"]:
                        data_pip_packages["pip"].append(package_to_add)

        with open(self._yaml_file, "w") as f:
            yaml.safe_dump(data, f)
