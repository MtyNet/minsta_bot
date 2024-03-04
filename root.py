import os
import asyncio
import sys
import threading ## no compelte
sys.path.insert(0, os.path.dirname(__file__))
try:
	import telebot
except ImportError: 
	os.system("pip install pytelegrambotapi")
try:
	import aiohttp
except ImportError: 
    os.system("pip install aiohttp")
    
import telebot 
from telebot import types 
from telebot.async_telebot import AsyncTeleBot
# import my proje
from minsta_bot.root_minstabot import RootMinsta
# my cods
from config import admin_id ,adimin_bot_token

# my program Name
programs = ['minstabot']

bot = AsyncTeleBot(adimin_bot_token) # root bot
markup = types.InlineKeyboardMarkup
button = types.InlineKeyboardButton
################################################################################
### Root
################################################################################
# control all bots 
@bot.message_handler(commands=['start'] ,func=lambda msg:msg.from_user.id == admin_id)
async def start_message(msg):
    mark = markup(row_width=1)
    text = 'Choose your bot ⬇️\n'
    for program in programs:
        t = f'/{program} \n'
        text += t
        mark.add(button(program ,callback_data=program))
    return await bot.send_message(chat_id=admin_id, text=text, reply_markup=mark)
    

################################################################################
### Minstabot
################################################################################
insta = RootMinsta(bot_=bot) # (#)

