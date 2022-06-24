import config, sqlite3
import math as m
from telegram import *
from telegram.ext import *
from geopy.geocoders import Nominatim
from requests import *

with open("token.txt", "r", ) as f:
    TOKEN = f.read()
    print("Il tuo token è: ", TOKEN)

iscloseStazClicked = False
Mappa = "Mappa del 💨"
closeStaz = "Stazione 💨 piu vicina"
Indietro = "Indietro"
db = sqlite3.connect("wether.db")

def start(update: Update, context: CallbackContext):
    buttons = [[KeyboardButton(Mappa)], [(KeyboardButton(closeStaz))]]
    context.bot.send_message(chat_id=update.effective_chat.id, text="Benvenuto nel WindBot",
        reply_markup=ReplyKeyboardMarkup(buttons))

def get_loc(street: str) -> str:
    geolocator = Nominatim(user_agent="TelegramWindBot")
    location = geolocator.geocode(street)
    return location.longitude, location.latitude

def cloasest(db, update: Update, context: CallbackContext):
    # try:
    #     cursor = db.cursor()
    #     querry = """SELECT IDSTAZ, Latitude, Longitude FROM CoordinateStazioni"""
    #     cursor.execute(querry)
    #     allStaz = cursor.fetchall()
    # except sqlite3.Error as sqlerror:
    #     print("Error while connecting to sqlite", sqlerror)

    street = update.message.text + " Vr" # <-- se non si inserisce una via ma qualsiasi altro messaggio si rompe tutto
    update.message.reply_text(street)
    coords = get_loc(street)
    update.message.reply_text(f"{coords[1]}, {coords[0]}")

#(iscloseStazClicked, Mappa, closeStaz, db, update, callbackContext)
def handle_message(update: Update, context: CallbackContext):

    global iscloseStazClicked
    global Mappa
    global closeStaz
    global db

    if iscloseStazClicked:
        if Indietro in update.message.text:
            iscloseStazClicked = False
            buttons = [[KeyboardButton(Mappa)], [(KeyboardButton(closeStaz))]]
            context.bot.send_message(chat_id=update.effective_chat.id, text="Usa i comandi per scegliere un'azione",
                reply_markup=ReplyKeyboardMarkup(buttons))
        elif Mappa in update.message.text or closeStaz in update.message.text:
                update.message.reply_text("Comando non valido. Please inserire un indirizzo")
        else:
            cloasest(db, update, context)
            iscloseStazClicked = False
    else:
        if Mappa in update.message.text:        
            buttons = [[InlineKeyboardButton("Link per la mappa delle stazioni meteo", url = "http://u.osmfr.org/m/780280/")]]
            context.bot.send_message(chat_id=update.effective_chat.id, text = "Hai richiesto la mappa delle stazioni meteo", reply_markup= InlineKeyboardMarkup(buttons))
        elif closeStaz in update.message.text:
            iscloseStazClicked = True
            buttons = [[KeyboardButton(Mappa)], [(KeyboardButton(closeStaz))], [(KeyboardButton(Indietro))]]
            context.bot.send_message(chat_id=update.effective_chat.id, text="Inserire un indirizzo",
            reply_markup=ReplyKeyboardMarkup(buttons))

"""
        else:
            update.message.reply_text("Comando non valido")
"""


def dist(lat1, lon1, lat2, lon2) -> float:
    """Calcutaes the distance between two coords

    Args:
        lat1 (float): latitude of first pos
        lon1 (float): longitude of first pos
        lat2 (float): latitude of second pos
        lon2 (float): longitude of second pos

    Returns:
        float: Distace between the two coords
    """
    num1 = m.sin((m.radians(lat2) - m.radians(lat1)) / 2)
    num2 = m.sin((m.radians(lon2) - m.radians(lon1)) / 2)
    return 6371 * 2 * m.asin(m.sqrt(m.pow(num1, 2) + m.cos(lat1) * m.cos(lat2) * m.pow(num2, 2)))

def help(update: Update, context: CallbackContext):
    update.message.reply_text("""
    Sono disponibili i seguenti comandi:

    /start --> Per avviare il bot
    """)

def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")

def main():

    
    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher

    disp.add_handler(CommandHandler("start", start))
    disp.add_handler(CommandHandler("help", help))
    disp.add_handler(MessageHandler(Filters.text, handle_message))

    disp.add_error_handler(error)

    updater.start_polling()
    updater.idle()
    if db:
        db.close()


if __name__ == "__main__":
    main()
