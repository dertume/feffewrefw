from __future__ import annotations

from importlib import import_module
from types import ModuleType

from abiense_userbot.core.module import BotApp, Module


def _resolve_module_class(mod: ModuleType) -> type[Module]:
    if hasattr(mod, "MODULE_CLASS"):
        return getattr(mod, "MODULE_CLASS")

    for value in vars(mod).values():
        if isinstance(value, type) and issubclass(value, Module) and value is not Module:
            return value

    raise RuntimeError(f"Cannot find Module subclass in {mod.__name__}")


def load_modules(app: BotApp, paths: list[str]) -> None:
    for path in paths:
        imported = import_module(path)
        module_cls = _resolve_module_class(imported)
        instance = module_cls(app)
        app.register_module(instance)
