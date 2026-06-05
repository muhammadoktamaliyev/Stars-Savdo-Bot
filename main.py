Import os
import telebot
from telebot import types
from flask import Flask

# Flask veb server (Render serveri uchun)
app = Flask(__name__)

# BotFather bergan token muvaffaqiyatli joylashtirildi
TOKEN = '8608266628:AAFWj6LjTVi6gFaAvEvzy7W6xLc4x8DfzC0'
bot = telebot.TeleBot(TOKEN)

@app.route('/')
def home():
    return "Bot ishlamoqda..."

# /start buyrug'i kelganda chiroyli menyu chiqarish
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    # Tugmalarni yaratamiz
    btn_prices = types.KeyboardButton("⭐️ STARS narxlari")
    btn_admin = types.KeyboardButton("👤 Admin bilan bog'lanish")
    btn_channel = types.KeyboardButton("📢 Bizning kanal")
    
    # Tugmalarni joylashtiramiz
    markup.add(btn_prices)
    markup.add(btn_admin, btn_channel)
    
    welcome_text = (
        "👋 Salom! Telegram Stars botiga xush kelibsiz.\n\n"
        "Kerakli bo'limni tanlash uchun pastdagi tugmalardan foydalaning 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

# Tugmalar bosilganda qaytariladigan javoblar
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "⭐️ STARS narxlari":
        prices_text = (
            "⭐️ **STARS MATNLI NARXLARI** ⭐️\n\n"
            "🔹 50 ⭐️ — 13.000 so’m\n"
            "🔹 100 ⭐️ — 25.000 so’m\n"
            "🔹 150 ⭐️ — 35.000 so’m\n"
            "🔹 250 ⭐️ — 58.000 so’m\n"
            "🔹 350 ⭐️ — 80.000 so'm\n"
            "🔹 500 ⭐️ — 115.000 so’m\n"
            "🔹 1000 ⭐️ — 220.000 so'm\n\n"
            "💳 Xarid qilish uchun Adminga murojaat qiling!"
        )
        bot.send_message(message.chat.id, prices_text, parse_mode="Markdown")
        
    elif message.text == "👤 Admin bilan bog'lanish":
        admin_text = "👨‍💻 Savollar va Stars sotib olish uchun adminga yozing:\n\n👉 @muhammad_16"
        bot.send_message(message.chat.id, admin_text)
        
    elif message.text == "📢 Bizning kanal":
        channel_text = "📢 Bizning rasmiy kanalimizga a'zo bo'ling, yangiliklar va aksiyalar shu yerda berib boriladi:\n\n👉 https://t.me/tg_yulduz_savdo"
        bot.send_message(message.chat.id, channel_text)
        
    else:
        bot.reply_to(message, "Iltimos, pastdagi tugmalardan birini tanlang. 👇")

# Botni alohida oqimda ishga tushirish
import threading
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
