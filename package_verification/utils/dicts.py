def check_if_dict_in_list(lst):
    for i in lst:
        if isinstance(i, dict):
            return i
    return None


def format_dependencies(dependencies: list):
    dependencies_dict = {}
    for dependency in dependencies:
        if "=" in dependency:
            name, version = dependency.split("=")[:2]
            dependencies_dict[name] = version
        else:
            dependencies_dict[dependency] = ""
    return dependencies_dict
