import distutils.sysconfig as sysconfig
import os


def check_if_dict_in_list(lst):
    for i in lst:
        if isinstance(i, dict):
            return i
    return None


def std_modules():
    ret_list = []
    std_lib = sysconfig.get_python_lib(standard_lib=True)
    for top, dirs, files in os.walk(std_lib):
        for nm in files:
            if nm != "__init__.py" and nm[-3:] == ".py":
                ret_list.append(
                    os.path.join(top, nm)[len(std_lib) + 1 : -3].replace("\\", ".")
                )
    return ret_list
