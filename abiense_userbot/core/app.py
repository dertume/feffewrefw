from __future__ import annotations

import logging
import shlex
import time

from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, Message

from abiense_userbot.config import settings
from abiense_userbot.core.loader import load_modules
from abiense_userbot.core.module import BotApp, CommandContext
from abiense_userbot.db.storage import JsonStorage
from abiense_userbot.utils.emoji import pemoji

logging.basicConfig(
    level=getattr(logging, settings.log_level.upper(), logging.INFO),
    format="[%(asctime)s] %(levelname)s | %(name)s | %(message)s",
)
logger = logging.getLogger("abiense.userbot")


def _build_client() -> Client:
    return Client(
        name="abiense_userbot",
        api_id=settings.api_id,
        api_hash=settings.api_hash,
        session_string=settings.session_string,
        in_memory=True,
    )


def _parse_command(prefix: str, text: str) -> tuple[str, list[str], str] | None:
    if not text or not text.startswith(prefix):
        return None

    payload = text[len(prefix) :].strip()
    if not payload:
        return None

    parts = shlex.split(payload)
    cmd = parts[0].lower()
    args = parts[1:]
    raw_args = payload[len(parts[0]) :].strip()
    return cmd, args, raw_args


async def run() -> None:
    started_at = int(time.time())
    client = _build_client()
    app = BotApp(client=client, prefix=settings.cmd_prefix, owner_id=settings.owner_id, storage=JsonStorage())
    load_modules(app, settings.enabled_modules)
    logger.info("Loaded %s modules and %s commands", len(app.modules), len(app.commands))

    @client.on_message(filters.me & filters.text)
    async def userbot_router(_: Client, message: Message) -> None:
        parsed = _parse_command(app.prefix, message.text or "")
        if not parsed:
            return

        cmd_name, args, raw_args = parsed
        command = app.commands.get(cmd_name)
        if not command:
            await message.reply_text(
                f"<b>{pemoji('cross', '❌')} Неизвестная команда: <code>{cmd_name}</code></b>"
            )
            return

        ctx = CommandContext(app=app, message=message, args=args, raw_args=raw_args)
        await command.handler(ctx)

    @client.on_message(filters.private & ~filters.me)
    async def afk_auto_reply(_: Client, message: Message) -> None:
        afk = app.storage.get("afk")
        if not afk:
            return

        reason = afk.get("reason") or "Без причины"
        await message.reply_text(
            f"<b>{pemoji('time', '⏰')} Я сейчас AFK.</b>\n"
            f"<b>{pemoji('file', '📁')} Причина:</b> <code>{reason}</code>"
        )

    @client.on_message(filters.command("start") & filters.me)
    async def start_overlay(_: Client, message: Message) -> None:
        kb = InlineKeyboardMarkup(
            inline_keyboard=[
                [
                    InlineKeyboardButton(
                        text="Статус",
                        callback_data="noop_status",
                        icon_custom_emoji_id="5870921681735781843",
                    ),
                    InlineKeyboardButton(
                        text="Модули",
                        callback_data="noop_modules",
                        icon_custom_emoji_id="5870528606328852614",
                    ),
                ]
            ]
        )
        uptime = int(time.time()) - started_at
        await message.reply_text(
            f"<b>{pemoji('gift', '🎁')} Abiense Userbot активен.</b>\n"
            f"<b>{pemoji('stats', '📊')} Uptime:</b> <code>{uptime}s</code>",
            reply_markup=kb,
        )

    await client.start()
    me = await client.get_me()
    logger.info("Authorized as @%s (%s)", me.username, me.id)
    await client.idle()
