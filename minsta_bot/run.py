import os
import sys
import asyncio

sys.path.insert(0, os.path.dirname(__file__))
###########
from telebot import TeleBot, types, util
bot = TeleBot('235867187:AAFpLl0rscOr3lHZB1lvvSLa_SYsJPyqv8k',threaded=False)
###########
try: import minsta_bot
except Exception as e: bot.send_message(5037427439,f"#Error Import : {e}")

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    if (environ['REQUEST_METHOD'] ==  'POST'):
        asyncio.run(run(environ))
    response = 'OK'
    return [response.encode()]

async def run(environ):
    try:
        token = environ['PATH_INFO'][1:]
        update = [types.Update.de_json(environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8'))]
        if token == minsta_bot.bot.token:
            try: return await minsta_bot.bot.process_new_updates(update)
            except Exception as e: return bot.send_message(5037427439,f"#Error minsta_bot : {e}")
        return
    except Exception as e:
        return bot.send_message(5037427439,f"#Error app : {e}")



# Minsta
# https://api.telegram.org/bot5064984249:AAH5fXKKHSQHJFOjLes7Cd5P4piFO0gRn00/setWebhook?url=https://botcode.uno/Minsta-Bot/5064984249:AAH5fXKKHSQHJFOjLes7Cd5P4piFO0gRn00