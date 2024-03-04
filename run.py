import os
import sys
import asyncio
from telebot import TeleBot, types
from config import adimin_bot_token ,admin_id

bot = TeleBot(adimin_bot_token,threaded=False)
sys.path.insert(0, os.path.dirname(__file__))

try: import root
except Exception as e: bot.send_message(admin_id,f"#Error Import : {e}")

def app(environ, start_response):
    start_response('200 OK', [('Content-Type', 'text/plain')])
    asyncio.run(multi_bot(environ))
    response = 'OK'
    return [response.encode()]
            
async def multi_bot(environ):
    try:
        if (environ['REQUEST_METHOD'] ==  'POST'):
            token = environ['PATH_INFO'][1:]
            update = [types.Update.de_json(environ['wsgi.input'].read(int(environ['CONTENT_LENGTH'])).decode('utf-8'))]
            if token == root.bot.token:
                try: return await root.bot.process_new_updates(update)
                except Exception as e: return bot.send_message(admin_id,f"#Error root : {e}")
            else: return bot.send_message(admin_id,f"#Error Token : {token} => is not set your bot")
        return 
    except Exception as e:
        return bot.send_message(admin_id,f"#Error app : {e}")



# MetWork
# https://api.telegram.org/bot5357808613:AAFX-HIXP6xivyvHYQJ1qf1_5aTBsPGxQZc/setWebhook?url=https://botcode.uno/MetWork/5357808613:AAFX-HIXP6xivyvHYQJ1qf1_5aTBsPGxQZc
# Test
# https://api.telegram.org/bot235867187:AAFpLl0rscOr3lHZB1lvvSLa_SYsJPyqv8k/setWebhook?url=https://botcode.uno/MetWork/235867187:AAFpLl0rscOr3lHZB1lvvSLa_SYsJPyqv8k
# Test