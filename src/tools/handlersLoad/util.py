import sys


def insert_methods_path(methods_path):
    for path in methods_path:
        if path not in sys.path:
            sys.path.append(path)