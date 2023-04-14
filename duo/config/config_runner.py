from duo.config import runners

from inspect import getmembers, isfunction
import importlib
import pkgutil


class ConfigRunner:
    @staticmethod
    def run():
        package = importlib.import_module(runners.__name__)
        results = {}
        for loader, name, is_pkg in pkgutil.walk_packages(package.__path__):
            full_name = package.__name__ + '.' + name
            results[full_name] = importlib.import_module(full_name)

        for name, obj in results.items():
            getattr(obj, 'execute')()
        return results
