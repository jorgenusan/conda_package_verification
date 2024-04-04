import subprocess

import yaml


class CondaManagement:
    def __init__(self, env_name: str) -> None:
        self._env_name = env_name

    def get_package_info(self, package_name):
        try:
            output = subprocess.check_output(
                ["conda", "list", package_name, "-n", self._env_name],
                stderr=subprocess.STDOUT,
            )
            output = output.decode("utf-8")
            last_line = output.strip().split("\n")
            if len(last_line) < 4 or not last_line[3]:
                return None
            name, version = last_line[3].split()[:2]
            return {"name": name, "version": version}
        except subprocess.CalledProcessError:
            return None

    def export_pip_dependencies(self):
        try:
            output = subprocess.check_output(
                ["conda", "env", "export", "-n", self._env_name],
                stderr=subprocess.STDOUT,
            )
            if not output:
                return None
            output_str = output.decode("utf-8")
            output_dict = yaml.safe_load(output_str)
            return [
                item.split("=")[0] for item in output_dict["dependencies"][-1]["pip"]
            ]
        except subprocess.CalledProcessError:
            return None
        except KeyError:
            return None
