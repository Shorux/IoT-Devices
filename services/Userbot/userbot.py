from telethon import TelegramClient, events


api_id =
api_hash = ''
source_chat = -1002617742941     # ID исходной группы
target_chat = -1002560974644     # ID группы/канала-получателя

client = TelegramClient('userbot_session', api_id, api_hash)


@client.on(events.NewMessage(chats=source_chat))
async def handler(event):
    try:
        await client.send_message(target_chat, event.message)
    except Exception as e:
        print(f'Ошибка при отправке: {e}')


with client:
    client.run_until_disconnected()