import os
import sys
import asyncio
import telebot 
from telebot import types 
from telebot.async_telebot import AsyncTeleBot
import re
sys.path.append('/home/botcodeu/Telegram-Bot/minsta_bot')
from .config import admin_id ,setting_channel_id ,setting ,users_db ,admin_db ,support_db ,database_minsta

bot = AsyncTeleBot
markup = types.InlineKeyboardMarkup
button = types.InlineKeyboardButton

################################################################################
### Minstabot
################################################################################
class RootMinsta:
    
    def __init__(self ,bot_:AsyncTeleBot):
        global bot
        bot = bot_
        self.mark_cansel = markup().row(button('Cancel' ,callback_data='Minstabot_dlt'))
        self.pm = False
        self.cal = False
        self.def_next = None


    async def minstabot(self ,msg):
        try:
            mark = markup(row_width=1)
            text = '............    Minstabot    ..............'
            mark.add(button('Setting',callback_data='#S'),
                        button('User',callback_data='#U'),
                        button('Propaganda',callback_data='#P'),
                        button('Database',callback_data='#D'),
                        button('support_db',callback_data='#C'),
                        button('Admins',callback_data='#A'))
            return await bot.send_message(admin_id ,text ,reply_markup=mark)
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.minstabot : {e}')
    
    async def next_landle(self ,msg):
        try:
            self.pm = False
            if(msg.text == '/cancel'):
                await bot.delete_message(admin_id ,msg.id)
                return await bot.delete_message(admin_id ,msg.id-1)
            else:
                if self.def_next :
                    try:
                        func , *arg = self.def_next
                        self.def_next = None
                        return await func(msg ,*arg )
                    except:
                        func =self.def_next[0]
                        self.def_next = None
                        return await func(msg)
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.next_landle : {e}')
        
    async def callback_minsta(self ,call):
        try:
            if  (call.data == 'Minstabot'):
                mark = markup(row_width=1)
                text = '............    Minstabot    ..............'
                mark.row(button('Setting',callback_data='#S'))
                mark.row(button('User',callback_data='#U'))
                mark.row(button('Propaganda',callback_data='#P'))
                mark.row(button('Database',callback_data='#D'))
                mark.row(button('support_db',callback_data='#C'))
                mark.row(button('Admins',callback_data='#A'))
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            if call.data.endswith('dlt'): 
                self.pm = False
                self.def_next = None
                return await bot.delete_message(admin_id ,call.message.id )
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.callback_minsta : {e}')
        
        # _________________________________________ Database _________________________________________ #
    
    async def backup_data(self ,call):
        try:
            return await bot.answer_callback_query(call.id ,'Not Complit Src Backup DataBase !!! ',show_alert=True)
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.backup_data : {e}')
        # _________________________________________ Database _________________________________________ #
        # _________________________________________ Poshtibani _________________________________________ #
    
    async def support_db(self ,call):
        try:
            if (call.data == '#C'):
                mark = markup()
                mark.row(button('Get All Messages support_db' ,callback_data='#C_0'))
                mark.row(button('Delete All Messages support_db' ,callback_data='#CAD'))
                mark.row(button('Back' ,callback_data='Minstabot'))
                text = 'MinstaBot/support_db \n...................................\n'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
            
            elif call.data.startswith('#C_'):
                _ , id_ = call.data.split('_')
                id_ = int(id_)
                if id_ < 0 : id_ = 0 
                data = support_db.get_all()
                if not data :return await bot.answer_callback_query(call.id ,'! eadmin_id support_db message !',show_alert=True)
                if id_ > len(data)-1: id_ = len(data)-1
                msg = support_db.select_id(data[id_][0])
                mark = markup()
                mark.row(button(msg[1] , url=f'https://t.me/{msg[2]}') ,button('Veiw message' , callback_data=f'#CV_{msg[3]}'))
                mark.row(button('Answer' , callback_data=f'#CA_{data[id_][0]}'),button('Delete' , callback_data=f'#CD_{data[id_][0]}'))
                mark.row(button('Delete bot msg' ,callback_data='Minstabot_dlt'))
                mark.row(button('< Back',callback_data=f'#C_{id_-1}') ,button('Next >',callback_data=f'#C_{id_+1}'))
                return await bot.copy_message(admin_id ,setting_channel_id ,msg[3] ,reply_markup=mark)
    
            elif call.data.startswith('#CV_'):
                _ , id_ = call.data.split('_')
                id_ = int(id_)
                return await bot.forward_message(admin_id ,setting_channel_id ,id_)
    
            elif call.data.startswith('#CA_'): ########### go to minstabot ###########
                _ , rowid = call.data.split('_')
                rowid = int(rowid) 
                data = support_db.select_id(rowid)
                if not data :return await bot.answer_callback_query(call.id ,'! eadmin_id support_db message !',show_alert=True) 
                self.pm = True
                async def suport_pm(msg , data ,bmsg ,rowid):
                    await bot.delete_message(admin_id ,bmsg.id)
                    bm = await bot.copy_message(setting_channel_id ,admin_id ,msg.id ,reply_to_message_id=data[3])
                    support_db.insert_answer(admin_id ,data[0] ,bm.message_id ,data[3])
                    support_db.delete_row(rowid)
                    mark = markup()
                    mark.row(button('⭐️',callback_data='#CS_1'),
                    button('2⭐️',callback_data='#CS_2'),
                    button('3⭐️',callback_data='#CS_3'),
                    button('4⭐️',callback_data='#CS_4'),
                    button('5⭐️',callback_data='#CS_5'))
                    return await bot.copy_message(data[0] ,admin_id ,msg.id ,reply_markup=mark)
    
                
                text = 'pls send answer for user or /cancel'
                bmsg = await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                self.def_next = (suport_pm ,data ,bmsg ,rowid)
                return
                
            elif call.data.startswith('#CS_'):
                _ , i = call.data.split('_') ; i = int(i)  
                mark = markup()
                mark.row(button('⭐️'*i ,callback_data='_')) 
                return await bot.edit_message_reply_markup(call.from_user.id ,call.message.id ,reply_markup=mark)  
            
            else:
                return await bot.send_message(admin_id ,f'#Error RootMinsta.minstabot : data = {call.data}')
                
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.support_db : {e}')
        # _________________________________________ Poshtibani _________________________________________ #
        # _________________________________________ Admins _________________________________________ #

    async def admin_contorol(self ,call):
        try: 
            if (call.data == '#A'):
                mark = markup()
                mark.row(button('Admins',callback_data='#AS'))
                mark.row(button('Add Admin',callback_data='#AA'),
                button('Remove Admin',callback_data='#AR'))
                mark.row(button('Back',callback_data='Minstabot'))
                text = 'Minstabot/Admins : \n.......................................\n'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif (call.data == '#AS'):
                #await bot.answer_callback_query(call.id ,'hii mahdi',show_alert=True,url='https://t.me/MetworkBot?start=XXXX')
                mark = markup()
                for i in admin_db.admin:
                    mark.row(button(f'[{i}] = {admin_db[i]["name"]}',callback_data=f'#AS_{i}'))
                mark.row(button('Add Admin',callback_data='#AA'),button('Back',callback_data='#A'))
                text = 'Minstabot/Admins : \n.......................................\n'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif call.data.startswith('#AS_'):
                _ , id_ = call.data.split('_')
                id_ = int(id_)
                data = admin_db[id_]
                mark = markup()
                mark.row(button(f'{data["name"]} 🖊',callback_data=f'#AE${id_}$name') ,
                        button(f'{data["username"]}',url=f'https://t.me/{data["username"]}'))
                mark.row(button(f'ok [{"✅" if data["ok"] else "🚫"}]🖊',callback_data=f'#AE${id_}$ok') ,
                        button(f'day_run [ {data["day_run"]} ]🖊',callback_data=f'#AE${id_}$day_run'))
                mark.row(button(f'rejester [{"✅" if data["rejester"] else "🚫"}]🖊',callback_data=f'#AE${id_}$rejester') ,
                        button(f'poshtibani [{"✅" if data["poshtibani"] else "🚫"}]🖊',callback_data=f'#AE${id_}$poshtibani'))
                mark.row(button(f'Database [{"✅" if data["Database"] else "🚫"}]🖊',callback_data=f'#AE${id_}$Database') ,
                        button(f'Help [{"✅" if data["Help"] else "🚫"}]🖊',callback_data=f'#AE${id_}$Help'))
                mark.row(button(f'User [{"✅" if data["User"] else "🚫"}]',callback_data=f'#AE*{id_}*User') ,
                        button(f'Propaganda [{"✅" if data["Propaganda"] else "🚫"}]',callback_data=f'#AE*{id_}*Propaganda'))
    
                mark.row(button(f'Remove [{id_}]',callback_data=f'#AR_{id_}'),button('Back',callback_data='#AS'))
                text = f'Setting Admin For\n[{id_}] = {data["name"]}'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
                
            elif call.data.startswith('#AE*'):
                _ ,id_ ,mod = call.data.split('*')
                id_ = int(id_)
                data = admin_db[id_]
                mark = markup()
                if (mod == 'User'):
                    mark.row(button(f'User [{"✅" if data["User"] else "🚫"}]🖊',callback_data=f'#AE${id_}$User'))
                    mark.row(button(f'SendMessageUser [{"✅" if data["send_message_for_user"] else "🚫"}]🖊',callback_data=f'#AE${id_}$send_message_for_user'))
                    mark.row(button(f'AllSendsMessage [ {data["all_sends_message"]} ]🖊',callback_data=f'#AE${id_}$all_sends_message'))
                    mark.row(button(f'ban/undan [{"✅" if data["ban/undan"] else "🚫"}]🖊',callback_data=f'#AE${id_}$ban/undan'))
                else:
                    mark.row(button(f'Propaganda [{"✅" if data["Propaganda"] else "🚫"}]🖊',callback_data=f'#AE${id_}$Propaganda'))
                    mark.row(button(f'ForcedToJoin [{"✅" if data["Forced_to_join"] else "🚫"}]🖊',callback_data=f'#AE${id_}$Forced_to_join'))
                    mark.row(button(f'TabliqBotMsg [{"✅" if data["tabliq_bot_msg"] else "🚫"}]🖊',callback_data=f'#AE${id_}$tabliq_bot_msg'))
                    mark.row(button(f'TabSendMessage [ {data["tab_Send_Message"]} ]🖊',callback_data=f'#AE${id_}$tab_Send_Message'))
                    mark.row(button(f'TabSendMessageDay [ {data["tab_Send_Message_day"]} ]🖊',callback_data=f'#AE${id_}$tab_Send_Message_day'))
                mark.row(button(f'[{id_}] = {data["name"]} ...',callback_data=f'#AS_{id_}'))
                mark.row(button('Back',callback_data='#A'))
                text = f'Setting Admin For\n[{id_}] = {data["name"]}'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
                
            elif call.data.startswith('#AE$'):
                _ ,id_ ,mod = call.data.split('$')
                id_ = int(id_)
                data = admin_db[id_]
                if mod in ("ok" ,"rejester" ,"Database" ,"poshtibani" ,"Help" ,
                            "User" ,"send_message_for_user" ,"ban/undan" ,"Propaganda" ,"Forced_to_join" ,"tabliq_bot_msg"):
                    if data[mod]:
                        admin_db.update_self(id_ ,mod ,'0')
                    else:
                        admin_db.update_self(id_ ,mod ,'1')
                    if (mod == "ok"):call.message.reply_markup.keyboard[1][0].text= f'ok [{"✅" if data["ok"] else "🚫"}]🖊'
                    elif (mod == "rejester"):call.message.reply_markup.keyboard[2][0].text= f'rejester [{"✅" if data["rejester"] else "🚫"}]🖊'
                    elif (mod == "Database"):call.message.reply_markup.keyboard[3][0].text= f'Database [{"✅" if data["Database"] else "🚫"}]🖊'
                    elif (mod == "poshtibani"):call.message.reply_markup.keyboard[2][1].text= f'poshtibani [{"✅" if data["poshtibani"] else "🚫"}]🖊'
                    elif (mod == "Help"):call.message.reply_markup.keyboard[3][1].text= f'Help [{"✅" if data["Help"] else "🚫"}]🖊'
                    elif (mod == "User"):call.message.reply_markup.keyboard[0][0].text= f'User [{"✅" if data["User"] else "🚫"}]🖊'
                    elif (mod == "send_message_for_user"):call.message.reply_markup.keyboard[1][0].text= f'SendMessageUser [{"✅" if data["send_message_for_user"] else "🚫"}]🖊'
                    elif (mod == "ban/undan"):call.message.reply_markup.keyboard[3][0].text= f'ban/undan [{"✅" if data["ban/undan"] else "🚫"}]🖊'
                    elif (mod == "Propaganda"):call.message.reply_markup.keyboard[0][0].text= f'Propaganda [{"✅" if data["Propaganda"] else "🚫"}]🖊'
                    elif (mod == "Forced_to_join" ):call.message.reply_markup.keyboard[1][0].text= f'ForcedToJoin [{"✅" if data["Forced_to_join"] else "🚫"}]🖊'
                    elif (mod == "tabliq_bot_msg" ):call.message.reply_markup.keyboard[2][0].text= f'TabliqBotMsg [{"✅" if data["tabliq_bot_msg"] else "🚫"}]🖊'
                    return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup=call.message.reply_markup)
                else:
                    if (mod == "name"):
                        self.pm = True
                        async def set_admin_str(msg ,call ,bmsg):
                            admin_db.update_self(id_ ,mod ,msg.text)
                            await bot.delete_message(admin_id ,bmsg.id)
                            await bot.delete_message(admin_id ,msg.id)
                            call.message.reply_markup.keyboard[0][0].text= f'{msg.text} 🖊'
                            return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup=call.message.reply_markup)
                        text = f'pls send new name for set [{id_}] or /cancel'
                        bmsg = await bot.send_message(admin_id , text ,reply_markup=self.mark_cansel)
                        self.def_next = (set_admin_str ,call ,bmsg)
                        return 
                    else:
                        mark = markup()
                        mark.row(button('Reset 💢',callback_data=f'#A^{id_}^{mod}^0'))
                        mark.row(button('+1',callback_data=f'#A^{id_}^{mod}^1'),
                                button('+3',callback_data=f'#A^{id_}^{mod}^3'),
                                button('+5',callback_data=f'#A^{id_}^{mod}^5'),
                                button('+7',callback_data=f'#A^{id_}^{mod}^7'),
                                button('+10',callback_data=f'#A^{id_}^{mod}^10'))
                        mark.row(button(f'{mod}  [{data[mod]}]',callback_data='_'))
                        mark.row(button('-1',callback_data=f'#A^{id_}^{mod}^-1'),
                                button('-3',callback_data=f'#A^{id_}^{mod}^-3'),
                                button('-5',callback_data=f'#A^{id_}^{mod}^-5'),
                                button('-7',callback_data=f'#A^{id_}^{mod}^-7'),
                                button('-10',callback_data=f'#A^{id_}^{mod}^-10'))
                        if (mod == "day_run"): mark.row(button('Back',callback_data=f'#AS_{id_}'))
                        elif (mod == "all_sends_message"): mark.row(button('Back',callback_data=f'#AE*{id_}*User'))
                        elif (mod in ("tab_Send_Message" ,"tab_Send_Message_day")): mark.row(button('Back',callback_data=f'#AE*{id_}*Propaganda'))
                        return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup=mark)
    
            elif call.data.startswith('#A^'):
                _ ,id_ ,mod ,val = call.data.split('^')
                id_ = int(id_)
                data = admin_db[id_]
                if (val == '0'):
                    admin_db.update_self(id_ ,mod ,val)
                else:
                    val = int(val)
                    data[mod] += val
                    if data[mod] < 0 : data[mod] = 0
                    admin_db.update_self(id_ ,mod ,str(data[mod]))
                call.message.reply_markup.keyboard[2][0].text= f'{mod}  [ {data[mod]} ]'
                return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup=call.message.reply_markup)
                
            elif (call.data == '#AA'):           
                self.pm = True
                async def add_admin(msg,bmsg=None):
                    async def insert_admin(n):
                        admin_db.insert_admin(n.id) 
                        admin_db.update_self(n.id,option_name='name' ,data=n.first_name)
                        admin_db.update_self(n.id,option_name='username' ,data=n.username)
                        text = f'[{n.id}] : {admin_db[n.id]["name"]}'
                        mark = markup()
                        mark.row(button(text ,callback_data=f'#AS_{n.id}'))
                        mark.row(button('Back' ,callback_data='#A'))
                        await bot.delete_message(admin_id ,msg.id-1)
                        return await bot.send_message(admin_id ,text ,reply_markup=mark)
    
                    if msg.forward_from: 
                        try:
                            n = await bot.get_chat(msg.forward_from.id)
                        except :
                            self.pm = True
                            bmsg.text +='\n\nError [Not Found User] :User not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                            self.def_next = (add_admin ,bmsg)
                            await bot.delete_message(admin_id ,msg.id)
                            return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                        else:
                            if (n.type == 'private'):
                                    return await insert_admin(n)
    
                            else:
                                self.pm = True
                                bmsg.text +='\n\nError [Not Found User] :User not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                                self.def_next = (add_admin ,bmsg)
                                await bot.delete_message(admin_id ,msg.id)
                                return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                    elif msg.text.isdigit():
                        try: 
                            n = await bot.get_chat(msg.text)
                        except :
                            self.pm = True
                            bmsg.text +='\n\nError [Not Found User] :User not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                            self.def_next = (add_admin ,bmsg)
                            await bot.delete_message(admin_id ,msg.id)
                            return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                        else:
                            if (n.type == 'private'):
                               return await insert_admin(n)
    
                            else:
                                self.pm = True
                                bmsg.text +='\n\nError [Not Found User] :User not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                                self.def_next = (add_admin ,bmsg)
                                await bot.delete_message(admin_id ,msg.id)
                                return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                    else:       
                        self.pm = True
                        bmsg.text +='\n\nError [Found User] : type not private.'
                        self.def_next = (add_admin ,bmsg)
                        await bot.delete_message(admin_id ,msg.id)
                        return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)            
                    
                text = 'Pls Forward Message From User For Me For Set Admin Bot(Minstabot)\nOr Send User Int Id Or /cancel \n'
                bmsg = await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                self.def_next = (add_admin ,bmsg)
                return 
    
            elif call.data.startswith('#AR'):
                if (call.data == '#AR'):
                    mark = markup()
                    for i in admin_db.admin:
                        mark.row(button(f'[{i}] = {admin_db[i]["name"]}',callback_data=f'#AR_{i}'))
                    mark.row(button('Back',callback_data='#A'))
                    text = 'Minstabot/Admins/Remove Admin : \n.......................................\n'
                    return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)    
    
                elif call.data.startswith('#AR_'):
                    _ ,id_ = call.data.split('_')
                    id_ = int(id_)
                    mark = markup()
                    mark.row(button('Delete 🗑',callback_data=f'#AROK_{id_}'))
                    mark.row(button('Back',callback_data='#AR'))
                    text = f'Minstabot/Admins/Remove Admin : \n.......................................\n\n\n Do you want to remove this user([{id_}] = {admin_db[id_]["name"]}) from admin?'
                    return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
                elif call.data.startswith('#AROK_'):
                    _ ,id_ = call.data.split('_')
                    id_ = int(id_)
                    admin_db.del_data(id_)
                    await bot.answer_callback_query(call.id ,f'Successful operation!\nThe user({id_}) was deleted with your status.',show_alert=True)
                    call.data = '#A'
                    return await self.admin_contorol(call)
            
            else: return await bot.send_message(admin_id ,f'#Error RootMinsta.admin_contorol : data = {call.data}')
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.admin_contorol : {e}')
        
        # _________________________________________ Admins _________________________________________ #
        # _________________________________________ Tbligh _________________________________________ #

    async def callback_minsta_propaganda(self ,call):
        try: 
            def test_link(link):
                if link : return link
                else : return 'https://t.me/MetworkBot'
                
            if (call.data == '#P'):  # Minstabot_Propaganda  ++++++++++++++++++++++++++++++++
                fp = '✅' if setting.join_agbary else '❌'
                tb = '✅' if setting.tab else '❌'
                tbl = '✅' if setting.tab_inline else '❌'
                mark = markup()
                mark.row(button('Forced to join',callback_data='#PFJ'),
                            button(fp ,callback_data='#PFJ0'))
                mark.row(button('tabliq' ,callback_data='#PT'),
                            button(tb ,callback_data='#PT0'))
                mark.row(button('tabliq inline' ,callback_data='#PTL'),
                            button(tbl ,callback_data='#PTL0'))
                mark.row(button('Send Message',callback_data='#PSM'))
                mark.row(button('back',callback_data='Minstabot'))
    
                text = 'Minstabot/Propaganda \n......................................'
                await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif call.data.endswith('0'):
                if (call.data == '#PFJ0'):
                    if setting.join_agbary :
                        setting.join_agbary = 0
                        call.message.reply_markup.keyboard[0][1].text= '❌'
                    else :
                        setting.join_agbary = 1
                        call.message.reply_markup.keyboard[0][1].text= '✅'
                elif (call.data == '#PT0'):    
                    if setting.tab :
                        setting.tab = 0
                        call.message.reply_markup.keyboard[1][1].text= '❌'
                    else :
                        setting.tab = 1
                        call.message.reply_markup.keyboard[1][1].text= '✅'
                elif (call.data == '#PTL0'):
                    if setting.tab_inline :
                        setting.tab_inline = 0
                        call.message.reply_markup.keyboard[2][1].text= '❌'
                    else :
                        setting.tab_inline = 1
                        call.message.reply_markup.keyboard[2][1].text= '✅'
                return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup= call.message.reply_markup)
            # Forced to join  ++++++++++++++++++++++++++++++++
            elif (call.data == '#PFJ'):
                mark = markup()
                mark.row(button('url_join' ,url=test_link(setting.url_join)) ,button('✏️ Edit' ,callback_data='#PTEDIT$url_join'))
                mark.row(button('channel_id' ,url=test_link(setting.url_join)) ,button('✏️ Edit' ,callback_data='#PTEDIT$channel_id'))
                mark.row(button('Saves',callback_data='#PTLSA$join_agbary'),button('Update',callback_data='#PTLUP$join_agbary'))
                mark.row(button('Back',callback_data='#P'))
                text = f'''Minstabot/Propaganda/Forced to join \n......................................\n
                msg id : {setting.join_agbary_msg}\n
                "channel_id" : {setting.channel_id}\n
                "url_join" : {setting.url_join}\n'''
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            # tabliq  ++++++++++++++++++++++++++++++++ 
            elif (call.data == '#PT'):
                mark = markup()
                mark.row(button('tab_pv_text' ,url=test_link(setting.tab_pv_msg)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_pv_text'))
                mark.row(button('tab_pv_button_text' ,url=test_link(setting.tab_pv_msg)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_pv_button_text'))
                mark.row(button('tab_pv_button_url' ,url=test_link(setting.tab_pv_button_url)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_pv_button_url')) 
                mark.row(button('Saves',callback_data='#PTLSA$tab_pv') ,button('Update',callback_data='#PTLUP$tab_pv'))          
                mark.row(button('Back',callback_data='#P'))
                text = f'''Minstabot/Propaganda/Tabliq \n......................................\n
                msg ig : {setting.tab_pv_msg}\n
                "tab_pv_text" : {setting.tab_pv_text}\n
                "tab_pv_button_text" : {setting.tab_pv_button_text}\n
                "tab_pv_button_url" : {setting.tab_pv_button_url}\n'''
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
    
            # tabliq inline  ++++++++++++++++++++++++++++++++
            elif (call.data == '#PTL'):
                mark = markup()
                mark.row(button('tab_inline_img' ,url=test_link(setting.tab_inline_msg)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_inline_img'))
                mark.row(button('tab_inline_text' ,url=test_link(setting.tab_inline_msg)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_inline_text'))
                mark.row(button('tab_inline_text_button' ,url=test_link(setting.tab_inline_msg)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_inline_text_button'))
                mark.row(button('tab_inline_button_url' ,url=test_link(setting.tab_inline_msg)) ,button('✏️ Edit' ,callback_data='#PTEDIT$tab_inline_button_url'))
                mark.row(button('Saves',callback_data='#PTLSA$tab_inline'), button('Update',callback_data='#PTLUP$tab_inline'))
                mark.row(button('Back',callback_data='#P'))
                text = f'''Minstabot/Propaganda/tab_inline :\n......................................\n
                msg id : {setting.tab_inline_msg}\n
                "tab_inline_img" : {setting.tab_inline_img}\n
                "tab_inline_text" : {setting.tab_inline_text}\n
                "tab_inline_text_button" : {setting.tab_inline_text_button}
                "tab_inline_button_url" : {setting.tab_inline_button_url}'''
                await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif call.data.startswith('#PTEDIT$'):##############&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&*********************
                self.pm = True
                _ , key = call.data.split('$')
                async def edit_tab_(msg ,key):
                    if 'url' in key:
                        if not msg.text.startswith('http'):
                            self.pm = True
                            self.def_next = (edit_tab_ ,key)
                            await bot.delete_message(admin_id ,msg.id)
                            text = f'Send Value To Set "{key}" Or /cancel\n{key} = {setting[key]}'
                            text += f'\n\n Erorr [{key}]: The link entry is wrong({msg.text}), please enter a valid link.'
                            return await bot.edit_message_text(text ,admin_id ,msg.id-1 ,reply_markup=self.mark_cansel)
    
                    mark = markup()
    
                    if key.startswith('tab_inline'):
                        mark.row(button('Saves',callback_data='#PTLSA$tab_inline'),
                        button('Update',callback_data=f'#PTLUP${key}'))
                        mark.row(button('Back' ,callback_data='#PTL') ,
                        button('Delete PM' ,callback_data='Minstabot_dlt'))
                    elif key.startswith('tab_pv_'):
                        mark.row(button('Saves',callback_data='#PTLSA$tab_pv'),
                        button('Update',callback_data=f'#PTLUP${key}'))
                        mark.row(button('Back' ,callback_data='#PT') ,
                        button('Delete PM' ,callback_data='Minstabot_dlt'))
                    else:
                        mark.row(button('Saves',callback_data='#PTLSA$join_agbary'),
                        button('Update',callback_data=f'#PTLUP$join_agbary'))
                        mark.row(button('Back' ,callback_data='#PFJ') ,
                        button('Delete PM' ,callback_data='Minstabot_dlt'))
    
                    if (key == 'tab_inline_img'):
                        if msg.photo:
                            msg.text = msg.photo[0].file_id
                        else:
                            text = f'Error [tab_inline_img]: Type Not Imge\nPls Send Photo for Set Value "tab_inline_img"'
                            return await bot.send_message(admin_id ,text ,reply_markup=mark)
                        setting[key] = msg.text
                        text = f'Updated "{key}" = "{msg.text}"'
                        await bot.send_message(admin_id ,text ,reply_markup=mark)
                        return await bot.delete_message(admin_id ,msg.id-1) 
                    setting[key] = msg.text
                    text = f'Updated "{key}" = "{msg.text}"'
                    await bot.send_message(admin_id ,text ,reply_markup=mark)
                    return await bot.delete_message(admin_id ,msg.id-1) 
    
                text = f'Send Value To Set "{key}" Or /cancel\n{key} = {setting[key]}'
                self.def_next = (edit_tab_ ,key)
                return await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                
    
    
            # Send Message  ++++++++++++++++++++++++++++++++
            elif call.data in ('#PSM' ,'#PSME','#PSMF','#PSMA'):
                if call.data in ('#PSME','#PSMF','#PSMA'):
                    if (call.data == '#PSME'):
                        call.message.reply_markup.keyboard[0][0].text = 'EN User ✅'
                        call.message.reply_markup.keyboard[0][1].text = 'FA User'
                        call.message.reply_markup.keyboard[0][2].text = 'All User'
                    elif (call.data == '#PSMF'):
                        call.message.reply_markup.keyboard[0][0].text = 'EN User'
                        call.message.reply_markup.keyboard[0][1].text = 'FA User ✅'
                        call.message.reply_markup.keyboard[0][2].text = 'All User'
                    else:
                        call.message.reply_markup.keyboard[0][0].text = 'EN User'
                        call.message.reply_markup.keyboard[0][1].text = 'FA User'
                        call.message.reply_markup.keyboard[0][2].text = 'All User ✅'
                    await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup= call.message.reply_markup)
                else:
                    _ue = 'EN User ✅' if call.data == '#PSME' else 'EN User'
                    _uf = 'FA User ✅' if call.data == '#PSMF' else 'FA User'
                    _ua = 'All User ✅' if call.data not in ('#PSME','#PSMF') else 'All User'
                    m = 'A' if call.data not in ('#PSME','#PSMF') else 'E' if call.data == '#PSME' else 'F'
    
                    en_user = len(database_minsta.UserDict.get_all_user(lan='EN'))
                    fa_user = len(database_minsta.UserDict.get_all_user(lan='EN'))
                    mark = markup()
                    mark.row(button(_ue,callback_data='#PSME'),
                                button(_uf,callback_data='#PSMF'),
                                button(_ua,callback_data='#PSMA'))
                    mark.row(button(f'{en_user}',callback_data='#'),
                                button(f'{fa_user}',callback_data='#'),
                                button(f'{en_user+fa_user}',callback_data='#'))
                    mark.row(button('send message',callback_data='#USA_')) 
                    mark.row(button('Back',callback_data='#P'))
                    text = text = f'''Minstabot/Propaganda/Send Message \n
                    EN User : {en_user}
                    FA User : {fa_user}
                    All User : {en_user+fa_user}'''
                    await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif call.data in ('#PTLUP$tab_inline','#PTLUP$tab_pv' ,'#PTLUP$join_agbary'
            '#PTLUP$tab_inline_img','#PTLUP$tab_inline_text','#PTLUP$tab_inline_text_button',
            '#PTLUP$tab_inline_button_url','#PTLUP$tab_pv_text',
            '#PTLUP$tab_pv_button_text','#PTLUP$tab_pv_button_url'):
                _ , mod = call.data.split('$')
                mid = 'join_agbary' if mod.startswith('join_agbary') else 'tab_pv' if mod.startswith('tab_pv') else 'tab_inline'
                if setting[mid+'_msg'] == 'https://t.me/c/1757110357/':
                    call.message.text += '\n\n Erorr : There is no message ID to update, you must save first.'
                    call.message.reply_markup.keyboard[-2][1].text = 'Updated ❌'
                    call.message.reply_markup.keyboard[-2][1].callback_data= '_'
                    return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                    call.message.reply_markup)
    
                mark = markup()
    
                if mod == 'tab_inline':
                    mark.row(button(setting.tab_inline_text_button ,
                    url = setting.tab_inline_button_url))
                    msgid = setting.tab_inline_msg.split('/')
                    msgid = int(msgid[-1])
                    await bot.edit_message_media(types.InputMediaPhoto(setting.tab_inline_img,
                    setting.tab_inline_text ,parse_mode='HTML') ,setting_channel_id ,
                    msgid ,reply_markup=mark)
    
                elif mod == 'tab_pv':
                    mark.row(button(setting.tab_pv_button_text ,
                    url = setting.tab_pv_button_url))
                    msgid = setting.tab_inline_msg.split('/')
                    msgid = int(msgid[-1])
                    await bot.edit_message_text(setting.tab_pv_text ,setting_channel_id ,msgid ,reply_markup= mark)
    
                elif mod == 'join_agbary':
                    fp = '✅' if setting.join_agbary else '❌'
                    text = f'''Forced to join {fp}
                    "channel_id" : {setting.channel_id}\n
                    "url_join" : {setting.url_join}\n
                    '''
                    msgid = setting.join_agbary_msg.split('/')
                    msgid = int(msgid[-1])
                    await bot.edit_message_text(text ,setting_channel_id ,msgid)
    
                elif mod == 'tab_inline_img':
                    msgid = setting.tab_inline_msg.split('/')
                    msgid = int(msgid[-1])
                    await bot.edit_message_media(types.InputMediaPhoto(setting.tab_inline_img) ,setting_channel_id ,
                    msgid)
    
                elif mod == 'tab_inline_text':
                    msgid = setting.tab_inline_msg.split('/')
                    msgid = int(msgid[-1])
                    if setting.tab_inline_button_url == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_button_url]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    if setting.tab_inline_text_button == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_text_button]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    mark.row(button(setting.tab_inline_text_button ,
                    url = setting.tab_inline_button_url))                    
                    await bot.edit_message_caption(setting.tab_inline_text ,setting_channel_id ,msgid ,reply_markup=mark)
    
                elif mod == 'tab_inline_text_button':
                    msgid = setting.tab_inline_msg.split('/')
                    msgid = int(msgid[-1])
                    if setting.tab_inline_button_url == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_button_url]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    mark.row(button(setting.tab_inline_text_button ,
                    url = setting.tab_inline_button_url))
                    await bot.edit_message_reply_markup(setting_channel_id ,msgid ,reply_markup=mark)
    
                elif mod == 'tab_inline_button_url':
                    msgid = setting.tab_inline_msg.split('/')
                    msgid = int(msgid[-1])
                    if setting.tab_inline_text_button == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_text_button]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    mark.row(button(setting.tab_inline_text_button ,
                    url = setting.tab_inline_button_url))
                    await bot.edit_message_reply_markup(setting_channel_id ,msgid ,reply_markup=mark)
    
                elif mod == 'tab_pv_text':
                    msgid = setting.tab_pv_msg.split('/')
                    msgid = int(msgid[-1])
                    if setting.tab_pv_button_url == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_button_url]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    if setting.tab_pv_button_text == 'None':
                        call.message.text += '\n\n Erorr [tab_pv_button_text]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    mark.row(button(setting.tab_pv_button_text ,
                    url = setting.tab_pv_button_url))
                    await bot.edit_message_caption(setting.tab_pv_text ,setting_channel_id ,msgid ,reply_markup=mark)
    
                elif mod == 'tab_pv_button_text':
                    msgid = setting.tab_pv_msg.split('/')
                    msgid = int(msgid[-1])
                    if setting.tab_pv_button_url == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_button_url]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    mark.row(button(setting.tab_pv_button_text ,
                    url = setting.tab_pv_button_url))
                    await bot.edit_message_reply_markup(setting_channel_id ,msgid ,reply_markup=mark)
    
                elif mod == 'tab_pv_button_url':
                    msgid = setting.tab_pv_msg.split('/')
                    msgid = int(msgid[-1])
                    if setting.tab_pv_button_text == 'None':
                        call.message.text += '\n\n Erorr [tab_pv_button_text]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    mark.row(button(setting.tab_pv_button_text ,
                    url = setting.tab_pv_button_url))
                    await bot.edit_message_reply_markup(setting_channel_id ,msgid ,reply_markup=mark)
    
                else:
                    print(mod)
    
                call.message.reply_markup.keyboard[-2][1].text = 'Updated ✅'
                call.message.reply_markup.keyboard[-2][1].callback_data= None
                call.message.reply_markup.keyboard[-2][1].url = setting.tab_inline_msg 
                return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup=
                call.message.reply_markup)
    
            elif call.data in ('#PTLSA$tab_inline','#PTLSA$tab_pv' ,'#PTLSA$join_agbary'):
                _ , mod = call.data.split('$')
                mark = markup()
                if mod == 'tab_inline':
                    if setting.tab_inline_img == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_img]: No photo uploaded. Please go back to the settings and upload the photo.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    if setting.tab_inline_text == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_text]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    if setting.tab_inline_button_url == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_button_url]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    if setting.tab_inline_text_button == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_text_button]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    mark.row(button(setting.tab_inline_text_button ,
                    url = setting.tab_inline_button_url))
                    m = await bot.send_photo(setting_channel_id ,setting.tab_inline_img ,
                    setting.tab_inline_text ,parse_mode='HTML',reply_markup=mark)
                    setting.tab_inline_msg = 'https://t.me/c/1757110357/'+str(m.message_id)
                    call.message.reply_markup.keyboard[-2][0].url = setting.tab_inline_msg 
                    call.message.reply_markup.keyboard[-2][1].url = setting.tab_inline_msg 
                    
    
                elif mod == 'tab_pv':
                    if setting.tab_pv_button_text == 'None':
                        call.message.text += '\n\n Erorr [tab_pv_button_text]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    if setting.tab_pv_button_url == 'None':
                        call.message.text += '\n\n Erorr [tab_inline_button_url]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    if setting.tab_pv_text == 'None':
                        call.message.text += '\n\n Erorr [tab_pv_text]: No text entered. Please go to settings and enter the text.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    mark.row(button(setting.tab_pv_button_text ,
                    url = setting.tab_pv_button_url))
                    m = await bot.send_message(setting_channel_id ,setting.tab_pv_text,parse_mode='HTML',reply_markup=mark)
                    setting.tab_pv_msg = 'https://t.me/c/1757110357/'+str(m.message_id)
                    call.message.reply_markup.keyboard[-2][0].url = setting.tab_pv_msg
                    call.message.reply_markup.keyboard[-2][1].url = setting.tab_pv_msg
    
                elif mod == 'join_agbary':
                    if setting.url_join == 'None':
                        call.message.text += '\n\n Erorr [url_join]: The link is not entered. Please go to settings and enter the link.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
    
                    if setting.channel_id == 'None':
                        call.message.text += '\n\n Erorr [channel_id]: No channel_id entered. Please go to settings and enter the channel_id.'
                        call.message.reply_markup.keyboard[-2][0].text = 'Saves ❌'
                        call.message.reply_markup.keyboard[-2][0].callback_data= '_'
                        return await bot.edit_message_text(call.message.text ,admin_id ,call.message.id ,reply_markup=
                                        call.message.reply_markup)
                    fp = '✅' if setting.join_agbary else '❌'
                    text = f'''Forced to join {fp}
                    "channel_id" : {setting.channel_id}\n
                    "url_join" : {setting.url_join}\n
                    '''
                    m = await bot.send_message(setting_channel_id ,text)
                    setting.join_agbary_msg = 'https://t.me/c/1757110357/'+str(m.message_id)
                    call.message.reply_markup.keyboard[-2][0].url = setting.join_agbary_msg
                    call.message.reply_markup.keyboard[-2][1].url = setting.join_agbary_msg
                else:
                    print(mod)
                call.message.reply_markup.keyboard[-2][1].text = 'Updated ✅'
                call.message.reply_markup.keyboard[-2][1].callback_data= None
                call.message.reply_markup.keyboard[-2][0].text = 'Saves ✅'
                call.message.reply_markup.keyboard[-2][0].callback_data= None    
                return await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup=call.message.reply_markup)
                
            else: return await bot.send_message(admin_id ,f'#Error RootMinsta.callback_minsta_propaganda : data = {call.data}')
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.callback_minsta_propaganda : {e}')
        
        # _________________________________________ Tbligh _________________________________________ #        

        # _________________________________________ User _________________________________________ #

    async def callback_minsta_user(self ,call): 
        try:
            if call.data in ('#U','#UE','#UF','#UA') :
                if call.data in ('#UE','#UF','#UA'):
                    if (call.data == '#UE'):
                        call.message.reply_markup.keyboard[0][0].text = 'EN User ✅'
                        call.message.reply_markup.keyboard[0][1].text = 'FA User'
                        call.message.reply_markup.keyboard[0][2].text = 'All User'
                    elif (call.data == '#UF'):
                        call.message.reply_markup.keyboard[0][0].text = 'EN User'
                        call.message.reply_markup.keyboard[0][1].text = 'FA User ✅'
                        call.message.reply_markup.keyboard[0][2].text = 'All User'
                    else:
                        call.message.reply_markup.keyboard[0][0].text = 'EN User'
                        call.message.reply_markup.keyboard[0][1].text = 'FA User'
                        call.message.reply_markup.keyboard[0][2].text = 'All User ✅'
                    await bot.edit_message_reply_markup(admin_id ,call.message.id ,reply_markup= call.message.reply_markup)
                else:
                    _ue = 'EN User ✅' if call.data == '#UE' else 'EN User'
                    _uf = 'FA User ✅' if call.data == '#UF' else 'FA User'
                    _ua = 'All User ✅' if call.data not in ('#UE','#UF') else 'All User'
                    m = 'A' if call.data not in ('#UE','#UF') else 'E' if call.data == '#UE' else 'F'
    
                    en_user = len(database_minsta.UserDict.get_all_user(lan='EN'))
                    fa_user = len(database_minsta.UserDict.get_all_user(lan='FA'))
                    mark = markup()
                    mark.row(button(_ue,callback_data='#UE'),
                                button(_uf,callback_data='#UF'),
                                button(_ua,callback_data='#UA'))
                    mark.row(button(f'{en_user}',callback_data='#'),
                                button(f'{fa_user}',callback_data='#'),
                                button(f'{en_user+fa_user}',callback_data='#'))
                    mark.row(button('send message',callback_data='#USA_')) 
                    mark.row(button('send message for user ',callback_data='#')) 
                    mark.row(button('ban and unban',callback_data='#')) 
                    mark.row(button('Back',callback_data='Minstabot')) 
                    text =f'''____________________User____________________
                    EN User : {en_user}
                    FA User : {fa_user}
                    All User : {en_user+fa_user}'''
                    await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)                                   
                
            elif (call.data == '#USA_'):    # amozesh ersal pm     user send all
                self.pm = True
                async def user_send_next(msg ,*args ,**kwargs):     # amade sazi pm
                    mark = markup()
                    try:
                        text ,_ ,cod = re.split(r'(\<.)' ,msg.text ,re.DOTALL)
                    except:
                        text = msg.text
                    else:
                        try:
                            for i in re.findall(r'(\[.*\]\(.*\))',cod):
                                _ ,k ,_ ,y ,_ = re.split(r'[\[\]\(\)]' ,i)
                                mark.row(button(k,url=y),
                                button('+',callback_data=f'#U+{k}'))
                            for i in re.findall(r'\$.+',cod):
                                _,k ,v = re.split(r'[\$|\#]',i)
                                text = re.sub(k,f'<a href="{v}">{k}</a>',text)
                        except:
                            pass
                    mark.row(button('+',callback_data='#U+'))
                    mark.row(button('Send',callback_data='#USAOK') ,
                            button('Delete PM',callback_data='Minstabot_dlt'))
                    await bot.send_message(admin_id ,text ,reply_markup=mark ,parse_mode="HTML")
                    await bot.delete_message(admin_id ,msg.id)
                    await bot.delete_message(admin_id ,msg.id-1)  
    
                text =f'''Send Text For "User" or /cancel :
                <?
                Button = [text_button](link)
                Create link = $text #link
                >'''
                await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel,parse_mode=None)
                self.def_next = (user_send_next ,)
    
            elif (call.data == '#USAOK'):
                async def user_send_next_ok(text ,mark):
                    await bot.send_message(admin_id ,text ,parse_mode="HTML",reply_markup=mark)
                markup_old = call.message.reply_markup.keyboard
                mark = markup()
                for i in markup_old:
                    l = []
                    for n in i:
                        if n.url:
                            l.append(n)
                    if l:
                        mark.keyboard.append(l)           
                await user_send_next_ok(call.message.html_text ,mark)
    
            elif call.data.startswith('#U+'):
                self.pm = True
                async def new_key(msg ,mark=None ,mid=None ,key=None):
                    text , val = msg.text.split(' = ')
                    markup_ = markup()
                    for i in mark:
                        l = []
                        for n in i:
                            if n.callback_data == key:
                                c = button(text,url=val)
                                l.append(c)
                            else:
                                if n.url :
                                    l.append(n)
                        if l:
                            l.append(button('+',callback_data=f'#U+{len(markup_.keyboard)}'))
                            markup_.keyboard.append(l)
                    markup_.row(button('+',callback_data='#U+'))
                    markup_.row(button('Send',callback_data='#USAOK') ,
                            button('Delete PM',callback_data='Minstabot_dlt'))                    
                    await bot.edit_message_reply_markup(admin_id ,mid ,reply_markup=markup_)
                    await bot.delete_message(admin_id ,msg.id)
                    await bot.delete_message(admin_id ,msg.id-1) 
    
                text = 'Send "Button" Or /cancel \nKey = Link'
                await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                self.def_next = (new_key ,call.message.reply_markup.keyboard ,call.message.id ,call.data)
    
            else: return await bot.send_message(admin_id ,f'#Error RootMinsta.callback_minsta_user : data = {call.data}')
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.callback_minsta_user : {e}')
        # _________________________________________ User _________________________________________ #

        # _________________________________________ Setting _________________________________________ #
    
    async def callback_minsta_setting(self ,call):
        try:
            async def update_setting(msg=None ,bmsg_id=None ,mod=None):
                mark = markup()
                mark.row(button('Delete PM',callback_data='Minstabot_dlt'),
                            button('backe',callback_data='#S'))
                if mod == "token":
                    setting.token = msg.text
                    text =f'*Minstabot Token  updated*:\n\n{setting.token}'
                    await bot.edit_message_text(text ,admin_id ,bmsg_id ,reply_markup=mark)
                await bot.delete_message(admin_id ,msg.id)
                
            if (call.data == '#S'):
                mark = markup()
                url = setting.channelurl if setting.channelurl else 'https://t.me/c/1757110357/3'
                mark.row(button('Token',callback_data='#STS'))
                mark.row(button('Setting channel :',callback_data='#SC'),
                            button(f'{setting.setchannel}',url=url))
                mark.row(button('Help Bot',callback_data='#SH'))
                mark.row(button('Backe',callback_data='Minstabot'))
                text = '............Setting.............'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            # token
            elif (call.data == '#STS'):
                mark = markup()
                mark.row(button('Delete PM',callback_data='Minstabot_dlt'),
                            button('Edit',callback_data='#STE'),
                            button('Back',callback_data='#S'))
                text = f'Minstabot Token :\n\n{setting.token}'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            # Token_Edit
            elif (call.data == '#STE'):
                self.pm = True
                text = 'Send New "Token" Or /cancel : '
                bmsg = await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                self.def_next = (update_setting ,bmsg.id ,'token')
                return
    
    
            # Setting_channel
            elif (call.data =='#SC'):
                mark = markup()
                mark.row(button(f'{setting.setchannel}',url=f'{setting.channelurl}'),
                            button('Edit',callback_data='#SCE'))
                mark.row(button('Back',callback_data='#S')) 
                text = f'setting/channel/{setting.setchannel} :\n __________________________________'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif (call.data.startswith('#SCE')):
                self.pm = True
                async def edit_channel(msg ,bmsg):
                    if msg.forward_from_chat:
                        if msg.forward_from_chat.type == 'channel':
                            try: n = await bot.get_chat(msg.forward_from_chat.id)
                            except :
                                self.pm = True
                                bmsg.text +='\n\nError [set channel] :Channel not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                                self.def_next = (edit_channel ,bmsg)
                                await bot.delete_message(admin_id ,msg.id)
                                return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                            else:
                                if (n.type == 'channel'):
                                    if not n.invite_link :
                                        self.pm = True
                                        bmsg.text +='\n\nError [set channel] :Your bot is not an admin in this channel.'
                                        self.def_next = (edit_channel ,bmsg)
                                        await bot.delete_message(admin_id ,msg.id)
                                        return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                                    else:
                                        setting.setchannel = n.title
                                        setting.channelurl = n.invite_link
                                        setting.channelid = n.id 
                                        setting.channel_id_url = f'https://t.me/c/{str(n.id)[4:]}/'
                                        text = f'Uodated !!\n{n.title}\n{n.invite_link}\n{n.id}' 
                                        mark = markup()
                                        mark.row(button('Back' ,callback_data='#S'))
                                        await bot.delete_message(admin_id ,msg.id)
                                        return await bot.edit_message_text(text ,admin_id ,bmsg.id ,reply_markup=mark)
                                else:
                                    self.pm = True
                                    bmsg.text +='\n\nError [set channel] :Channel not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                                    self.def_next = (edit_channel ,bmsg)
                                    await bot.delete_message(admin_id ,msg.id)
                                    return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                        else:
                            self.pm = True
                            bmsg.text +='\n\nError [set channel] : type not channel.'
                            self.def_next = (edit_channel ,bmsg)
                            await bot.delete_message(admin_id ,msg.id)
                            return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
    
                    elif msg.text.isdigit():
                        id_ = int('-100'+msg.text)
                        try: n = await bot.get_chat(id_)
                        except :
                            self.pm = True
                            bmsg.text +='\n\nError [set channel] :Channel not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                            self.def_next = (edit_channel ,bmsg)
                            await bot.delete_message(admin_id ,msg.id)
                            return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                        else:
                            if (n.type == 'channel'):
                                if not n.invite_link :
                                    self.pm = True
                                    bmsg.text +='\n\nError [set channel] :Your bot is not an admin in this channel.'
                                    self.def_next = (edit_channel ,bmsg)
                                    await bot.delete_message(admin_id ,msg.id)
                                    return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                                else:
                                    setting.setchannel = n.title
                                    setting.channelurl = n.invite_link
                                    setting.channelid = n.id 
                                    setting.channel_set()
                                    text = f'Uodated !!\n{n.title}\n{n.invite_link}\n{n.id}' 
                                    mark = markup()
                                    mark.row(button('Back' ,callback_data='#S'))
                                    await bot.delete_message(admin_id ,msg.id)
                                    return await bot.edit_message_text(text ,admin_id ,bmsg.id ,reply_markup=mark)
                            else:
                                self.pm = True
                                bmsg.text +='\n\nError [set channel] :Channel not found. Probably, the bot is not a member of the channel or the sent ID is wrong.'
                                self.def_next = (edit_channel ,bmsg)
                                await bot.delete_message(admin_id ,msg.id)
                                return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)
                    else:       
                        self.pm = True
                        bmsg.text +='\n\nError [set channel] : type not channel.'
                        self.def_next = (edit_channel ,bmsg)
                        await bot.delete_message(admin_id ,msg.id)
                        return await bot.edit_message_text(bmsg.text ,admin_id ,bmsg.id ,reply_markup=bmsg.reply_markup)            
                    
    
                text = 'Pls Forward Message In Channel For Me For Set Setting Channel\nOr Send Channel Int Id Or /cancel \n'
                text += f'{setting.setchannel}\n{setting.channelurl}\n{setting.channelid}'
                bmsg = await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                self.def_next = (edit_channel ,bmsg)
                return
    
            # Help
            elif (call.data == '#SH'):
                mark = markup()
                mark.row(button('help PM',callback_data='#SHP'))
                mark.row(button('help inline',callback_data='#SHI'))
                mark.row(button('Back',callback_data='#S'))
                text = 'Setting/help func :\n......................................'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif (call.data == '#SHP'):
                mark = markup()
                comd = ('help find pro' ,'help download link' ,'help connet pag' )
                urls = [setting.channel_id_url+i for i in setting.hlp_pv]
                for i in range(3):
                    mark.row(button(comd[i],url=urls[i]),
                                button('Edit',callback_data=f'#SH$hlp_pv${i}'))
                mark.row(button('Back',callback_data='#SH'))
                text = 'Setting/help func/help pm :\n......................................'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif (call.data == '#SHI'):
                mark = markup()
                comd = ('hlp_hilghit' ,'hlp_post' ,'hlp_story' ,'hlp_find_pro')
                urls = [setting.channel_id_url+i for i in setting.hlp_inline]
                for i in range(4):
                    mark.row(button(comd[i],url=urls[i]),
                                button('Edit',callback_data=f'#SH$hlp_inline${i}'))
                mark.row(button('Back',callback_data='#SH'))
                text = 'Setting/help func/help inline :\n......................................'
                return await bot.edit_message_text(text ,admin_id ,call.message.id ,reply_markup=mark)
    
            elif (call.data.startswith('#SH$')):
                self.pm = True
                _ ,mod ,key = call.data.split('$')
                async def help_(msg ,mod ,key):
                    if (mod == 'hlp_pv'):
                        bmsg = await bot.copy_message(setting.channelid ,admin_id ,msg.id)
                        setting.hlp_pv[int(key)] = str(bmsg.message_id)
                        setting.help_set(mod ,setting.hlp_pv)
                        urls = [setting.channel_id_url+i for i in setting.hlp_pv]
                        text = f'updated [{mod}]!!\n{urls}'
                    
                    elif (mod == 'hlp_inline'):
                        bmsg = await bot.copy_message(setting.channelid ,admin_id ,msg.id)
                        setting.hlp_inline[int(key)] = str(bmsg.message_id)
                        setting.help_set(mod ,setting.hlp_inline)
                        urls = [setting.channel_id_url+i for i in setting.hlp_inline]
                        text = f'updated [{mod}]!!\n{urls}'
                    
                    else:
                        print(mod)
                    mark = markup()
                    mark.row(button('Back',callback_data='#SH'))
                    await bot.send_message(admin_id ,text ,reply_markup=mark)
                    await bot.delete_message(admin_id ,msg.id-1)
                    return await bot.delete_message(admin_id ,msg.id) 
                    
                text = f"Pls send msg for set {mod} : {key}  Or /cancel "
                self.def_next = (help_ ,mod ,key)
                return await bot.send_message(admin_id ,text ,reply_markup=self.mark_cansel)
                
        except Exception as e : return await bot.send_message(admin_id ,f'#Error RootMinsta.callback_minsta_setting : {e}')    
        # _________________________________________ Setting _________________________________________ #



