import time

from abiense_userbot.core.module import CommandContext, Module
from abiense_userbot.utils.emoji import pemoji


class PingModule(Module):
    name = "ping"
    description = "Проверка задержки"

    def setup(self) -> None:
        @self.command("ping", "Проверить пинг")
        async def ping(ctx: CommandContext) -> None:
            started = time.perf_counter()
            msg = await ctx.reply(f"<b>{pemoji('loading', '🔄')} Измеряю задержку...</b>")
            latency = (time.perf_counter() - started) * 1000
            await msg.edit_text(
                f"<b>{pemoji('check', '✅')} Pong:</b> <code>{latency:.2f} ms</code>"
            )


MODULE_CLASS = PingModule
