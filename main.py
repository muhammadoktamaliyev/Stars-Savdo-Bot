import os
import telebot
from telebot import types
from flask import Flask
import threading

# Flask veb-server (Render o'chib qolmasligi uchun)
app = Flask(__name__)

# Bot sozlamalari
TOKEN = '8608266628:AAFWj6LjTVi6gFaAvEvzy7W6xLc4x8DfzC0'
bot = telebot.TeleBot(TOKEN)

# 💳 SIZNING CLICK TOKENINGIZ
PROVIDER_TOKEN = '398062629:TEST:999999999_F91D8F69C042267444B74CC0B3C747757EB0E065' 

# 🛠 SIZNING TELEGRAM ID RAQAMINGIZ (Admin panel faqat sizga ko'rinadi)
ADMIN_ID = 6807375870  

# Foydalanuvchilar ro'yxati va holatlar uchun vaqtinchalik baza
USERS_DB = set()
admin_state = {}

@app.route('/')
def home():
    return "Bot muvaffaqiyatli ishlamoqda..."

# Stars paketlari va narxlari (so'mda)
STARS_PRODUCTS = {
    "stars_50":  {"title": "50 ⭐️ Stars", "price": 13000,  "amount": 50},
    "stars_100": {"title": "100 ⭐️ Stars", "price": 25000, "amount": 100},
    "stars_150": {"title": "150 ⭐️ Stars", "price": 35000, "amount": 150},
    "stars_250": {"title": "250 ⭐️ Stars", "price": 58000, "amount": 250},
    "stars_350": {"title": "350 ⭐️ Stars", "price": 80000, "amount": 350},
    "stars_500": {"title": "500 ⭐️ Stars", "price": 115000, "amount": 500},
    "stars_1000": {"title": "1000 ⭐️ Stars", "price": 220000, "amount": 1000}
}

# Asosiy inline-menyu
def get_main_menu():
    markup = types.InlineKeyboardMarkup()
    btn_buy_stars = types.InlineKeyboardButton("⭐️ Telegram Stars sotib olish", callback_data="show_stars_prices")
    btn_create_check = types.InlineKeyboardButton("📄 Chek yaratish", callback_data="create_check")
    btn_profile = types.InlineKeyboardButton("🥷 Mening profilim", callback_data="my_profile")
    btn_support = types.InlineKeyboardButton("🎧 Yordam / Aloqa", url="https://t.me/muhammad_16")
    btn_reviews = types.InlineKeyboardButton("💬 Fikrlar va sharhlar", url="https://t.me/tg_yulduz_savdo")
    btn_how_it_works = types.InlineKeyboardButton("Bu qanday ishlaydi ⁉️", callback_data="how_it_works")
    
    markup.add(btn_buy_stars)
    markup.add(btn_create_check)
    markup.add(btn_profile, btn_support)
    markup.add(btn_reviews)
    markup.add(btn_how_it_works)
    return markup

# Admin panel menyusi
def get_admin_menu():
    markup = types.InlineKeyboardMarkup()
    btn_send_ads = types.InlineKeyboardButton("📣 Reklama (Rassilka) yuborish", callback_data="admin_send_ads")
    btn_stats = types.InlineKeyboardButton("📊 Bot statistikasi", callback_data="admin_stats")
    markup.add(btn_send_ads)
    markup.add(btn_stats)
    return markup

# /start buyrug'i kelganda
@bot.message_handler(commands=['start'])
def start_message(message):
    USERS_DB.add(message.chat.id) # Foydalanuvchini bazaga qo'shish
    
    welcome_text = (
        "🌟 **Stars Do'koni**\n\n"
        "«Stars xarid qiling — oltin ichidagi Patrikdek yashang 🛍»\n\n"
        "🤑 **Stars paketlarini Telegram'dan ancha arzon narxda oling**\n"
        "🔥 Birinchi xaridingiz uchun maxsus chegirma amal qilmoqda!\n\n"
        "👇 Kerakli bo'limni tanlang:"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")

# /admin paneli (Faqat siz yozganingizda ishlaydi)
@bot.message_handler(commands=['admin'])
def admin_panel(message):
    if message.chat.id == ADMIN_ID:
        bot.send_message(message.chat.id, "🛠 **Xush kelibsiz Admin!**\nBotni boshqarish paneli:", reply_markup=get_admin_menu(), parse_mode="Markdown")

# Admindan reklama matnini qabul qilish
@bot.message_handler(func=lambda message: admin_state.get(message.chat.id) == "waiting_for_ad")
def receive_ad_text(message):
    admin_state[message.chat.id] = None
    success_count = 0
    bot.send_message(message.chat.id, "⏳ Reklama barcha foydalanuvchilarga yuborilmoqda...")
    
    for user_id in USERS_DB:
        try:
            bot.copy_message(chat_id=user_id, from_chat_id=message.chat.id, message_id=message.message_id)
            success_count += 1
        except:
            continue
    bot.send_message(message.chat.id, f"✅ Reklama yakunlandi!\n\n👥 Muvaffaqiyatli yetkazildi: {success_count} ta foydalanuvchiga.")

# Inline tugmalar boshqaruvi
@bot.callback_query_handler(func=lambda call: True)
def handle_callbacks(call):
    # Admin bo'limi tugmalari
    if call.data == "admin_send_ads" and call.message.chat.id == ADMIN_ID:
        admin_state[call.message.chat.id] = "waiting_for_ad"
        bot.send_message(call.message.chat.id, "📝 **Reklama xabarini yuboring:**\n(Matn, rasm yoki video yuborishingiz mumkin, bot uni hamma foydalanuvchilarga tarqatadi)")
        bot.answer_callback_query(call.id)
        
    elif call.data == "admin_stats" and call.message.chat.id == ADMIN_ID:
        stats_text = f"📊 **Bot statistikasi:**\n\n👥 Jami foydalanuvchilar: {len(USERS_DB)} ta\n🟢 Bot holati: Aktiv"
        bot.send_message(call.message.chat.id, stats_text)
        bot.answer_callback_query(call.id)

    # Foydalanuvchilar uchun tugmalar
    elif call.data == "show_stars_prices":
        markup = types.InlineKeyboardMarkup(row_width=2)
        buttons = []
        for key, product in STARS_PRODUCTS.items():
            btn = types.InlineKeyboardButton(f"{product['title']} — {product['price']:,} so'm", callback_data=f"buy_{key}")
            buttons.append(btn)
        markup.add(*buttons)
        markup.add(types.InlineKeyboardButton("⬅️ Asosiy menyu", callback_data="back_to_main"))
        
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="⭐️ **Kerakli Stars paketini tanlang:**", reply_markup=markup, parse_mode="Markdown")
        
    elif call.data == "back_to_main":
        welcome_text = (
            "🌟 **Stars Do'koni**\n\n"
            "«Stars xarid qiling — oltin ichidagi Patrikdek yashang 🛍»\n\n"
            "🤑 **Stars paketlarini Telegram'dan ancha arzon narxda oling**\n"
            "🔥 Birinchi xaridingiz uchun maxsus chegirma amal qilmoqda!\n\n"
            "👇 Kerakli bo'limni tanlang:"
        )
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=welcome_text, reply_markup=get_main_menu(), parse_mode="Markdown")
        
    elif call.data == "my_profile":
        profile_text = f"🥷 **Sizning profilingiz:**\n\n👤 Ism: {call.from_user.first_name}\n🆔 ID raqam: `{call.from_user.id}`\n🛒 Xaridlar soni: 0 ta"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=profile_text, reply_markup=markup, parse_mode="Markdown")

    elif call.data == "create_check":
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text="📄 Chek yaratish bo'limi hozircha ishlamayapti.", reply_markup=markup)

    elif call.data == "how_it_works":
        instructions = "⁉️ **Bu qanday ishlaydi?**\n\n1. Kerakli Stars miqdorini tanlaysiz.\n2. Click orqali plastik kartangiz bilan botni o'zida to'lov qilasiz.\n3. To'lov amalga oshishi bilan adminga srazi xabar boradi va Stars hisobingizga o'tkazib beriladi!"
        markup = types.InlineKeyboardMarkup()
        markup.add(types.InlineKeyboardButton("⬅️ Orqaga", callback_data="back_to_main"))
        bot.edit_message_text(chat_id=call.message.chat.id, message_id=call.message.message_id, text=instructions, reply_markup=markup, parse_mode="Markdown")
        
    # 💳 PULLIK CHEK (INVOICE) YUBORISH QISMI
    elif call.data.startswith("buy_"):
        product_key = call.data.split("_", 1)[1]
        product = STARS_PRODUCTS.get(product_key)
        
        if product:
            try:
                bot.send_invoice(
                    chat_id=call.message.chat.id,
                    title=product['title'],
                    description=f"Telegram uchun {product['amount']} dona Stars paketini Click orqali xarid qilish.",
                    provider_token=PROVIDER_TOKEN,
                    currency='UZS',
                    prices=[types.LabeledPrice(label=product['title'], amount=product['price'] * 100)], # Tiyinda hisoblangani uchun 100 ga ko'paytiriladi
                    start_parameter='stars-payment',
                    invoice_payload=f"payload_{product_key}"
                )
                bot.answer_callback_query(call.id)
            except Exception as e:
                bot.send_message(call.message.chat.id, "⚠️ To'lov tizimida texnik nosozlik yuz berdi. Iltimos admin bilan bog'laning.")

# TO'LOVDAN OLDINGI TEKSHIRUV (Telegram buni tasdiqlashi shart)
@bot.pre_checkout_query_handler(func=lambda query: True)
def checkout(pre_checkout_query):
    bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)

# 💰 TO'LOV MUVAFFAQIYATLI O'TGANDA ISHLAYDIGAN QISM
@bot.message_handler(content_types=['successful_payment'])
def got_payment(message):
    payment_info = message.successful_payment
    payload = payment_info.invoice_payload
    product_key = payload.split("_", 1)[1]
    stars_amount = STARS_PRODUCTS[product_key]["amount"]
    
    # 1. Xaridorga tabrik xabari yuboriladi
    bot.send_message(
        message.chat.id, 
        f"🎉 **To'lov muvaffaqiyatli qabul qilindi!**\n\n"
        f"🛒 Siz **{stars_amount} ⭐️ Stars** paketini sotib oldingiz.\n"
        f"⏳ Admin tez orada Stars'ni hisobingizga o'tkazib beradi!"
    )
    
    # 2. SIZGA (ADMINGA) AVTOMATIK SRAZI XABAR BORADI
    bot.send_message(
        ADMIN_ID, 
        f"💰 **YANGI TO'LOV TUSHDI!**\n\n"
        f"👤 Kim: @{message.from_user.username} (ID: `{message.from_user.id}`)\n"
        f"⭐️ Xarid qildi: {stars_amount} Stars\n"
        f"💵 Pul Click orqali hisobingizga tushdi.\n\n"
        f"👉 Foydalanuvchiga Stars taqdim etishni unutmang!"
    )

# Botni ishga tushirish (Thread orqali)
def run_bot():
    bot.infinity_polling()

if __name__ == "__main__":
    threading.Thread(target=run_bot).start()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
