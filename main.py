import logging
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.exceptions import TelegramBadRequest
import edge_tts

# Bot tokeningiz va kanal ID
TOKEN = "7392885687:AAHxRPFn4gCVRiFIkFKNdX_tmJ_p1II7958"
CHANNEL_ID = "@dawawetr"  # Kanal usernameni yoki ID sini qo'ying
ADMINS = [5630386788]  # Adminlarning user_id ro‘yxati

bot = Bot(token=TOKEN)
dp = Dispatcher()

# Foydalanuvchilar tanlagan ovozlarni saqlash uchun lug‘at
user_voices = {}

# Kanalga obuna bo‘lganligini tekshirish
async def check_subscription(user_id: int) -> bool:
    try:
        user = await bot.get_chat_member(CHANNEL_ID, user_id)
        return user.status in ["member", "administrator", "creator"]  # Faqat obuna bo‘lganlar
    except TelegramBadRequest:
        return False

# Matnni ovozga aylantirish
async def text_to_speech(text, file_path, voice="en-US-GuyNeural"):
    tts = edge_tts.Communicate(text, voice)
    await tts.save(file_path)

# Start komandasi
@dp.message(Command("start"))
async def start_command(message: Message):
    user_id = message.from_user.id

    # Agar foydalanuvchi admin bo‘lsa, obuna bo‘lishi shart emas
    if user_id in ADMINS:
        await message.answer("👑 Siz admin ekansiz, botdan foydalanishingiz mumkin! Erkak yoki Ayol deb yozing")
        return

    # Oddiy foydalanuvchilar uchun tekshiruv
    is_subscribed = await check_subscription(user_id)

    if not is_subscribed:
        await message.answer(
            "❌ Siz avval kanalimizga obuna bo‘lishingiz kerak!\n"
            f"👉 <a href='https://t.me/{CHANNEL_ID[1:]}'><b>Kanalga obuna bo‘lish</b></a>",
            parse_mode="HTML",
            disable_web_page_preview=True
        )
        return  # Obuna bo‘lmagani uchun boshqa kod ishlamaydi

    await message.answer("✅ Siz kanalga obuna bo‘lgansiz! Botdan foydalanishingiz mumkin.\n\n"
                         "🔹 `Erkak` yoki `Ayol` deb yozib ovoz turini tanlang.")

# Ovoz turini tanlash
@dp.message(lambda message: message.text.lower() in ["erkak", "ayol"])
async def choose_voice(message: Message):
    user_id = message.from_user.id

    # 🇬🇧 Inglizcha erkak va ayol ovozlari
    voices = {
        "erkak": "en-US-GuyNeural",   # Erkak ovozi
        "ayol": "en-US-JennyNeural"   # Ayol ovozi
    }

    # Tanlangan ovozni saqlash
    user_voices[user_id] = voices[message.text.lower()]
    
    await message.answer(f"✅ Ovoz turi `{message.text.capitalize()}` ga o‘zgartirildi.\n\n"
                         "Endi matn yuboring, bot uni ovozga aylantiradi.", parse_mode="Markdown")

# Matnni ovozga aylantirish va ovozli xabar jo‘natish
@dp.message()
async def convert_text_to_voice(message: types.Message):
    user_id = message.from_user.id

    # Admin bo‘lsa, tekshiruvdan o‘tmaydi
    if user_id not in ADMINS:
        is_subscribed = await check_subscription(user_id)
        if not is_subscribed:
            await message.answer(
                "❌ Siz avval kanalimizga obuna bo‘lishingiz kerak!\n  Erkak yoki Ayol deb yozing"
                f"👉 <a href='https://t.me/{CHANNEL_ID[1:]}'><b>Kanalga obuna bo‘lish</b></a>",
                parse_mode="HTML",
                disable_web_page_preview=True
            )
            return

    text = message.text
    file_path = "output.mp3"

    # Agar foydalanuvchi ovoz tanlamagan bo‘lsa, default - erkak ovozi ishlatiladi
    voice = user_voices.get(user_id, "en-US-GuyNeural")

    # Matnni ovozga aylantirish
    await text_to_speech(text, file_path, voice)

    # ✅ TO‘G‘RI OCHISH USULI
    voice_file = types.FSInputFile(file_path)
    await message.answer_voice(voice_file)

# Botni ishga tushirish
async def main():
    logging.basicConfig(level=logging.INFO)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
