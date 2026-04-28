import platform
import time

from abiense_userbot.core.module import CommandContext, Module
from abiense_userbot.utils.emoji import pemoji


class AliveModule(Module):
    name = "alive"
    description = "Системная сводка"

    def setup(self) -> None:
        @self.command("alive", "Показать статус")
        async def alive(ctx: CommandContext) -> None:
            launched_at = ctx.app.storage.get("launched_at")
            if launched_at is None:
                launched_at = int(time.time())
                ctx.app.storage.set("launched_at", launched_at)
            uptime = int(time.time()) - int(launched_at)

            await ctx.reply(
                f"<b>{pemoji('home', '🏘')} Abiense Userbot Online</b>\n"
                f"<b>{pemoji('stats', '📊')} Модулей:</b> <code>{len(ctx.app.modules)}</code>\n"
                f"<b>{pemoji('code', '</>')} Команд:</b> <code>{len(ctx.app.commands)}</code>\n"
                f"<b>{pemoji('time', '⏰')} Uptime:</b> <code>{uptime}s</code>\n"
                f"<b>{pemoji('settings', '⚙️')} Python:</b> <code>{platform.python_version()}</code>"
            )


MODULE_CLASS = AliveModule
