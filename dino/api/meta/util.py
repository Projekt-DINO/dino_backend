from os.path import isfile, isdir


def is_file(path: str):
    return isfile(path)


def is_dir(path: str):
    return isdir(path)


def upperfirst(string: str):
    return string[0].upper() + string[1:]


def isempty(string: str):
    return string is None or string == "" or len(string) == 0


def list_type_of(l: list, t):
    for obj in l:
        if not isinstance(obj, t):
            return False
    return True
