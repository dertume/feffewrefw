from abiense_userbot.core.module import CommandContext, Module
from abiense_userbot.utils.emoji import pemoji


class NotesModule(Module):
    name = "notes"
    description = "Локальные заметки"

    def setup(self) -> None:
        @self.command("save", "Сохранить заметку: .save key текст")
        async def save_note(ctx: CommandContext) -> None:
            if len(ctx.args) < 2:
                await ctx.reply(
                    f"<b>{pemoji('cross', '❌')} Использование:</b> <code>.save key текст</code>"
                )
                return

            key = ctx.args[0].strip().lower()
            value = ctx.raw_args[len(key) :].strip()
            notes = ctx.app.storage.get("notes", {})
            notes[key] = value
            ctx.app.storage.set("notes", notes)
            await ctx.reply(
                f"<b>{pemoji('check', '✅')} Заметка сохранена:</b> <code>{key}</code>"
            )

        @self.command("get", "Получить заметку: .get key")
        async def get_note(ctx: CommandContext) -> None:
            if not ctx.args:
                await ctx.reply(f"<b>{pemoji('cross', '❌')} Укажите ключ.</b>")
                return

            key = ctx.args[0].strip().lower()
            notes = ctx.app.storage.get("notes", {})
            value = notes.get(key)
            if not value:
                await ctx.reply(f"<b>{pemoji('cross', '❌')} Заметка не найдена.</b>")
                return

            await ctx.reply(
                f"<b>{pemoji('file', '📁')} {key}</b>\n"
                f"<code>{value}</code>"
            )

        @self.command("delnote", "Удалить заметку: .delnote key")
        async def delete_note(ctx: CommandContext) -> None:
            if not ctx.args:
                await ctx.reply(f"<b>{pemoji('cross', '❌')} Укажите ключ.</b>")
                return

            key = ctx.args[0].strip().lower()
            notes = ctx.app.storage.get("notes", {})
            if key not in notes:
                await ctx.reply(f"<b>{pemoji('cross', '❌')} Нет такой заметки.</b>")
                return

            del notes[key]
            ctx.app.storage.set("notes", notes)
            await ctx.reply(f"<b>{pemoji('check', '✅')} Удалено:</b> <code>{key}</code>")


MODULE_CLASS = NotesModule
