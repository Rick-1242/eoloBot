import sqlite3
import math as m
import functions
from telegram import *
from telegram.ext import *
from geopy.geocoders import Nominatim
from requests import *


def cloasest(update: Update, context: CallbackContext) -> bool:
    satisfied = False

    #! se non si inserisce una via ma qualsiasi altro messaggio non funziona(TODO check user input)
    street = update.message.text + " Vr"
    geolocator = Nominatim(user_agent="TelegramWindBot")
    location = geolocator.geocode(street)
    distance = []
    for staz in context.bot_data["stazCoords"]:
        calcDist = functions.dist(float(location.latitude),
                                  float(location.longitude),
                                  float(staz[2]), float(staz[1]))
        distance.append([staz[0], calcDist])
    sorteDistance = functions.Sort(distance)
    msg = f"La posrizione è {location.address}\n"
    msg += f"La stazione più vicina è ID{sorteDistance[0][0]}"
    msg += f" e si trova a {round(sorteDistance[0][1], 3)}Km dalla posizione"
    update.message.reply_text(msg)

    # buttons = [[KeyboardButton("✔️")], [(KeyboardButton("❌"))]]
    # context.bot.send_message(chat_id=update.effective_chat.id, text="É coretta?",
    #                          reply_markup=ReplyKeyboardMarkup(buttons))
    # if "✔️" in update.message.text:
    #     satisfied = True
    return satisfied


def handle_message(update: Update, context: CallbackContext):
    if context.bot_data["iscloseStazClicked"]:
        satisfied = cloasest(update, context)
        # TODO Make this work(if first inpunt is wrong offer second input)
        if satisfied:
            context.bot_data["iscloseStazClicked"] = False
    else:
        if context.bot_data["Mappa"] in update.message.text:
            buttons = [[InlineKeyboardButton(
                "Link per la mappa delle stazioni meteo", url="http://u.osmfr.org/m/780280/")]]
            context.bot.send_message(chat_id=update.effective_chat.id,
                                     text="Hai richiesto la mappa delle stazioni meteo", reply_markup=InlineKeyboardMarkup(buttons))
        elif context.bot_data["closeStaz"] in update.message.text:
            context.bot_data["iscloseStazClicked"] = True
            update.message.reply_text("Inserire un indirizzo.")
        # else:
        #     update.message.reply_text("Comando non valido")


def main():
    with open("token.txt", "r", ) as f:
        TOKEN = f.read()
        print("Il tuo token è: ", TOKEN)

    db = sqlite3.connect("../db/wether.db")
    updater = Updater(TOKEN, use_context=True)
    disp = updater.dispatcher
    disp.bot_data = {"Mappa": "Mappa del 💨",
                     "closeStaz": "Stazione 💨 piu vicina",
                     "iscloseStazClicked": False}

    try:
        cursor = db.cursor()
        querry = """SELECT IDSTAZ, Longitude, Latitude FROM CoordinateStazioni"""
        cursor.execute(querry)
        stazCoords = cursor.fetchall()
        disp.bot_data["stazCoords"] = stazCoords
    except sqlite3.Error as sqlerror:
        print("Error while connecting to sqlite", sqlerror)

    disp.add_handler(CommandHandler("start", functions.start))
    disp.add_handler(CommandHandler("help", functions.help))
    disp.add_handler(MessageHandler(Filters.text, handle_message))
    disp.add_error_handler(functions.error)

    updater.start_polling()
    updater.idle()

    if db:
        db.close()


if __name__ == "__main__":
    main()
