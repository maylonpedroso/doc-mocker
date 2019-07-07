import importlib
import pkgutil

import doc_mocker.plugins


class PluginLoader:
    @staticmethod
    def iter_namespace(ns_pkg):
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    @classmethod
    def get_all(cls):
        return {
            name: importlib.import_module(name)
            for finder, name, ispkg in cls.iter_namespace(doc_mocker.plugins)
        }
