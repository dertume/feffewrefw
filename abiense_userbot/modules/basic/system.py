import os

from abiense_userbot.core.module import CommandContext, Module
from abiense_userbot.utils.emoji import pemoji


class SystemModule(Module):
    name = "system"
    description = "Системные утилиты"

    def setup(self) -> None:
        @self.command("prefix", "Показать или сменить префикс")
        async def prefix(ctx: CommandContext) -> None:
            if not ctx.args:
                await ctx.reply(
                    f"<b>{pemoji('settings', '⚙️')} Текущий префикс:</b> <code>{ctx.app.prefix}</code>"
                )
                return

            new_prefix = ctx.args[0]
            if len(new_prefix) > 3:
                await ctx.reply(f"<b>{pemoji('cross', '❌')} Префикс слишком длинный.</b>")
                return
            ctx.app.prefix = new_prefix
            await ctx.reply(
                f"<b>{pemoji('check', '✅')} Новый префикс:</b> <code>{new_prefix}</code>"
            )

        @self.command("about", "Инфо о проекте")
        async def about(ctx: CommandContext) -> None:
            await ctx.reply(
                f"<b>{pemoji('gift', '🎁')} Abiense Userbot</b>\n"
                f"<b>{pemoji('code', '</>')} Архитектура:</b> <code>Modular + SDK</code>\n"
                f"<b>{pemoji('file', '📁')} CWD:</b> <code>{os.getcwd()}</code>"
            )


MODULE_CLASS = SystemModule
