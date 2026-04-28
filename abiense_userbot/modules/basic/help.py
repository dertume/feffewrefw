from abiense_userbot.core.module import CommandContext, Module
from abiense_userbot.utils.emoji import pemoji


class HelpModule(Module):
    name = "help"
    description = "Список команд"

    def setup(self) -> None:
        @self.command("help", "Показать помощь")
        async def help_cmd(ctx: CommandContext) -> None:
            lines = [
                f"<b>{pemoji('settings', '⚙️')} Доступные команды:</b>",
                "",
            ]
            for cmd_name, spec in sorted(ctx.app.commands.items()):
                lines.append(f"<b><code>{ctx.app.prefix}{cmd_name}</code></b> — {spec.description}")

            await ctx.reply("\n".join(lines))


MODULE_CLASS = HelpModule
