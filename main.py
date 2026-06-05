import os
import telebot
from telebot import types
from flask import Flask
import threading

# Flask veb server (Render uchun)
app = Flask(__name__)

# Bot sozlamalari
TOKEN = '8608266628:AAFWj6LjTVi6gFaAvEvzy7W6xLc4x8DfzC0'
bot = telebot.TeleBot(TOKEN)

PROVIDER_TOKEN = 'YOUR_PROVIDER_TOKEN_HERE' 

@app.route('/')
def home():
    return "Bot ishlamoqda..."

# Stars mahsulotlari ro'yxati
STARS_PRODUCTS = {
    "stars_50":  {"title": "50 ⭐️ Stars", "price": 13000,  "amount": 50},
    "stars_100": {"title": "100 ⭐️ Stars", "price": 25000, "amount": 100},
    "stars_150": {"title": "150 ⭐️ Stars", "price": 35000, "amount": 150},
    "stars_250": {"title": "250 ⭐️ Stars", "price": 58000, "amount": 250},
    "stars_350": {"title": "350 ⭐️ Stars", "price": 80000, "amount": 350},
    "stars_500": {"title": "500 ⭐️ Stars", "price": 115000, "amount": 500},
    "stars_1000": {"title": "1000 ⭐️ Stars", "price": 220000, "amount": 1000}
}

# Patrik botidagidek asosiy inline menyu (Premium va Partnerka olib tashlangan)
def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    
    # 1. Kupit Telegram Stars (alohida qatorda jozibador)
    btn_buy_stars = types.InlineKeyboardButton("⭐️ Kupit Telegram Stars", callback_data="show_stars_prices")
    
    # 2. Sozdat chek (alohida qatorda)
    btn_create_check = types.InlineKeyboardButton("📄 Sozdat chek", callback_data="create_check")
    
    # 3. Moy profil va Podderjka (bitta qatorda yonma-yon)
    btn_profile = types.InlineKeyboardButton("🥷 Moy profil", callback_data="my_profile")
    btn_support = types.InlineKeyboardButton("🎧 Podderjka", url="https://t.me/muhammad_16") # Admin havolasi
    
    # 4. Otzivi (alohida qatorda, kanalingizga yo'naltirilgan)
    btn_reviews = types.InlineKeyboardButton("💬 Otzivi", url="https://t.me/tg_yulduz_savdo")
    
    # 5. Kak eto rabotaet (eng pastda alohida qatorda)
    btn_how_it_works = types.InlineKeyboardButton("Как это работает ⁉️", callback_data="how_it_works")
    
    # Tugmalarni rasmdagi tartibda joylashtiramiz
    markup.add(btn_buy_stars)
    markup.add(btn_create_check)
    markup.add(btn_profile, btn_support) # yonma-yon
    markup.add(btn_reviews)
    markup.add(btn_how_it_works)
    
    return markup

# /start buyrug'i kelganda Patrik botidek chiroyli matn va inline tugmalar chiqadi
@bot.message_handler(commands=['start'])
def start_message(message):
    welcome_text = (
        "🌟 **Магазин звёзд Патрика**\n\n"
        "«Купил Stars — живёшь, как Патрик в золоте 🛍»\n\n"
        "🤑 **Хватай звёзды НАМНОГО дешевле, чем в ТГ**\n"
        "🔥 У тебя действует скидка на первую покупку!\n\n"
        "👇 Kerakli bo'limni tanlang:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# Inline tugmalar bosilganda ishlaydigan qism
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    if call.data == "show_stars_prices":
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        for key, product in STARS_PRODUCTS.items():
            btn = types.InlineKeyboardButton(f"{product['title']} — {product['price']:,} so'm", callback_data=f"buy_{key}")
            buttons.append(btn)
        markup.add(*buttons)
        # Bosh sahifaga qaytish tugmasi
        markup.add(types.InlineKeyboardButton("⬅️ Главное меню", callback_data="back_to_main"))
        
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text="⭐️ **Kerakli miqdordagi Stars paketini tanlang:**",
            reply_markup=markup,
            parse_mode="Markdown"
        )
        
    elif call.data == "back_to_main":
        welcome_text = (
            "🌟 **Магазин звёзд Патрика**\n\n"
            "«Купил Stars — живёшь, как Патрик в золоте 🛍»\n\n"
            "🤑 **Хватай звёзды НАМНОГО дешевле, чем в ТГ**\n"
            "🔥 У тебя действует скидка на первую покупку!\n\n"
            "👇 Kerakli bo'limni tanlang:"
        )
        bot.edit_message_text(
            chat_id=call.message.chat.id,
            message_id=call.message.message_id,
            text=welcome_text,
            reply_markup=get_main_menu(),
            parse_mode="Markdown"
        )
        
    elif call.data == "my_profile":
        profile_text = (
            f"🥷 **Ваш профиль:**\n\n"
            f"👤 Имя: {call.from_user.first_name}\n"
            f"🆔 ID: `{call.from_user.id}`\n"
            f"🛒 Покупки: 0 раз"
        )
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=profile_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "create_check":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📄 Chek yaratish bo'limi hozircha faol emas.", reply_markup=markup)

    elif call.data == "how_it_works":
        instructions = "⁉️ **Как это работает?**\n\n1. Выбираете количество Stars.\n2. Оплачиваете заказ удобным способом.\n3. Робот автоматически или админ вручную отправляет звёзды на ваш аккаунт!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Назад", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=instructions, reply_markup=markup, parse_mode="Markdown")
        
    elif call.data.startswith("buy_"):
        product_key = call.data.split("_", 1)[1]
        product = STARS_PRODUCTS.get(product_key)
        
        if product:
            bot.send_invoice(
                chat_id=call.message.chat.id,
                title=product['title'],
                description=f"Купить {product['amount']} Stars.",
                provider_token=PROVIDER_TOKEN,
                currency='UZS',
                prices=[types.LabeledPrice(label=product['title'], amount=product['price'] * 100)],
                start_parameter='stars-payment',
                invoice_payload=f"payload_{product_key}"
            )
            bot.answer_callback_query(call.id)

# To'lovoldi tekshiruvi
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# Muvaffaqiyatli to'lov
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    bot.send_message(message.chat.id, "🎉 Оплата прошла успешно! Ваши Stars будут зачислены в ближайшее время.")

# Botni alohida oqimda ishga tushirish
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
