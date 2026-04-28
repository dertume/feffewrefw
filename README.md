# Abiense Userbot

**Abiense Userbot** — масштабный, модульный и расширяемый Telegram-юзербот на базе **Pyrogram**.

## Возможности

- Гибкая модульная архитектура (hot-load модулей).
- Базовые модули из коробки: `help`, `ping`, `alive`, `afk`, `notes`, `system`.
- SDK для написания собственных модулей за 2–3 функции.
- Единый стиль premium-emoji интерфейса через `<tg-emoji emoji-id="...">`.
- Командный парсер с префиксом (`.` по умолчанию).

## Быстрый старт

```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .
cp .env.example .env
```

Заполните `.env` и запустите:

```bash
python -m abiense_userbot.main
```

## Структура

- `abiense_userbot/main.py` — точка входа.
- `abiense_userbot/core/app.py` — запуск клиента и регистрация модулей.
- `abiense_userbot/core/loader.py` — автозагрузка модулей.
- `abiense_userbot/core/module.py` — базовый класс модуля + контекст.
- `abiense_userbot/db/storage.py` — встроенное key-value хранилище (JSON).
- `abiense_userbot/modules/basic/*.py` — встроенные команды.
- `abiense_userbot/utils/emoji.py` — централизованные premium emoji id.

## Как написать свой модуль

Создайте файл `abiense_userbot/modules/custom/my_module.py`:

```python
from abiense_userbot.core.module import Module

class MyModule(Module):
    name = "my"
    description = "Мой модуль"

    def setup(self) -> None:
        @self.command("hello", "Приветствие")
        async def hello(ctx):
            await ctx.reply(
                '<b><tg-emoji emoji-id="5870764288364252592">🙂</tg-emoji> Привет от custom-модуля!</b>'
            )
```

После этого добавьте `abiense_userbot.modules.custom.my_module` в `ENABLED_MODULES` (см. `config.py`).

## Заметки по UX

- В инлайн-кнопках используйте `icon_custom_emoji_id`.
- В HTML-сообщениях используйте `<tg-emoji emoji-id="...">`.
- Не смешивайте обычные emoji в тексте кнопок — только premium id.
