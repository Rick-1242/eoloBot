from telegram import *
from telegram.ext import *
import math as m
import numpy


def start(update: Update, context: CallbackContext):
    msg = f"Ciao {update.effective_user.first_name}\nBenvenuto nel WindBot"
    buttons = [[KeyboardButton(context.bot_data["Mappa"])], [
        (KeyboardButton(context.bot_data["closeStaz"]))]]
    context.bot.send_message(chat_id=update.effective_chat.id, text=msg,
                             reply_markup=ReplyKeyboardMarkup(buttons))


def error(update: Update, context: CallbackContext):
    print(f"Update {update} caused error {context.error}")


def help(update: Update, context: CallbackContext):
    update.message.reply_text("""
    Sono disponibili i seguenti comandi:

    /start --> Per avviare il bot
    """)


def dist(latitude1,  longitude1,  latitude2,  longitude2) -> float:
    """Calcutaes the distance between two coords

    Args:
        lat1 (float): latitude of first pos
        lon1 (float): longitude of first pos
        lat2 (float): latitude of second pos
        lon2 (float): longitude of second pos

    Returns:
        float: Distace between the two coords in KM
    """
    theta =  longitude1 -  longitude2; 
    distance = (m.sin(numpy.deg2rad( latitude1)) * m.sin(numpy.deg2rad( latitude2))) + (m.cos(numpy.deg2rad( latitude1)) * m.cos(numpy.deg2rad( latitude2)) * m.cos(numpy.deg2rad( theta))); 
    distance = m.acos(distance); 
    distance = numpy.rad2deg(distance); 
    distance =  distance * 60 * 1.1515; 
    distance =  distance * 1.609344;  
    return (round( distance,2)); 

    #num1 = m.sin((m.radians(lat2) - m.radians(lat1)) / 2)
    #num2 = m.sin((m.radians(lon2) - m.radians(lon1)) / 2)
    #return 6371 * 2 * m.asin(m.sqrt(m.pow(num1, 2) + m.cos(lat1) * m.cos(lat2) * m.pow(num2, 2)))


def Sort(sub_li):
    l = len(sub_li)
    for i in range(0, l):
        for j in range(0, l-i-1):
            if (sub_li[j][1] > sub_li[j + 1][1]):
                tempo = sub_li[j]
                sub_li[j] = sub_li[j + 1]
                sub_li[j + 1] = tempo
    return sub_li
