from pathlib import Path

import yaml

from cpv.utils.dicts import check_if_dict_in_list


class EnvFileManagement:
    def __init__(self) -> None:
        self.possible_names = [
            "conda.yml",
            "conda.yaml",
            "environment.yml",
            "environment.yaml",
            "requirements.txt",
        ]
        self.txt_file = None
        self.yaml_file = None

    def find_env_file(self, directory: Path) -> None:
        for file in directory.rglob("*"):
            if file.name in self.possible_names:
                if file.name == "requirements.txt":
                    self.txt_file = file
                else:
                    self.yaml_file = file

    def get_txt_dependencies(self) -> dict:
        if not self.txt_file:
            return None
        dependencies = {}
        with open(self.txt_file, "r") as f:
            for line in f.readlines():
                line = line.strip()
                if "==" in line:
                    name, version = line.split("==")
                    dependencies[name] = version
        return dependencies

    def get_yaml_dependencies(self) -> dict:
        if not self.yaml_file:
            return None
        dependencies = {}
        with open(self.yaml_file, "r") as f:
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
        if not self.txt_file:
            return
        with open(self.txt_file, "r") as f:
            lines = f.readlines()

        for package in packages:
            package_to_add = package["name"] + "==" + package["version"] + "\n"
            if package_to_add not in lines:
                lines.append(package_to_add)

        with open(self.txt_file, "w") as f:
            f.writelines(lines)

    def update_yaml_file(self, conda_packages: list, pip_packages: list) -> None:
        if not self.yaml_file:
            return
        with open(self.yaml_file, "r") as f:
            data = yaml.safe_load(f)
            data_pip_packages = check_if_dict_in_list(data["dependencies"])

        for package in conda_packages:
            if package not in data["dependencies"]:
                package_to_add = package["name"] + "=" + package["version"]
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

        with open(self.yaml_file, "w") as f:
            yaml.safe_dump(data, f)