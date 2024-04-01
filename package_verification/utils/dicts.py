def check_if_dict_in_list(lst):
    return any(isinstance(i, dict) for i in lst)
