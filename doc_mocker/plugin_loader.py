import importlib
import logging
import pkgutil
from typing import Dict, Any, Generator, Tuple, Iterable

import doc_mocker.plugins


logger = logging.getLogger(__name__)


class PluginLoader:
    @staticmethod
    def iter_namespace(ns_pkg):
        return pkgutil.iter_modules(ns_pkg.__path__, ns_pkg.__name__ + ".")

    @staticmethod
    def validate_arguments(plugin: Any) -> None:
        assert hasattr(plugin, "arguments"), "CLI arguments required"
        assert type(plugin.arguments) is list, "Arguments must be a list"
        for arg in plugin.arguments:
            assert (
                type(arg) is tuple and len(arg) == 2
            ), "Each argument must be a 2 elements tuple (name, options)"
            assert (
                type(arg[0]) is tuple and len(arg[0]) == 1
            ), "Argument name must be a single element tuple"
            assert type(arg[1]) is dict, "Argument options must be a dict"

    @staticmethod
    def validate_class(plugin: Any) -> None:
        assert hasattr(plugin, "cls"), "Missing `cls` attribute"
        assert type(plugin.cls) is type, "`cls` attribute must be a type"

    @classmethod
    def clean(cls, plugins: Iterable[Tuple[str, Any]]) -> Generator[Tuple[str, Any], None, None]:
        for name, plugin in plugins:
            try:
                cls.validate_arguments(plugin)
                cls.validate_class(plugin)
            except AssertionError as e:
                logger.warning(f"Invalid plugin definition [{name}]: {e}")
            else:
                yield name, plugin

    @classmethod
    def get_all(cls) -> Dict[str, Any]:
        return dict(
            cls.clean(
                (name, importlib.import_module(name))
                for finder, name, ispkg in cls.iter_namespace(doc_mocker.plugins)
            )
        )
