import os
import json
import gspread
from google.oauth2.service_account import Credentials
from telegram import Update, ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes
from datetime import datetime

TOKEN = os.environ.get("BOT_TOKEN")
SHEET_ID = os.environ.get("SHEET_ID")
GOOGLE_CREDENTIALS = os.environ.get("GOOGLE_CREDENTIALS")

IMAGE_URL = "https://i.ibb.co/twgTsdxf/Chat-GPT-Image-13-svi-2026-20-55-23.png"

MESSAGES = {
    "Balkan": {
        "image": "https://i.ibb.co/hRJYdnn8/Chat-GPT-Image-13-svi-2026-21-10-41.png",
        "welcome": "*🇭🇷🇧🇦🇷🇸🇲🇪🇸🇮 Odlično!*\n\nDa bi primio *World Cup Ebook* sa svim važnim stvarima i predikcijama, klikni ispod i poslat ćemo ga direktno na tvoj broj mobitela 👇",
        "success": "✅ *Savršeno! Registracija uspješna!* Pripremi se za World Cup tipove! 🏆🔥",
    },
    "Sweden": {
        "image": "https://i.ibb.co/R49n42PG/Chat-GPT-Image-13-svi-2026-21-43-42.png",
        "welcome": "*🇸🇪 Välkommen!*\n\nFör att få *World Cup Ebook* med all viktig information och förutsägelser, klicka nedan så skickar vi det direkt till ditt telefonnummer 👇",
        "success": "✅ *Perfekt! Registreringen lyckades!* Gör dig redo för World Cup picks! 🏆🔥",
    },
    "Finland": {
        "image": "https://i.ibb.co/JRTCyM5n/Chat-GPT-Image-13-svi-2026-21-48-44.png",
        "welcome": "*🇫🇮 Tervetuloa!*\n\nSaadaksesi *World Cup Ebook* -kirjan, jossa on kaikki tärkeät tiedot ja ennusteet, klikkaa alla ja lähetämme sen suoraan puhelinnumeroosi 👇",
        "success": "✅ *Täydellinen! Rekisteröinti onnistui!* Valmistaudu World Cup vinkkeihin! 🏆🔥",
    },
    "Norway": {
        "image": "https://i.ibb.co/rGDJzG5x/Chat-GPT-Image-13-svi-2026-21-27-00.png",
        "welcome": "*🇳🇴 Velkommen!*\n\nFor å motta *World Cup Ebook* med all viktig informasjon og spådommer, klikk nedenfor så sender vi det direkte til telefonnummeret ditt 👇",
        "success": "✅ *Perfekt! Registreringen var vellykket!* Gjør deg klar for World Cup-tips! 🏆🔥",
    },
    "Netherlands": {
        "image": "https://i.ibb.co/279T0mcN/Chat-GPT-Image-13-svi-2026-21-35-52.png",
        "welcome": "*🇳🇱 Welkom!*\n\nOm het *World Cup Ebook* te ontvangen met alle belangrijke informatie en voorspellingen, klik hieronder en we sturen het direct naar je telefoonnummer 👇",
        "success": "✅ *Perfect! Registratie geslaagd!* Maak je klaar voor World Cup tips! 🏆🔥",
    },
    "France": {
        "image": "https://i.ibb.co/Z1vLJ6Qs/Chat-GPT-Image-13-svi-2026-21-38-56.png",
        "welcome": "*🇫🇷 Bienvenue!*\n\nPour recevoir le *World Cup Ebook* avec toutes les informations importantes et les prédictions, cliquez ci-dessous et nous vous l'enverrons directement sur votre numéro de téléphone 👇",
        "success": "✅ *Parfait! Inscription réussie!* Préparez-vous pour les picks de la Coupe du Monde! 🏆🔥",
    },
    "Bulgaria": {
        "image": "https://i.ibb.co/S7HMvT0v/Chat-GPT-Image-13-svi-2026-21-52-43.png",
        "welcome": "*🇧🇬 Добре дошли!*\n\nЗа да получиш *World Cup Ebook* с всички важни неща и прогнози, кликни по-долу и ще го изпратим директно на телефонния ти номер 👇",
        "success": "✅ *Перфектно! Регистрацията е успешна!* Пригответе се за прогнози от Световното! 🏆🔥",
    },
    "Other": {
        "image": "https://i.ibb.co/gZP0135N/Chat-GPT-Image-13-svi-2026-22-26-29.png",
        "welcome": "*🌍 Welcome!*\n\nTo receive the *World Cup Ebook* with all important stuff and predictions click below and we will send it directly to your phone number 👇",
        "success": "✅ *Perfect! Registration successful!* Get ready for World Cup picks! 🏆🔥",
    },
}

COUNTRIES = [
    ("🇭🇷🇧🇦🇷🇸🇲🇪🇸🇮 Balkan", "Balkan"),
    ("🇸🇪 Sweden", "Sweden"),
    ("🇫🇮 Finland", "Finland"),
    ("🇳🇴 Norway", "Norway"),
    ("🇳🇱 Netherlands", "Netherlands"),
    ("🇫🇷 France", "France"),
    ("🇧🇬 Bulgaria", "Bulgaria"),
    ("🌍 Something else", "Other"),
]

def get_sheet():
    creds_dict = json.loads(GOOGLE_CREDENTIALS)
    creds = Credentials.from_service_account_info(creds_dict, scopes=[
        "https://www.googleapis.com/auth/spreadsheets"
    ])
    client = gspread.authorize(creds)
    return client.open_by_key(SHEET_ID).sheet1

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = InlineKeyboardMarkup([
        [InlineKeyboardButton(label, callback_data=code)]
        for label, code in COUNTRIES
    ])
    await update.message.reply_photo(
        photo=IMAGE_URL,
        caption="*Sector1 World Cup Event IS HERE!!!* 🌍🏆\n\nWe prepared an Ebook for you to help you understand how Sector1 team is going to approach the BIGGEST EVENT on the market 🎯\n\nWe will also give you information on best picks and hot topic during the World Cup 🔥\n\nSelect where are you from 👇",
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def country_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data
    context.user_data["country"] = country

    msg = MESSAGES[country]
    button = KeyboardButton("📱 Share My Number", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await query.message.reply_photo(
        photo=msg["image"],
        caption=msg["welcome"],
        reply_markup=keyboard,
        parse_mode="Markdown"
    )

async def contact_received(update: Update, context: ContextTypes.DEFAULT_TYPE):
    contact = update.message.contact
    name = update.effective_user.first_name
    phone = contact.phone_number
    telegram_id = update.effective_user.id
    country = context.user_data.get("country", "Unknown")
    date = datetime.now().strftime("%Y-%m-%d %H:%M")

    sheet = get_sheet()
    sheet.append_row([name, phone, str(telegram_id), country, date])

    msg = MESSAGES.get(country, MESSAGES["Other"])
    await update.message.reply_text(
        msg["success"],
        parse_mode="Markdown"
    )

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(country_selected))
app.add_handler(MessageHandler(filters.CONTACT, contact_received))
app.run_polling()
