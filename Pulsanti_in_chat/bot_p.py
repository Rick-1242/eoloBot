import sqlite3
import math as m
import bot_functions
from telegram import *
from telegram.ext import *
from geopy.geocoders import Nominatim
from requests import *
############################### Bot ############################################

def cloasest(update: Update, context: CallbackContext) -> bool:

    #! se non si inserisce una via ma qualsiasi altro messaggio non funziona(TODO check user input)
    street = update.message.text
    street = street + " Vr"
    print(street)
    geolocator = Nominatim(user_agent="TelegramWindBot")
    location = geolocator.geocode(street)
    distance = []
    for staz in context.bot_data["stazCoords"]:
        calcDist = bot_functions.dist(float(location.latitude),
                                  float(location.longitude),
                                  float(staz[2]), float(staz[1]))
        distance.append([staz[0], calcDist])
    sorteDistance = bot_functions.Sort(distance)
    msg = f"La posizione è {location.address}\n"
    msg += f"La stazione più vicina è ID{sorteDistance[0][0]}"
    msg += f" e si trova a {round(sorteDistance[0][1], 3)}Km dalla posizione"
    update.message.reply_text(msg)
    main_menu()


def start(bot, update):
  bot.message.reply_text(main_menu_message(),
                         reply_markup=main_menu_keyboard())

def main_menu(bot, update):
  bot.callback_query.message.edit_text(main_menu_message(),
                          reply_markup=main_menu_keyboard())

def first_menu(bot, update, ):
  bot.callback_query.message.edit_text(first_menu_message(),
                          reply_markup=first_menu_keyboard())

def second_menu(bot:Bot, update: Update, context):
    bot.callback_query.message.edit_text(second_menu_message(),
                          reply_markup=second_menu_keyboard())
    cloasest(update, context)

def first_submenu(bot, update):
  pass

def second_submenu(bot, update):
  pass

def error(update, context):
    print(f'Update {update} caused error {context.error}')

############################ Keyboards #########################################
def main_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Mappa', callback_data='M')],
              [InlineKeyboardButton('Stazione', callback_data='C')]]
  return InlineKeyboardMarkup(keyboard)

def first_menu_keyboard():
  keyboard = [[InlineKeyboardButton("Link per mappa", url = "http://u.osmfr.org/m/780280/")], 
              [InlineKeyboardButton('Mappa', callback_data='M')],
              [InlineKeyboardButton('Stazione', callback_data='C')]]
  return InlineKeyboardMarkup(keyboard)

def second_menu_keyboard():
  keyboard = [[InlineKeyboardButton('Mappa', callback_data='M')],
              [InlineKeyboardButton('Stazione', callback_data='C')]]
  return InlineKeyboardMarkup(keyboard)

############################# Messages #########################################
def main_menu_message():
  return 'f"Ciao {update.effective_user.first_name}\nBenvenuto nel WindBot"'

def first_menu_message():
  return 'Hai richiesto la mappa delle stazioni'

def second_menu_message():
  return 'Inserire un\'indirizzo:'

############################# Handlers #########################################
def main():
    with open("token.txt", "r", ) as f:
        TOKEN = f.read()
        print("Il tuo token è: ", TOKEN)

    db = sqlite3.connect("wether.db")
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

    disp.add_handler(CommandHandler('start', start))
    disp.add_handler(CallbackQueryHandler(main_menu, pattern='main'))
    disp.add_handler(CallbackQueryHandler(first_menu, pattern='M'))
    disp.add_handler(CallbackQueryHandler(second_menu, pattern='C'))
    disp.add_error_handler(error)
    disp.add_handler(CallbackQueryHandler(first_submenu, pattern=''))
    disp.add_handler(CallbackQueryHandler(second_submenu, pattern=''))

    updater.start_polling()
    updater.idle()

    if db:
        db.close()


if __name__ == "__main__":
    main()
