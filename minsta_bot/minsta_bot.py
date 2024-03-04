import os 
import sys
import asyncio
import re
try:
    import telebot 
except ImportError:
    os.system("pip3 install pytelegrambotapi")
from telebot.async_telebot import AsyncTeleBot
from telebot import types
from .config import admin_id ,setting_channel_id ,setting ,users_db ,admin_db ,support_db ,database_minsta ,next_msg_db # . del #
from CFunc import MenuInsta , MainMenu

sys.path.insert(0, os.path.dirname(__file__))

class Register(MainMenu ,MenuInsta):
    '''
    all func Register
    '''   
    def __init__(self):
        self.bot = AsyncTeleBot(setting['token'])
        self.next_msg_db = next_msg_db
        self.Register()
        return
    
    async def Error(self ,name=None ,e=None):# Error handler
        return await self.bot.send_message(admin_id ,f'#Error MinstaBot.{name} : {e}')

    # Register bot handler
    def Register(self):
        
        self.bot.register_message_handler(self.msg_command ,
            commands=['start' ,'settings' ,'profile' ,'help'],pass_bot=True)

        self.bot.register_callback_query_handler(self.callback_menu ,
            func=lambda c : c.data.startswith('#') ,pass_bot=True)

        self.bot.register_callback_query_handler(self.callback_insta ,
            func=lambda c : c.data.startswith('$') ,pass_bot=True)

        self.bot.register_message_handler(self.nextpm ,func=lambda m: self.next_msg_db[m.from_user.id],
            content_types=['text'],pass_bot=True)
        
        self.bot.register_message_handler(self.register_msg ,
            content_types=['text'],pass_bot=True)

        self.bot.register_inline_handler(self.inline_query ,
            func=lambda q:True,pass_bot=True)
        return

    # all inline query
    async def inline_query(self ,inline_query:types.InlineQuery ,bot:AsyncTeleBot):# startswiths (#)
        '''
        command:
            @Mnistabot {username_id}/   => find profile
            @Minstabot {username_id}/p/{index}/ => post
            @Minstabot {username_id}/s/{index}/ => story
            @Minstabot {username_id}/h/{index}/ => hilight caver
            @Minstabot {username_id}/h/{index}/{index2}/ => hilight item
        '''
        try:
            if len(inline_query.query) == 0: return await self.inline_help_pro(bot ,inline_query)
            if not inline_query.query.endswith('/'): return await self.inline_tab(bot ,inline_query)
            u = users_db[inline_query.from_user.id]
            data = inline_query.query.split('/')
            l = len(data)
            if (data[1] == ''):return await self.inline_profile(u ,bot ,inline_query ,data)
            elif (data[1] == 'p'):
                if (l == 4):return await self.inline_post(u ,bot ,inline_query ,data)
                else:return await self.inline_help_post(bot ,inline_query)
            elif (data[1] == 's'):
                if (l == 4):return await self.inline_story(u ,bot ,inline_query ,data)
                else:return await self.inline_help_story(bot ,inline_query)
            elif (data[1] == 'h'):
                if (l == 5): return await self.inline_hilight(u ,bot ,inline_query ,data ,item=True)
                elif (l == 4): return await self.inline_hilight(u ,bot ,inline_query ,data)
                else: return await self.inline_help_hilight(bot ,inline_query)
        except Exception as e : return await self.Error('inline_query_all',e)

    # menu call back for minstabot    call.data.startswith('#')
    async def callback_menu(self ,call:types.CallbackQuery ,bot:AsyncTeleBot):#=> (#)
        try:
            print(call.data)
            u = users_db[call.from_user.id]
            if self.next_msg_db[admin_id] :self.next_msg_db.delete_pm(admin_id)
            if (call.data == '#M'): return await self.start_menu(u=u ,bot=bot ,edit=call.message.id)
            elif (call.data == '#S'): return await self.setting_(u=u ,bot=bot ,edit=call.message.id)
            elif call.data.startswith('#W'): return await self.watch_list(u=u ,bot=bot ,call=call)
            elif call.data.startswith('#L'): return await self.set_lan(u=u ,bot=bot ,call=call ,edit=call.message.id)
            elif call.data.startswith('#IP'): return await self.profile_(u=u ,bot=bot ,call=call)
            elif call.data.startswith('#X'): return await self.login(u=u ,bot=bot  ,mode='u' ,data={"bmsg_id":call.message.id})
            elif call.data.startswith('#P'): return await self.poshtibai(u=u ,bot=bot ,bmsg=call.message.id)
            else: return await bot.send_message(admin_id ,f'Linkbot.callback_menu : data = {call.data}') 
        except Exception as e : return await self.Error('callback_menu',e)
    
    # insta call back for minstabot   call.data.startswith('$')
    async def callback_insta(self ,call:types.CallbackQuery ,bot:AsyncTeleBot):#=> ($)
        try:
            print(call.data) # DEBUG TRUE
            u = users_db[call.from_user.id]
            if self.next_msg_db[admin_id] :self.next_msg_db.delete_pm(admin_id)
            if call.data.startswith('$PR'): 
                return await self.find_pro(u ,bot ,msg=call.message ,profile_id=int(call.data.split('/')[-1]))
            elif call.data.startswith('$PS'): return await self.menu_post(u ,bot ,call)
            elif call.data.startswith('$SP'): return await self.menu_saved_post(u ,bot ,call)
            elif call.data.startswith('$ST'): return await self.menu_story(u ,bot ,call)
            elif call.data.startswith('$HI'): return await self.menu_hilight(u ,bot ,call)
            elif call.data.startswith('$IG'): return await self.menu_igtv(u ,bot ,call)
            else: return await bot.send_message(admin_id ,f'Linkbot.callback_insta : data = {call.data}') 
        except Exception as e : return await self.Error('callback_insta',e)

    # get command msg
    async def msg_command(self ,msg:types.Message ,bot:AsyncTeleBot):
        try:  
            u = users_db[msg.from_user.id]  
            if (msg.text == '/start'): return await self.start_menu(u=u ,bot=bot ,msg=msg)
            elif msg.text.startswith('/start'):
                if (len(msg.text.split(' ')) == 2):
                    _ , data_ = msg.text.split(' ')
                    mod ,userid = data_.split('_')

                # /start  PRO/{profile_id}
                if (mod == 'PRO'): return await self.find_pro(u ,bot ,msg ,profile_id=msg.text.split('/')[-1])
                
                # /start  PS/{shortcode} or /start  IG/{shortcode}  
                elif (mod == 'PS') or (mod == 'IG'): return await self.menu_shortcode(u ,bot ,msg)

                # /start  ST/{profile_id}/{index}
                elif (mod == 'ST'): return await self.command_story(u ,bot ,msg)

                # /start  HI/{profile_id}/{index}/{index2}
                elif (mod == 'HI'): return await self.command_hilight(u ,bot ,msg)

            elif msg.text.startswith('/settings'): return await self.setting_(u=u ,bot=bot ,msg=msg)
            elif msg.text.startswith('/profile'): return await self.profile_(u=u ,bot=bot ,msg=msg)
            elif msg.text.startswith('/whatch_list'): return await self.watch_list(u=u ,bot=bot ,msg=msg)
            elif msg.text.startswith('/help'): self.min_help(u ,bot)
        except Exception as e: return await bot.send_message(admin_id ,f'msg_start : {e}')

    # next msg handler
    async def nextpm(self ,msg:types.Message ,bot:AsyncTeleBot):#Call Back Next Msg
        try:
            u = users_db[msg.from_user.id]
            data = self.next_msg_db[msg.from_user.id]
            self.next_msg_db.delete_pm(msg.from_user.id)
            print(f"nect pm : {data['mod']}")
            if data['mod'].startswith('p'): return await self.login(u=u ,bot=bot  ,msg=msg ,mode='p' ,data=data)
            elif data['mod'].startswith('x'): return await self.login(u=u ,bot=bot  ,msg=msg ,mode='x' ,data=data)
            elif data['mod'].startswith('c'): return await self.login(u=u ,bot=bot  ,msg=msg ,mode='c' ,data=data)
            elif data['mod'].startswith('#P'): return await self.poshtibai(u=u ,bot=bot ,msg=msg ,data=data)
            else: return await bot.send_message(admin_id ,f'nextpm Not Set: {data}')
        except Exception as e: return self.Error('nextpm',e)    
    
    # get msg for register
    async def register_msg(self ,msg:types.Message ,bot:AsyncTeleBot):
        u = users_db[msg.from_user.id] 
        if msg.text.startswith('@'): return await self.find_pro(u ,bot ,msg)

        # https://www.instagram.com/p/{short_code}
        elif ('/p/' in msg.text): return await self.find_pro(u ,bot ,msg)

        # https://www.instagram.com/tv/{short_code}
        elif ('/tv/' in msg.text): return await self.find_pro(u ,bot ,msg)

        else: print(msg)


if __name__ == "__main__":
    print('__run__')
    br = Register()
    async def main():
        await br.bot.infinity_polling()
    asyncio.run(main())