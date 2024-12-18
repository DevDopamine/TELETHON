import os
import csv
from datetime import datetime

LOG_FOLDER = "Messages"
BASIC_MEDIA_FOLDER = rf'{LOG_FOLDER}\media'

async def save_message_to_csv(chat_id, where, status, sender_name, sender_first_name, telegram_id, message_id, text, date, media_path=None):
    if not os.path.exists(LOG_FOLDER):
        os.makedirs(LOG_FOLDER)
    
    file_name = f"messages.csv"
    file_path = os.path.join(LOG_FOLDER, file_name)

    is_new_file = not os.path.exists(file_path)

    message_data = [
        where,
        status,
        chat_id,
        sender_name,
        sender_first_name,
        telegram_id,
        message_id,
        text,
        date,
        media_path or ""
    ]

    with open(file_path, mode='a', newline='', encoding='utf-8') as csvfile:
        writer = csv.writer(csvfile)
        if is_new_file:
            writer.writerow([
                "Where",
                "Status",
                "Chat_ID",
                "User.name",
                "User.first_name",
                "User.id",
                "Message.id",
                "Text",
                "Date",
                "Media_path"
            ])
        writer.writerow(message_data)

    print(f"Сообщение сохранено в {file_path}: {message_data}")

async def process_message(event, status):
    sender = await event.get_sender()
    sender_username = getattr(sender, "username", None) or "Unknown"
    sender_first_name = getattr(sender, "first_name", "Unknown")

    chat_id = event.chat_id
    user_telegram_id = event.sender_id
    message_id = event.id
    text = (' ').join(event.text.split('\n')) if event.text else ""
    date = datetime.now().strftime('%d.%m.%y %H:%M')

    media_path = None
    if event.media:
        folder = rf'{BASIC_MEDIA_FOLDER}\ID Чата - [{event.chat_id}]\{status}'
        if not os.path.exists(folder):
            os.makedirs(folder)
        media_path = await event.download_media(file=folder)
        print(f"Медиафайл сохранен: {media_path}")

    await save_message_to_csv(
        chat_id,
        "Беседа" if not event.is_private else "Личные сообщения",
        status,
        sender_username,
        sender_first_name,
        user_telegram_id,
        message_id,
        text,
        date,
        media_path
    )