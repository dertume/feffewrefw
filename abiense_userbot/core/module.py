from __future__ import annotations

from collections.abc import Awaitable, Callable
from dataclasses import dataclass
from typing import Any

from pyrogram import Client
from pyrogram.types import Message


@dataclass(slots=True)
class CommandSpec:
    name: str
    description: str
    handler: Callable[["CommandContext"], Awaitable[None]]


@dataclass(slots=True)
class CommandContext:
    app: "BotApp"
    message: Message
    args: list[str]
    raw_args: str

    async def reply(self, text: str) -> Message:
        return await self.message.reply_text(text, quote=True)


class Module:
    name = "module"
    description = "base module"

    def __init__(self, app: "BotApp") -> None:
        self.app = app
        self.commands: list[CommandSpec] = []

    def setup(self) -> None:
        """Override in subclasses to register commands and handlers."""

    def command(self, name: str, description: str) -> Callable[[Callable], Callable]:
        def decorator(func: Callable[[CommandContext], Awaitable[None]]) -> Callable:
            self.commands.append(CommandSpec(name=name, description=description, handler=func))
            return func

        return decorator


class BotApp:
    def __init__(self, client: Client, prefix: str, owner_id: int, storage: Any) -> None:
        self.client = client
        self.prefix = prefix
        self.owner_id = owner_id
        self.storage = storage
        self.modules: dict[str, Module] = {}
        self.commands: dict[str, CommandSpec] = {}

    def register_module(self, module: Module) -> None:
        module.setup()
        self.modules[module.name] = module
        for cmd in module.commands:
            self.commands[cmd.name] = cmd
