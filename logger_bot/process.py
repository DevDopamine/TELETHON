import os
from telethon import TelegramClient, events

from logger_bot.chat_manage import (
    load_allowed_groups,
    add_allowed_group,
    remove_allowed_group
)
from logger_bot.saving import process_message


api_id = os.getenv('API_ID')
api_hash = os.getenv('API_HASH')

client = TelegramClient('message_logger', api_id, api_hash)


@client.on(events.NewMessage(incoming=True))
async def handle_incoming_message(event):
    allowed_groups = load_allowed_groups()
    if not event.is_private:
        if event.chat_id in allowed_groups:
            await process_message(event, "Входящее")
    else:
        await process_message(event, "Входящее")

@client.on(events.NewMessage(outgoing=True))
async def handle_outcomming_message(event):
    allowed_groups = load_allowed_groups()
    if not event.is_private:
        if event.chat_id in allowed_groups:
            if event.text == '.выкл':

                await event.edit("❌ Беседа отключена!")
                remove_allowed_group(event.chat_id)
            
            await process_message(event, "Отправленное")

        elif event.text == '.вкл':
            add_allowed_group(event.chat_id)
            await event.delete()
            await event.respond("✅ Беседа подключена!")

    else:
        await process_message(event, "Отправленное")


async def main():
    print("Начато прослушивание сообщений. Нажмите Ctrl+C для выхода.")
    await client.run_until_disconnected()
