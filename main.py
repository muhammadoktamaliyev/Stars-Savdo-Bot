import os
import telebot
from telebot import types
from flask import Flask
import threading

# Flask veb server (Render serveri uchun)
app = Flask(__name__)

# Bot sozlamalari
TOKEN = '8608266628:AAFWj6LjTVi6gFaAvEvzy7W6xLc4x8DfzC0'
bot = telebot.TeleBot(TOKEN)

# BotFather'dan olingan To'lov provayderi tokeni (Masalan, Click yoki Payme uchun)
# Agar hozircha yo'q bo'lsa, pastdagi to'lov tugmasi ishlashi uchun buni BotFather'dan olishingiz kerak
PROVIDER_TOKEN = 'YOUR_PROVIDER_TOKEN_HERE' 

@app.route('/')
def home():
    return "Bot ishlamoqda..."

# Stars mahsulotlari ro'yxati (Nomi, Narxi so'mda, va necha Stars berilishi)
STARS_PRODUCTS = {
    "stars_50":  {"title": "50 ⭐️ Stars", "price": 13000,  "amount": 50},
    "stars_100": {"title": "100 ⭐️ Stars", "price": 25000, "amount": 100},
    "stars_150": {"title": "150 ⭐️ Stars", "price": 35000, "amount": 150},
    "stars_250": {"title": "250 ⭐️ Stars", "price": 58000, "amount": 250},
    "stars_350": {"title": "350 ⭐️ Stars", "price": 80000, "amount": 350},
    "stars_500": {"title": "500 ⭐️ Stars", "price": 115000, "amount": 500},
    "stars_1000": {"title": "1000 ⭐️ Stars", "price": 220000, "amount": 1000}
}

# /start buyrug'i kelganda
@bot.message_handler(commands=['start'])
def start_message(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    
    btn_shop = types.KeyboardButton("🛒 Do'kon / Xarid qilish")
    btn_admin = types.KeyboardButton("👤 Admin bilan bog'lanish")
    btn_channel = types.KeyboardButton("📢 Bizning kanal")
    
    markup.add(btn_shop)
    markup.add(btn_admin, btn_channel)
    
    welcome_text = (
        "👋 Salom! Telegram Stars avtomatik botiga xush kelibsiz.\n\n"
        "Sotib olishni boshlash uchun **🛒 Do'kon / Xarid qilish** tugmasini bosing 👇"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup, parse_mode="Markdown")

# Matnli xabarlarni ushlash
@bot.message_handler(func=lambda message: True)
def handle_messages(message):
    if message.text == "🛒 Do'kon / Xarid qilish":
        # Kategoriyani inline tugma ko'rinishida chiqaramiz (Xuddi patrickshop robot kabi)
        markup = types.InlineKeyboardMarkup()
        btn_stars_cat = types.InlineKeyboardButton("⭐️ Telegram Stars sotib olish", callback_data="show_stars_prices")
        markup.add(btn_stars_cat)
        
        bot.send_message(
            message.chat.id, 
            "🛍 Kerakli mahsulot turini tanlang:\n\n*(Eslatma: Premium bo'limi mavjud emas)*", 
            reply_markup=markup, 
            parse_mode="Markdown"
        )
        
    elif message.text == "👤 Admin bilan bog'lanish":
        admin_text = "👨‍💻 Savollar va qo'llab-quvvatlash uchun adminga yozing:\n\n👉 @muhammad_16"
        bot.send_message(message.chat.id, admin_text)
        
    elif message.text == "📢 Bizning kanal":
        channel_text = "📢 Bizning rasmiy kanalimizga a'zo bo'ling:\n\n👉 https://t.me/tg_yulduz_savdo"
        bot.send_message(message.chat.id, channel_text)
        
    else:
        bot.reply_to(message, "Iltimos, pastdagi menyudan foydalaning. 👇")

# Inline tugmalar bosilganda ishlaydigan qism
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "show_stars_prices":
        # Stars miqdorlari tugmalarini chiqarish
        markup = types.InlineKeyboardMarkup(row_width=2)
        
        # Ro'yxatdan tugmalarni yasab olamiz
        buttons = []
        for key, product in STARS_PRODUCTS.items():
            btn = types.InlineKeyboardButton(f"{product['title']} — {product['price']:,} so'm", callback_data=f"buy_{key}")
            buttons.append(btn)
            
        markup.add(*buttons)
        # Orqaga qaytish tugmasi
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_categories"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⭐️ Kerakli miqdordagi Stars paketini tanlang:",
            reply_markup=markup
        )
        
    elif call.data == "back_to_categories":
        # Do'kon bosh sahifasiga qaytish
        markup = types.InlineKeyboardMarkup()
        btn_stars_cat = types.InlineKeyboardButton("⭐️ Telegram Stars sotib olish", callback_data="show_stars_prices")
        markup.add(btn_stars_cat)
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="🛍 Kerakli mahsulot turini tanlang:",
            reply_markup=markup
        )
        
    elif call.data.startswith("buy_"):
        product_key = call.data.split("_", 1)[1]
        product = STARS_PRODUCTS.get(product_key)
        
        if product:
            # Avtomatik hisob-faktura (Invoice) yuborish
            # Foydalanuvchi bu yerda to'g'ridan-to'g'ri plastik karta orqali to'lov qila oladi
            bot.send_invoice(
                chat_id=call.message.chat.id,
                title=product['title'],
                description=f"Telegram hisobingiz uchun {product['amount']} dona Stars sotib olish.",
                provider_token=PROVIDER_TOKEN,
                currency='UZS',
                prices=[types.LabeledPrice(label=product['title'], amount=product['price'] * 100)], # Tiyinlarda hisoblanadi
                start_parameter='stars-increment-payment',
                invoice_payload=f"payload_{product_key}"
            )
            # Tugma bosilganda bildirishnomani yopish
            bot.answer_callback_query(call.id, text="To'lov tizimi yuklanmoqda...")

# To'lovoldi tekshiruvi (Telegram talabi)
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True, error_message="To'lov jarayonida xatolik yuz berdi. Iltimos qayta urinib ko'ring.")

# To'lov muvaffaqiyatli yakunlanganda
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    payment_info = message.successful_payment
    bot.send_message(
        message.chat.id, 
        f"🎉 To'lov muvaffaqiyatli amalga oshirildi!\n\n"
        f"Siz {payment_info.total_amount / 100:,} so'm to'ladingiz. "
        f"Yaqin daqiqalar ichida Stars hisobingizga tushadi. Rahmat!"
    )
    # Adminni ogohlantirish (Kim qancha sotib olganini bilish uchun)
    admin_id = "YOUR_PERSONAL_TELEGRAM_ID_HERE" # O'zingizning Telegram ID raqamingizni yozing
    try:
        bot.send_message(admin_id, f"🔔 Yangi xarid!\nFoydalanuvchi: @{message.from_user.username}\nID: {message.from_user.id}\nTo'lov summasi: {payment_info.total_amount / 100:,} UZS")
    except Exception:
        pass

# Botni alohida oqimda ishga tushirish
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
