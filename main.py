from telethon import TelegramClient, events
from telethon.errors.rpcerrorlist import FloodWaitError
import asyncio
import re

# Telegram API bilgileri
api_id = '16200120'  # Telegram API ID
api_hash = '6611d0556f6f8dc7b9190803cc442dec'  # Telegram API Hash

# Kullanacağınız hesapların telefon numaraları ve session isimleri
accounts = [
    ('+447907325741 ', 'session_1'),
    ('+447801101779 ', 'session_2'),
    ('+447599168979 ', 'session_4'),
    ('+447729389626 ', 'session_5'),
    ('+447752559964 ', 'session_6'),
    ('+447742588629 ', 'session_7'),
    ('+447745161785 ', 'session_8'),
    ('+447517007674 ', 'session_9'),
    ('+447908575748 ', 'session_10'),
    ('+447985132321 ', 'session_11'),
    ('+447932346011 ', 'session_12'),
    ('+447930877620 ', 'session_13'),
    ('+447538366715 ', 'session_14'),
    ('+447961593801 ', 'session_15'),
    ('+447957613256 ', 'session_16'),
    ('+447961267689  ', 'session_17'),
    ('+447939686582 ', 'session_18'),
    ('+447563091691 ', 'session_19'),
    ('+447926762107 ', 'session_20'),
    ('+447517007599 ', 'session_21'),
    ('+447856096750  ', 'session_22'),
    ('+447469301950 ', 'session_23'),
    ('+447599154331 ', 'session_24'),
    ('+447599168809 ', 'session_25'),
    ('+447939684911  ', 'session_26'),
    ('+447957201395 ', 'session_27'),
    ('+447922452749 ', 'session_29'),
    ('+447585751430 ', 'session_30'),
    ('+447887221886 ', 'session_31'),
    ('+447563091688 ', 'session_32'),
    ('+447752558786 ', 'session_33'),
    ('+447887221885 ', 'session_34'),
    ('+447903319837 ', 'session_35'),
    ('+447301453676 ', 'session_36'),
    ('+447301383630 ', 'session_37'),
    ('+447879090554  ', 'session_38'),
    ('+447393306945 ', 'session_39'),
    ('+447555132839 ', 'session_40'),
    ('+447901829995 ', 'session_41'),
    ('+447887221883 ', 'session_42'),
    ('+447887221898 ', 'session_43'),
    ('+46760749893 ', 'session_44'),
    ('+353873812868 ', 'session_45'),
    ('+353873339293 ', 'session_46'),
    ('+14134498993 ', 'session_47'),
    ('+16812713836 ', 'session_48'),
    ('+14642272953 ', 'session_49'),
]

# Kaynak grup ve hedef grup chat id'leri
source_group = 'https://t.me/BetFury'  # Mesajların çekileceği grup
target_group = 'https://t.me/rouletteacademycanada'  # Mesajların gönderileceği grup

# Yasaklı kelimeler listesi
banned_keywords = ['betfury']

# Telegram istemcilerini başlatmak için async fonksiyonu
async def start_clients():
    clients = []

    for phone_number, session_name in accounts:
        client = TelegramClient(session_name, api_id, api_hash)
        await client.start(phone_number)
        clients.append(client)

    return clients

# URL, admin mesajları, bot mesajları ve yasaklı kelimeler içeren mesajları filtreleyen fonksiyon
def is_valid_message(message):
    # URL içeren mesajları filtrele
    url_pattern = r'(https?://\S+|www\.\S+)'
    if re.search(url_pattern, message.text):
        return False

    # Bot veya admin mesajlarını filtrele
    if message.sender.bot or message.is_channel:  # Admin veya bot mesajlarını filtreler
        return False

    # Yasaklı kelimeler içeren mesajları filtrele
    for keyword in banned_keywords:
        if keyword.lower() in message.text.lower():
            return False

    return True

# Kaynak gruptan gelen mesajları hedef gruba gönderme fonksiyonu
async def forward_messages(clients):
    client_index = 0  # Hesap döngüsü için başlangıç indeksi

    source_client = clients[client_index]

    @source_client.on(events.NewMessage(chats=source_group))
    async def handler(event):
        nonlocal client_index
        message = event.message

        # Geçerli mesajları (gif, sticker ve yanıtlı mesajlar dahil) filtrele
        if is_valid_message(message):
            try:
                # Mesaj yanıtlanmışsa, yanıtlanan mesajın içeriğini çek
                if message.is_reply:
                    # Yanıtlanan mesajı getir
                    replied_message = await message.get_reply_message()
                    # Yanıtlayarak mesajı hedef gruba gönder
                    await clients[client_index].send_message(target_group, message.text, reply_to=replied_message.id)
                else:
                    # Yanıtlanmamışsa direkt olarak hedef gruba gönder
                    await clients[client_index].send_message(target_group, message.text)
            except FloodWaitError as e:
                print(f"Flood hatası: {e.seconds} saniye bekleniyor.")
                await asyncio.sleep(e.seconds)  # Hata mesajında belirtilen süre kadar bekle
            finally:
                # Hesabı değiştir ve sıradaki hesaba geç
                client_index = (client_index + 1) % len(clients)

        print(f"{source_group} grubundan mesajlar çekilmeye başlandı...")

    await source_client.run_until_disconnected()

# Ana fonksiyon
async def main():
    clients = await start_clients()
    await forward_messages(clients)

# Botu başlat
if __name__ == '__main__':
    asyncio.run(main())
