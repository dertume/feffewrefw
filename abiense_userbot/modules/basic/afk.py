import time

from abiense_userbot.core.module import CommandContext, Module
from abiense_userbot.utils.emoji import pemoji


class AfkModule(Module):
    name = "afk"
    description = "AFK режим"

    def setup(self) -> None:
        @self.command("afk", "Включить AFK")
        async def afk_on(ctx: CommandContext) -> None:
            reason = ctx.raw_args or "Без причины"
            payload = {"reason": reason, "since": int(time.time())}
            ctx.app.storage.set("afk", payload)
            await ctx.reply(
                f"<b>{pemoji('lock', '🔒')} AFK включен.</b>\n"
                f"<b>{pemoji('file', '📁')} Причина:</b> <code>{reason}</code>"
            )

        @self.command("unafk", "Выключить AFK")
        async def afk_off(ctx: CommandContext) -> None:
            afk = ctx.app.storage.get("afk")
            if not afk:
                await ctx.reply(f"<b>{pemoji('cross', '❌')} AFK и так отключен.</b>")
                return

            since = int(afk.get("since", int(time.time())))
            spent = int(time.time()) - since
            ctx.app.storage.delete("afk")
            await ctx.reply(
                f"<b>{pemoji('check', '✅')} AFK отключен.</b>\n"
                f"<b>{pemoji('time', '⏰')} Был AFK:</b> <code>{spent}s</code>"
            )


MODULE_CLASS = AfkModule
