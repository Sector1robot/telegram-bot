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

MESSAGES = {
    "Balkan": {
        "welcome": "Odlično! 🇭🇷🇧🇦🇷🇸🇲🇪🇸🇮\n\nDobrodošao u Sector1 World Cup Event! 🌍🏆\n\nPodjeli svoj broj mobitela kako bi primao naše tipove direktno na mobitel 👇",
        "success": "✅ Savršeno! Registracija uspješna! Pripreми se za World Cup tipove! 🏆🔥",
    },
    "Sweden": {
        "welcome": "Välkommen! 🇸🇪\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nDela ditt telefonnummer för att få våra picks direkt på mobilen 👇",
        "success": "✅ Perfekt! Registreringen lyckades! Gör dig redo för World Cup picks! 🏆🔥",
    },
    "Finland": {
        "welcome": "Tervetuloa! 🇫🇮\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nJaa puhelinnumerosi saadaksesi vihjeet suoraan puhelimeesi 👇",
        "success": "✅ Täydellinen! Rekisteröinti onnistui! Valmistaudu World Cup vinkkeihin! 🏆🔥",
    },
    "Norway": {
        "welcome": "Velkommen! 🇳🇴\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nDel telefonnummeret ditt for å motta våre tips direkte på mobilen 👇",
        "success": "✅ Perfekt! Registreringen var vellykket! Gjør deg klar for World Cup-tips! 🏆🔥",
    },
    "Netherlands": {
        "welcome": "Welkom! 🇳🇱\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nDeel je telefoonnummer om onze tips direct op je mobiel te ontvangen 👇",
        "success": "✅ Perfect! Registratie geslaagd! Maak je klaar voor World Cup tips! 🏆🔥",
    },
    "France": {
        "welcome": "Bienvenue! 🇫🇷\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nPartagez votre numéro de téléphone pour recevoir nos picks directement sur votre mobile 👇",
        "success": "✅ Parfait! Inscription réussie! Préparez-vous pour les picks de la Coupe du Monde! 🏆🔥",
    },
    "Bulgaria": {
        "welcome": "Добре дошли! 🇧🇬\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nСподели телефонния си номер, за да получаваш нашите прогнози директно на телефона си 👇",
        "success": "✅ Перфектно! Регистрацията е успешна! Пригответе се за прогнози от Световното! 🏆🔥",
    },
    "Other": {
        "welcome": "Welcome! 🌍\n\nWelcome to Sector1 World Cup Event! 🌍🏆\n\nShare your phone number to receive our picks directly on your mobile 👇",
        "success": "✅ Perfect! Registration successful! Get ready for World Cup picks! 🏆🔥",
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
    await update.message.reply_text(
        "Sector1 World Cup Event IS HERE!!! 🌍🏆\n\nSelect where are you from 👇",
        reply_markup=keyboard
    )

async def country_selected(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    country = query.data
    context.user_data["country"] = country

    msg = MESSAGES[country]
    button = KeyboardButton("📱 Share My Number", request_contact=True)
    keyboard = ReplyKeyboardMarkup([[button]], resize_keyboard=True, one_time_keyboard=True)
    await query.message.reply_text(msg["welcome"], reply_markup=keyboard)

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
    await update.message.reply_text(msg["success"])

app = ApplicationBuilder().token(TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(CallbackQueryHandler(country_selected))
app.add_handler(MessageHandler(filters.CONTACT, contact_received))
app.run_polling()
