import os
#import sys
import requests
import random
from .config import (admin_id ,setting_channel_id, setting ,users_db ,
                     admin_db ,database_minsta ,
                     watch_list_db ,accounts_db ,next_msg_db,support_db ,helps_db,tablig_db) # . del #
from telebot import types
from telebot.apihelper import ApiTelegramException
from text import tx
from telebot.async_telebot import AsyncTeleBot
try:
	import instaloader
except ImportError: 
	os.system("pip3 install instaloader")
import instaloader 
from instaloader import *
from instaloader import Profile ,Post ,Story
import pickle #test
markup = types.InlineKeyboardMarkup
button = types.InlineKeyboardButton
#sys.path.insert(0, os.path.dirname(__file__))


class MainMenu:
    login_acc ={}
    def __init__(self):
        pass
    
    async def tablig_pv(self,u ,bot:AsyncTeleBot):
        try:
            mark = markup()
            mark.add(button(setting['tab_pv_button_text'], url=setting['tab_pv_button_url']))
            return await bot.send_message(u.id,setting['tab_pv_text'], reply_markup=mark) 
        except Exception as e: return await bot.send_message(admin_id ,f'tablig_pv : {e}')
   
    async def start_menu(self ,u=None ,bot:AsyncTeleBot=None ,msg:types.Message=None ,edit = False):
        try:
            if not u.lan:
                text = tx['FA']['setlan']
                mark =  markup()
                mark.add(button(text[1] ,callback_data='#LFA!') ,
                button(text[2] , callback_data='#LEN!'))
                return await bot.send_message(u.id ,text[0] ,reply_markup=mark)
            else:
                mark =  markup()
                text = tx[u.lan]['msg_start']
                mark.row(button(text[1] ,switch_inline_query_current_chat = ' '))
                mark.row(button(text[2],callback_data=f'#S'))
                if edit : return await bot.edit_message_text(text[0] ,u.id ,edit ,reply_markup=mark ,disable_web_page_preview=True)
                else: return await bot.send_message(u.id ,text[0] ,reply_markup=mark,disable_web_page_preview=True)
        except Exception as e: return await bot.send_message(admin_id ,f'start_menu : {e}')
        
    async def min_help(self ,u ,bot:AsyncTeleBot):
        text = tx[u.lan]['min_help']
        helps = setting['hlp_pv'].split(',')
        for i in helps:
            await bot.copy_message(u.id ,setting['setting_channel'] ,message_id=int(i))
        return await bot.send_message(u.id ,text)
        
    async def setting_(self ,u=None ,bot:AsyncTeleBot=None ,msg:types.Message=None  ,edit = False):
        try:
            mark =  markup()
            text = tx[u.lan]['setting']
            mark.row(button(text[1] ,callback_data='#IP')) # insta profile
            mark.row(button(text[2] ,callback_data='#W')) # watch list
            mark.row(button(text[3] ,callback_data='#P')) # poshtibai sopport
            mark.row(button(text[4] ,callback_data='#LS')) # set lan
            mark.row(button(text[5] ,callback_data='#M')) # back to mane
            if edit : return await bot.edit_message_text(text[0] ,u.id ,edit ,reply_markup=mark)
            else: return await bot.send_message(u.id ,text[0] ,reply_markup=mark,disable_web_page_preview=True)
        except Exception as e: return await bot.send_message(admin_id ,f'setting_ : {e}')

    async def set_lan(self ,u=None ,bot:AsyncTeleBot=None ,call:types.CallbackQuery=None ,edit = False):
        try:
            if call.data.endswith('!'):
                u.lan = call.data[2:4]
                return await self.start_menu(u=u ,bot=bot ,edit=edit)
            elif (call.data == '#LS'):
                text = tx[u.lan]['setlan']
                mark =  markup(row_width=2)
                l = []
                if (u.lan == "FA"): l.append(button(text[1]+'✅'   ,callback_data='#LFA'))
                else: l.append(button(text[1] ,callback_data='#LFA'))
                if (u.lan == "EN"): l.append(button(text[2]+'✅'   , callback_data='#LEN'))
                else: l.append(button(text[2] ,callback_data='#LEN'))
                mark.add(*l)
                mark.row(button('< Back' ,callback_data='#S'))
                return await bot.edit_message_text(text[0] ,u.id ,edit ,reply_markup=mark)
            else:
                l = call.data[2:]
                u.lan = l
                k = call.message.reply_markup.keyboard
                for i_ ,i in enumerate(k):
                    for v_ ,v in enumerate(k[i_]) :
                        if v.callback_data == call.data: 
                            if '✅'  in k[i_][v_].text: return 
                            k[i_][v_].text += '✅'
                        else:
                            if '✅'  in k[i_][v_].text:
                                k[i_][v_].text = k[i_][v_].text[:-1]
                mark =  markup(keyboard = k ,row_width=2)
                text = mark.to_dict()
                return await bot.edit_message_reply_markup(u.id ,edit ,reply_markup=mark) 
        except Exception as e: return await bot.send_message(admin_id ,f'set_lan : {e}')

    async def profile_(self ,u=None ,bot:AsyncTeleBot=None  ,call:types.CallbackQuery=None ,msg:types.Message=None ):
        try:
            mark = markup()
            if msg:
                acs = accounts_db.selcet_user_ac_wu(u.id) 
                if acs:
                    await bot.send_chat_action(u.id ,'typing')
                    text = tx[u.lan]['profile'][0]
                    for i in acs[-5]:
                        n = i[1]
                        n = '🔴Error' if n==0 else '🟢online' if n==1 else '⚪️offline' if n==2 else None
                        if n:
                            mark.row(button(f'{i[0]} :{n}' ,callback_data=f'#IP/{i[0]}'))
                    mark.row(button('ADD ACCOUNT', callback_data=f'#X')) # Login
                    mark.row(button('BACK' ,callback_data=f'#S')) # Back
                    if call: return await bot.edit_message_text(text[0] ,u.id ,call.message.id ,reply_markup=mark)
                    else:
                        return await bot.send_message(u.id ,text[0] ,reply_markup=mark)
                        # return await self.tablig_pv(u ,bot)
                else:
                    text = tx[u.lan]['profile'][1]
                    mark.row(button(text[1], callback_data=f'#X')) # Login
                    mark.row(button(text[2] ,callback_data=f'#S')) # Back
                    if call: return await bot.edit_message_text(text[0] ,u.id ,call.message.id ,reply_markup=mark)
                    else:
                        return await bot.send_message(u.id ,text[0] ,reply_markup=mark)
                        # return await self.tablig_pv(u ,bot)

            if (call.data =='#IP'):
                return await self.profile_(u ,bot ,call ,msg=call.message)
            
            elif (call.data =='#IP?'):
                await bot.delete_message(u.id ,call.message.id)
                return await self.profile_(u ,bot ,msg=True)

            elif call.data.startswith('#IPOF/'): # offline
                username , active= call.data.split('/')[-2:]
                await bot.answer_callback_query(call.id ,f'UPDATED ACCOUNT {active}')
                return accounts_db.update_avtive(uid=u.id ,username=username ,active=int(active))
            
            elif call.data.startswith('#IPLG'): # logout
                if call.data.startswith('#IPLGOK'):
                    username = call.data.split('/')[-1]
                    await bot.answer_callback_query(call.id ,f'EXIT ACCOUNT {username}')
                    await bot.delete_message(u.id ,call.message.id)
                    return accounts_db.update_avtive(uid=u.id ,username=username ,active=3)
                else:
                    username = call.data.split('/')[-1]
                    text = f'{username}\nDO YOU WANT EXIT THIS INSTAGRAM PAGE?'
                    mark.row(button('OKEY' ,callback_data=f'#IPLGOK/{username}'),
                             button('CANCEL' ,callback_data=f'#IP/{username}'))
                    return await bot.edit_message_caption(text ,u.id ,call.message.id ,reply_markup=mark)
            
            elif call.data.startswith('#IP/'):
                m = await bot.send_message(u.id ,'Loading . . .' )
                await bot.delete_message(u.id ,call.message.id)
                acs = call.data.split('/')[-1]
                acs = accounts_db.selcet_user_ac_one(u.id ,acs)
                if acs:
                    username , active = acs
                    L = instaloader.Instaloader()
                    L.load_session_from_file(username ,f"./database/accounts/{username}.{u.id}")
                    if not L.test_login():
                        accounts_db.update_avtive(uid=u.id ,username=username ,active=active)
                        active = 0
                    if active == 1 or active == 2:
                        pro = Profile.own_profile(L.context)
                        link = f'https://www.instagram.com/{pro.username}'
                        id_ = pro.userid
                        pablic = f'🔒Private🔒' if pro.is_private else '🔓Public🔓'
                        story = '✅' if pro.has_public_story else '❌'
                        caption = f'{pro.full_name}\n{pablic}\n{pro.biography}\nfollowers : {pro.followers}\tfolllowing : {pro.followees}'
                        mark.row(button('Instagram 🔗', url=link))
                        mark.row(button('connected ➡️', callback_data='-'),
                                    button(pro.username, callback_data='-')) 
                        mark.row(button('saved posts💾', callback_data=f'$SP/{id_}'),
                                 button('post 🌅', callback_data=f'$PS/{id_}'))
                        mark.row(button('Story 🎆', callback_data=f'$ST/{id_}'),
                                 button('igtv 📺', callback_data=f'$IG/{id_}'),
                                 button('hilight 🎇', callback_data=f'$HI/{id_}'))
                        
                        if (active == 1): 
                            mark.row(button('ONLINE 🟢', callback_data=f'#IPOF/{username}/2') ,
                                    button('logout AND EXIT ‼️', callback_data=f'#IPLG/{username}'))
                        else: 
                            mark.row(button('OFLINE 💤', callback_data=f'#IPOF/{username}/1') ,
                                    button('logout AND EXIT ‼️', callback_data=f'#IPLG/{username}'))
                            
                        mark.row(button('BACK', callback_data=f'#IP?'))
                        await bot.send_photo(u.id ,photo=pro.profile_pic_url ,
                                            caption=caption ,reply_markup=markup)
                        await self.tablig_pv(u ,bot)
                        return await bot.delete_message(u.id ,m.id)
                    else:# active == 0 
                        username = call.data.split('/')[-1]
                        text = f'{username}\nTHIS PAGE HAS BANNED INSTAGRAM\nDO YOU WANT EXIT THIS INSTAGRAM PAGE?'
                        mark.row(button('OKEY' ,callback_data=f'#IPLGOK/{username}'),
                                button('CANCEL' ,callback_data=f'#IP/{username}'))
                    return await bot.edit_message_text(text ,u.id ,call.message.id ,reply_markup=mark)
                                
        except Exception as e: return await bot.send_message(admin_id ,f'profile_ : {e}')

    async def login(self ,u=None ,bot:AsyncTeleBot=None ,msg:types.Message=None ,mode=None ,data=None):
        try:
            L = instaloader.Instaloader()
            bmsg = data['bmsg_id']
            text = tx[u.lan]['login']
            k = tx[u.lan]['login']['k']
            mark = markup()
            mark.add(button(k ,callback_data=f'#S'))
            if (mode == 'u'):
                next_msg_db.insert(uid=u.id ,mod='p' , bmsg_id=bmsg)
                return await bot.edit_message_text(text[mode] ,u.id ,bmsg ,reply_markup=mark)
            
            elif (mode == 'p'):
                next_msg_db.insert(
                    uid=u.id ,
                    mod=f'x<|>{msg.text}' ,
                    bmsg_id=bmsg)
                await bot.delete_message(u.id ,msg.id )
                t = f'<a href="https://www.instagram.com/{msg.text}/">{msg.text}</a> \n'+text[mode]
                return await bot.edit_message_text(t,u.id,bmsg ,parse_mode='html',reply_markup=mark)
            
            elif (mode == 'x'):
                username = data['mod'].split('<|>')[-1]
                password = msg.text
                await bot.delete_message(msg.from_user.id ,msg.id )
                await bot.edit_message_text('please wait . . .',u.id ,bmsg)
                try:
                    L.login(username ,password)

                except TwoFactorAuthRequiredException:
                    await bot.edit_message_text(f"{username}\n{text['c']}",u.id ,bmsg ,reply_markup=mark)
                    self.login_acc[u.id] = L
                    accounts_db.insert_into(u.id ,username ,password ,active=2)
                    return next_msg_db.insert(uid=u.id ,mod=f'c<|>{username}' , bmsg_id=bmsg)

                except InvalidArgumentException :
                    return await bot.edit_message_text('نام کاربری وجود ندارد',u.id,bmsg ,reply_markup=mark)
                    
                except BadCredentialsException :
                    return await bot.edit_message_text('رمز عبور اشتباه است',u.id,bmsg ,reply_markup=mark)     
                    
                except ConnectionException as e:
                    await bot.send_message(u.id ,e)
                    return await bot.edit_message_text('اتصال به اینستاگرام ناموفق بود لطفا بعدا تلاش کنید',u.id,bmsg ,reply_markup=mark)
                
                else:
                    L.save_session_to_file(filename=f"./database/accounts/{username}.{u.id}")
                    accounts_db.insert_into(u.id ,username ,password ,active=1)
                    u.active = 1
                    await bot.delete_message(msg.from_user.id ,msg.id)
                    return self.profile_(u)      
                
            elif (mode == 'c'):
                try:
                    username = data['mod'].split('<|>')[-1]
                    L:Instaloader = self.login_acc[u.id]
                    L.two_factor_login(msg.text)

                except InvalidArgumentException:
                    return await bot.edit_message_text(
                        'کد احرازهویتی که ارسال کردید نادرست است.دوباره  از اول تلاش کنید',u.id,bmsg ,reply_markup=mark)
                    
                else:
                    L.save_session_to_file(filename=f"./database/accounts/{username}.{u.id}")
                    accounts_db.update_avtive(u.id ,active=1)
                    u.active = 1
                    await bot.delete_message(msg.from_user.id ,msg.id)
                    return await self.profile_(u) 

        except Exception as e: return await bot.send_message(admin_id ,f'login : {e}')    

    async def watch_list(self ,u=None ,bot:AsyncTeleBot=None  ,call:types.CallbackQuery=None ,msg:types.Message=None):
        try:
            mark = markup()
            if (call.data == '#W') or msg:
                ls = watch_list_db.get_watch(u.id)
                if ls:
                    ls = ls.split('-')
                    ls =dict(map(lambda i: tuple(i.split('~')) ,ls))
                    for k , i in ls:
                        mark.add(button(k,callback_data=f'#WG{i}'))
                    mark.row(button('EDIT',callback_data='#WE'))
                    text = 'you can add 10 username in watchlist'
                else:
                    text = 'YOUR WATCH LIST IS EMPTY you can add 10 username in watchlist'
                mark.row(button('BACK',callback_data='#S'))
                if msg:
                    return await bot.send_message(u.id ,text ,reply_markup=mark)
                else:
                    return await bot.edit_message_text(text ,u.id ,call.message.id ,reply_markup=mark)

            elif (call.data == '#WE'):
                ls = watch_list_db.get_watch(u.id)
                if ls:
                    ls = ls.split('-')
                    ls =dict(map(lambda i: tuple(i.split('~')) ,ls))
                    a = 0
                    for k , i in ls:
                        mark.add(button(k+' X',callback_data=f'#WD{a}'))
                        a += 1
                    mark.row(button('BACK',callback_data='#W'))
                    text = 'you can rimove username in list'
                    return await bot.edit_message_text(text ,u.id ,call.message.id ,reply_markup=mark)

            elif call.data.startswith('#WD'):
                await bot.answer_callback_query(call.id ,'UPDATE YOUR WATCH LIST' ,show_alert=True)
                ls = watch_list_db.get_watch(u.id)
                ls = ls.split('-')
                key = int(call.data[3:])
                del ls[key]
                ls = '-'.join(ls)+'-'
                watch_list_db.edit(u.id ,watch_list=ls)
                call.data = '#WE'
                return await self.watch_list(u ,bot ,call)
            
            elif call.data.startswith('#WA/'): #WA-USERNAME~123456789
                user_id = call.data.split('/')[-1]
                ls = watch_list_db.get_watch(u.id)
                if ls and len(ls.split('-')) > 11:
                    await bot.answer_callback_query(call.id ,'ADD YOUR WATCH LIST' ,show_alert=True)
                    watch_list_db.uptoin(u.id ,user_id)
                else:
                    await bot.answer_callback_query(call.id ,
                        'YOUR WATCH LIST IS FULL WE ARE REMOVED INSEX 0 AND ADD YOUR WATCH LIST' ,show_alert=True)
                    ls = ls.split('-')
                    del ls[0]
                    ls = '-'.join(ls)+f'-{user_id}-'
                    watch_list_db.edit(u.id ,watch_list=ls)
                return
        except Exception as e :
            return await bot.send_message(admin_id ,'#ERROR Watch_list\n'+e)

    async def poshtibai(self ,u=None ,bot:AsyncTeleBot=None  ,call:types.CallbackQuery=None ,msg:types.Message=None ,data=None):
        mark = markup()
        if call:
            if (call.data == '#P'):
                mark.row(button('CANCEL AND BACK',callback_data='#S'))
                text = 'SHOMA DAR HAL ERSAL PM BE POSTIBANI HASTID'
                b = await bot.edit_message_text(text ,u.id ,call.message.id ,reply_markup=mark)
                return next_msg_db.insert( u.id,mod='#P', bmsg_id=b.message_id)
            
            elif call.data.startswith('#PS_'): #PS_rowid_scor
                _ ,rowid ,score = call.data.split('_')
                rowid ,score = int(rowid) ,int(score)
                support_db.set_score(rowid ,score)
                score = '⭐️'*score
                mark.row(button(score ,callback_data='-'))
                return await bot.edit_message_reply_markup(u.id ,message_id=call.message.id ,reply_markup=mark)
        else:
            mark.row(button('BACK' ,callback_data='#S'))
            text = 'AZ SABER VA SHAKIBAE SHOMA KHORSANDIM'
            await bot.send_message(u.id ,text ,reply_markup=mark)
            await bot.delete_message(u.id ,message_id=data['bmsg_id'])
            b = await bot.copy_message(u.id ,setting['setting_channel'] ,msg.id)
            mark = markup()
            mark.row(button('answer' ,url=f'https://t.me/MetWorkbot?start=answer_{b.message_id}'))
            await bot.edit_message_reply_markup(setting['setting_channel'] ,b.message_id ,reply_markup=mark)
            return support_db.insert(id_=u.id ,username=msg.from_user.username ,msg_id=b.message_id)
               
class Insta:
    # $SP/(saved post) $PS/(post) $ST/(story) $IG/(igtv) $HI/(hilight)
    profiles = {}
    all_acs = {'free':[]}

    def get_acc(self ,u) -> Instaloader:
        """
        select account file 
        if user has ac return user ac
        else select random ac free
        """
        if self.all_acs.get(u.id ,False): return self.all_acs[u.id]
        if u.active:
            acs = accounts_db.selcet_user_ac_wu(u.id)
            if not acs: u.active = 0
            else: 
                L = Instaloader()
                try:
                    L.load_session_from_file(acs[0] ,f"./database/accounts/{acs[0]}.{u.id}")
                    if  True: # L.test_login() #### testss #######
                        self.all_acs[u.id] = L
                        self.all_acs['free'].append(L)
                        return L
                except FileNotFoundError:
                    u.active = 0
                    accounts_db.update_avtive(u.id ,username=acs[0] ,active=0)

        if self.all_acs['free']: return random.choice(self.all_acs['free'])
        all_ac = accounts_db.select_ac()
        while True:
            try:
                username ,uid ,rowid = remove =random.choice(all_ac)
                L = Instaloader()
                try:
                    L.load_session_from_file(username ,f"database/accounts/{username}.{uid}")
                    if L.test_login(): # L.test_login() #### testss #######
                        self.all_acs['free'].append(L)
                        return L
                except FileNotFoundError:
                    accounts_db.update_avtive(rowid=rowid ,active=0)
                    all_ac.remove(remove)
            except Exception as e:
                return print(f'end accounts : {e}')
  
    def get_pro(self ,u ,profile_id:int|str) -> Profile:
        """
        :u = Telegram.User
        :profile_id = profile_id or profile_username in instagram
        :L => Instaloader => L.context  
        :return finde pro
        """
        if self.profiles.get(profile_id ,False): return self.profiles[profile_id]
        L:Instaloader = self.get_acc(u)
        if not L: return False
        try:
            if isinstance(profile_id ,int):
                pro = Profile.from_id(L.context ,profile_id)
            else:
                pro = Profile.from_username(L.context ,profile_id)
            self.profiles[pro.userid] = self.profiles[pro.username] = pro
            return pro
        except ProfileNotExistsException:
            return False

    def get_post(self ,u ,profile_id:int|str ,shortcode:str=None ,index:int=None ,range_:int=None):
        """
        :u = Telegram.User
        :profile_id = profile_id or profile_username in instagram
        :shortcode :str = get post by shortcode
        :indext :int = finde item index
        :range_ :int = Example: 5 => download post.5 to post.10
        :returns :list = post : [0 ,0 ,SELECT_ITEM ,0 ,0]
                            <OR IF Slider>
                          post: [0 ,0 ,[SELECT_ITEM ,SELECT_ITEM ,...] ,0 ,0]
                            <OR IF range_ TRUE>
                        posts: [ITEM ,ITEM ,...]
        """
        if shortcode:
            L:Instaloader = self.get_acc(u)
            post = Post.from_shortcode(L.context ,shortcode)
            if (post.typename == 'GraphSidecar'):
                sl = []
                for node in post.get_sidecar_nodes():
                   sl.append(node)
                return sl
            else:
                return post
            
        data = []        
        profile:Profile = self.get_pro(u , profile_id)
        if range_ or (range_ == 0):
            for post in profile.get_posts():
                if range_: range_ -= 1;continue
                if (post.typename == 'GraphSidecar'):
                    sl = [post]
                    for node in post.get_sidecar_nodes():
                        sl.append(node)
                    data.append(sl)
                else:
                    data.append(post)
                if len(data) == 5:
                    return data

        page ,item = divmod(index,5)
        page = page*5
        for post in profile.get_posts():
            if page: page -= 1;continue
            if item == len(data)-1:
                if (post.typename == 'GraphSidecar'):
                    sl = [post]
                    for node in post.get_sidecar_nodes():
                        sl.append(node)
                    data.append(sl)
                else:
                    data.append(post)
            else:
                data.append(0)

        return data
        
    def get_story(self ,u ,profile_id:int ,index:int=0 ,all_:bool=None):
        """
        :u = Telegram.User
        :profile_id = instagram int id
        :indext :int = finde item index
        :all_ :bool = if you want downloads all items ?
        :returns :dict = {'cont': 0 => How much is the add items?
                        'items': [0 ,0 ,[SELECT_ITEM] ,0 ,0]
                            <OR IF ALL TRUE>
                        'items': [ITEM ,ITEM ,...]
                         } 
        """
        L:Instaloader= self.get_acc(u)
        data = {}
        page ,item = divmod(index,5)
        page = page*5
        for storys in L.get_stories([profile_id]):
            data['cont'] = storys.itemcount
            data['items'] = []
            if all_:
                for items in storys:
                    if items.is_video:
                        media = requests.get(items.video_url)
                        data['items'].append(types.InputMediaVideo(media.content))
                    else:
                        media = requests.get(items.url)
                        data['items'].append(types.InputMediaPhoto(media.content))
                return data
            
            for items in storys:
                if page: page -= 1;continue
                if item == len(data['items'])-1:
                    if items.is_video:
                        media = requests.get(items.video_url)
                        data['items'].append([types.InputMediaVideo(media.content)])
                    else:
                        media = requests.get(items.url)
                        data['items'].append([types.InputMediaPhoto(media.content)])
                else:
                    data['items'].append(0)
                if len(data['items']) == 5:
                    break
        return data

    def get_saved_post(self ,u ,profile_id:str=None ,index:int=None ,range_:int=None):
        """
        :u = Telegram.User
        :profile_id :int
        :url :str = get post by url link
        :indext :int = finde item index
        :range_ :int = Example: 5 => download post.5 to post.10
        :returns :dict = [0 ,0 ,[SELECT_ITEM] ,0 ,0]
                            <OR IF range_ TRUE>
                         [ITEM ,ITEM ,...]
                         } 
        """
        data = []
        pro:Profile = self.get_pro(u ,profile_id)
        saved_post = pro.get_saved_posts()
        if range_ or (range_ == 0):
            for post in saved_post():
                if range_: range_ -= 1;continue
                if (post.typename == 'GraphSidecar'):
                    sl = []
                    for node in post.get_sidecar_nodes():
                        sl.append(node)
                    data.append(sl)
                else:
                    data.append(post)
                if len(data) == 5:
                    return data

        page ,item = divmod(index,5)
        page = page*5
        for post in saved_post:
            if page: page -= 1;continue
            if item == len(data)-1:
                if (post.typename == 'GraphSidecar'):
                    sl = []
                    for node in post.get_sidecar_nodes():
                        sl.append(node)
                    data.append(sl)
                else:
                    data.append(post)
            else:
                    data.append(0)
        return data

    def get_hilight(self ,u ,profile_id:int ,index:int=0 ,index2:int=0 ,
                    get_cover:bool=None ,get_item:bool=None ,all_:bool=None):
        """
        :u = Telegram.User
        :profile_id = instagram int id
        :L => Instaloader => L.context  
        :indext :int = finde cover item index in hilight
        :indext2 :int = finde item index in hilight gurop
        :get_cover :bool = get covers hilight
        :get_item :bool = get items this caver
        :all_ :bool = if you want downloads all items this caver?
        :returns :dict = {'cover': [CAVER ,CAVER ,[SELECT_CAVER] 
                                                    ,CAVER ,CAVER]
        <OR IF get_item TRUE>   
        :returns :dict = {'cover': [CAVER ,CAVER ,[SELECT_CAVER] 
                                                    ,CAVER ,CAVER]                                         
                        'items': [ITEM ,ITEM ,[SELECT_ITEM] 
                                                    ,ITEM ,ITEM]
                            <OR IF ALL TRUE>
                        'items': [ITEM ,TEM ,...]
        """
        data = {}
        L:Instaloader = self.get_acc(u) 
        hilight = L.get_highlights(profile_id)
        
        def get_hilight_cover(index:int=None):
            data['cover'] = []
            page ,item = divmod(index,5)
            page = page*5
            for cover in hilight:
                if page: page -= 1;continue
                if item == len(data['cover'])-1:
                    data['cover'].append([cover])
                else:
                    data['cover'].append(cover)
                if len(data['cover']) == 5:
                    break
            return data
        
        def get_hilight_item(index:int ,index2:int ,all_:bool=None):
            get_hilight_cover(index)
            data['items'] = []
            page ,item = divmod(index2,5)
            page = page*5
            for cover in data['cover']:
                if not isinstance(cover ,list): continue
                for items in cover[0].get_items():
                    if all_:
                        data['items'].append(items)
                    else:
                        if page: page -= 1;continue
                        if item == len(data['cover'])-1:
                            data['items'].append(items)
                        else:
                            data['items'].append(0)
                        if len(data['items']) == 5:
                            break
            return data

        if get_cover: return get_hilight_cover(index)
        if get_item:return get_hilight_item(index ,index2,all_=all_)

    def get_igtv(self ,u ,profile_id:Profile=None ,L:Instaloader=None ,index:int=None ): # type: ignore
        """
        :u = Telegram.User
        :profile_id = profile_id or profile_username in instagram
        :L => Instaloader => L.context  
        :url :str = get igtv by url link
        :indext :int = finde item index
        :returns :dict = {'igtv': [0 ,0 ,[SELECT_ITEM] ,0 ,0]
                         } 
                         <OR URL>
                         {'igtv': [ITEM]
                         } 
        igtv.thumbnail_url
        igtv.url
        """
        data = []
        
        profile:Profile = self.get_pro(u , profile_id) 
        page ,item = divmod(index,5)
        page = page*5
        for igtv in profile.get_igtv_posts():
            if page: page -= 1;continue
            if item == len(data)-1:
                data.append(igtv)
            else:
                data.append(0)
            if len(data) == 5:
                    break
        return data

class MenuInsta(Insta):
    inline_data = {}
    # $SP/(saved post) $PS/(post) $ST/(story) $IG/(igtv) $HI/(hilight)

    async def tabpm(self ,u ,bot:AsyncTeleBot):
        if setting['tab_pv']:
            return await bot.copy_message(
                chat_id=u.id ,
                from_chat_id = setting['setting_channel'] ,
                message_id = tablig_db['pv_msg_id'] ,
                reply_markup = markup().row(button(tablig_db['bt_text'] ,url=tablig_db['bt_url'])))
        return

    # msg.text.startswhit(@)    
    async def find_pro(self ,u=None ,bot:AsyncTeleBot=None  ,msg:types.Message=None ,profile_id:int=None):
        try:
            b = await bot.send_message(u.id ,text='[Finding Profile ...]' ,reply_to_message_id=msg.id)
            #text = tx[u.lan]['find_pro']
            if profile_id: pro = self.get_pro(u ,profile_id)         
            else: pro = self.get_pro(u ,msg.text[1:])

            if not pro:
                return await bot.edit_message_text('[Profile not found !]' ,u.id ,b.message_id)
            mark = markup()
            link = f'https://www.instagram.com/{pro.username}'
            pablic = f'🔒Private🔒' if pro.is_private else '🔓Public🔓'
            caption = f'{pro.full_name}\n\t{pablic}\n[followers {pro.followers}]\t[folllowing {pro.followees}]\n\n{pro.biography}'
            profile_id = pro.userid
            mark.row(button(pro.username+' 🔗', url=link))
            mark.row(button(f'Story 🎆{"✅"if pro.has_public_story else "❌"}', callback_data=f'$ST/{profile_id}'),
                        button(f'post 🌅{pro.mediacount}', callback_data=f'$PS/{profile_id}'))
            mark.row(button(f'igtv 📺{pro.igtvcount}', callback_data=f'$IG/{profile_id}'),
                        button(f'hilight 🎇{"✅"if pro.has_highlight_reels else "❌"}', callback_data=f'$HI/{profile_id}'))
            mark.row(button('📂 add Your watchlist 👀', callback_data=f'#WA/{pro.username}~{pro.userid}'))
            await bot.send_photo(u.id ,pro.profile_pic_url ,caption ,reply_markup=mark ,reply_to_message_id=msg.id)
            await self.tabpm(u ,bot)
            return await bot.delete_message(u.id ,b.message_id)
        except Exception as e:
            return await bot.send_message(admin_id ,e)
        
    # '$PS/{profile_id}' OR '$PS/{profile_id}/{index}'
    async def menu_post(self ,u ,bot:AsyncTeleBot ,call:types.CallbackQuery):
        call_data = call.data.split("/")
        mark = markup()

        # '$PS/{profile_id}' or '$PS/{profile_id}/{index}'
        if len(call_data) == 2 or len(call_data) == 3:
            s = True if len(call_data) == 2 else False
            if s: profile_id = int(call_data[-1]) ;index = 0
            else: profile_id ,index = map(int ,call_data[1:])
            if s: b = await bot.send_message(u.id ,text='[Downloading Post ...]' ,reply_to_message_id=call.message.id)
            else: await bot.edit_message_caption('[Downloading Post Please Wit...]' ,u.id ,call.message.id)
            posts = self.get_post(u ,profile_id ,index=index)
            
            if not posts: 
                if s: return await bot.edit_message_text('[Not Post In Profile For Download Or Page is Private]' ,u.id ,b.message_id)
                else: return await bot.edit_message_caption('[Not Post In Profile For Download]' ,u.id ,call.message.id)
            n ,_ = divmod(index,5)
            n = n*5
            row_1 = []
            if n >= 5: row_1.append(button('<<' ,callback_data=f'$PS/{profile_id}/{n-5}'))
            for post in posts:
                if post:
                    callback_data = f'$PS/{profile_id}/{n}'
                    if isinstance(post ,list): item:Post = post[0]
                    else: item:Post = post
                    row_1.append(button(f"[{n+1}]" ,callback_data='_'))
                else: row_1.append(button(f"{n+1}" ,callback_data=f'$PS/{profile_id}/{n}'))
                n += 1
            if len(row_1) == 5: row_1.append(button('>>' ,callback_data=f'$PS/{profile_id}/{n+1}'))
            mark.row(*row_1)
            if len(item.caption) > 200: mark.row(button('SEE CAPTION' ,callback_data=callback_data+'/PC'))
            if (item.typename == 'GraphSidecar'): mark.row(button('[DOWNLOAD ALL SLIDE]' ,callback_data=callback_data+'/DS'))
            mark.row(button('DOWNLOAD ALL' ,callback_data=f'$PS/{profile_id}/A/{index}'))
            mark.row(button('PROFILE' ,url=f"tg://openmessage?user_id={setting['bid']}&message_id={call.message.id}"))
            if not s:
                mark.keyboard[-1] = call.message.reply_markup.keyboard[-1]
            caption = f'{item.likes} ❤️     {item.comments} 💬\n_______________________\n{item.caption[:200]}'
            if s:
                if  item.is_video: media = item.video_url
                else: media = item.url
            else:
                if  item.is_video: media = types.InputMediaVideo(requests.get(item.video_url).content)
                else: media = types.InputMediaPhoto(requests.get(item.url).content)
                
            if s:
                if item.is_video: await bot.send_video(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                else: await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
            else: return await bot.edit_message_media(media ,u.id ,call.message.id ,reply_markup=mark)
                 
        # f'$PS/{profile_id}/A/{range}' or '$PS/{profile_id}/{index}' + '/PC' | '/DS'
        elif len(call_data) == 4:
            if (call_data[2] == 'A'):# download all post
                profile_id , range_ = int(call_data[1]) ,int(call_data[3])
                if range_: await bot.delete_message(u.id ,call.message.id)
                b = await bot.send_message(u.id ,text='[Downloading Post ...]' ,reply_to_message_id=call.message.id)
                posts = self.get_post(u ,profile_id ,range_=range_)
                if not posts: return await bot.edit_message_text('[Not Post In Profile For Download]' ,u.id ,b.message_id)
                for item in posts:
                    if isinstance(item ,list):
                        medias = []
                        caption = f'{item[0].owner_username}\n{item[0].likes} ❤️     {item[0].comments} 💬\n_______________________\n{item[0].caption[:200]}'
                        for it in item:
                            if it.is_video:
                                media = requests.get(it.video_url)
                                media = types.InputMediaVideo(media.content)
                            else:
                                media = requests.get(it.url) # it.display_url
                                media = types.InputMediaPhoto(media.content)
                            medias.append(media)
                        await bot.send_media_group(u.id ,medias)
                        continue
                    caption = f'{item.owner_username}\n{item.likes} ❤️     {item.comments} 💬\n_______________________\n{item.caption[:200]}'
                    if  item.is_video:
                        media = requests.get(item.video_url)
                        media = types.InputMediaVideo(media.content)
                        await bot.send_video(u.id ,media ,caption=caption)
                    else: 
                        media = requests.get(item.url)
                        media = types.InputMediaPhoto(media.content)
                        await bot.send_photo(u.id ,media ,caption=caption)
                await self.tabpm(u ,bot)
                mark.row(button('+' ,callback_data=f'$PS/{profile_id}/A/{range_+5}'))
                await bot.send_message(u.id ,'[Download More ...]' ,reply_markup=mark)
                return await bot.delete_message(u.id ,b.message_id)
                    
            elif (call_data[3] == 'PC'):# post caption
                profile_id , index = int(call_data[1]) ,int(call_data[2])
                b = await bot.send_message(u.id ,text='[Load Caption Post ...]' ,reply_to_message_id=call.message.id)
                posts = self.get_post(u ,profile_id ,index=index)
                if not posts: return await bot.edit_message_text('[Not Post In Profile For Get CAption]' ,u.id ,b.message_id)
                for post in posts:
                    if post:
                        cap = post.caption
                        break
                if cap: await bot.send_message(u.id ,cap ,reply_to_message_id=call.message.id) ;await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)

            elif (call_data[3] == 'DS'):# download slider
                profile_id , index = int(call_data[1]) ,int(call_data[2])
                b = await bot.send_message(u.id ,text='[Downloading Slides ...]' ,reply_to_message_id=call.message.id)
                posts = self.get_post(u ,profile_id ,index=index)
                if not posts: return await bot.edit_message_text('[Not Post Slider In Profile For Download]' ,u.id ,b.message_id)
                medias = []
                for post in posts:
                    if post and isinstance(post ,list):
                        caption = f'{post[0].owner_username}\n{post[0].likes} ❤️     {post[0].comments} 💬\n_______________________\n{post[0].caption[:200]}'
                        for item in post:
                            if it.is_video:
                                media = requests.get(it.video_url)
                                media = types.InputMediaVideo(media.content ,caption=caption)
                            else:
                                media = requests.get(it.url) # it.display_url
                                media = types.InputMediaPhoto(media.content ,caption=caption)
                            medias.append(media)
                        break
                if medias: await bot.send_media_group(u.id ,medias ,reply_to_message_id=call.message.id) ;await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
    
    #  '$ST/{profile_id}' OR '$ST/{profile_id}/{index}' OR  f'$PS/{profile_id}/A/0'
    async def menu_story(self ,u ,bot:AsyncTeleBot ,call:types.CallbackQuery):
        call_data = call.data.split("/")
        mark = markup()
        
        # '$ST/{profile_id}' or '$ST/{profile_id}/{index}'
        if len(call_data) == 2 or len(call_data) == 3:
            s = True if len(call_data) == 2 else False
            if s: profile_id = int(call_data[-1]) ;index = 0
            else: profile_id ,index = map(int ,call_data[1:])
            
            if s: b = await bot.send_message(u.id ,text='[Downloading story ...]' ,reply_to_message_id=call.message.id)
            else: await bot.edit_message_caption('[Downloading story ...]' ,u.id ,call.message.id)

            storys = self.get_story(u ,profile_id ,index=index)
            if not storys['items']: 
                if s: return await bot.edit_message_text('[Not Story In Profile For Download]' ,u.id ,b.message_id)
                else: return await bot.edit_message_text('[Not Story In Profile For Download]' ,u.id ,call.message.id)

            n ,_ = divmod(index,5)
            n = n*5
            row_1 = []
            if n >= 5: row_1.append(button('<<' ,callback_data=f'$ST/{profile_id}/{n-5}'))
            for story in storys['items']:
                if story:
                    item = story 
                    row_1.append(button(f"[{n+1}]" ,callback_data='_'))
                else: row_1.append(button(f"{n+1}" ,callback_data=f'$ST/{profile_id}/{n}'))
                n += 1
            if n > storys['cont']: row_1.append(button('>>' ,callback_data=f'$ST/{profile_id}/{n+1}'))
            mark.row(*row_1)
            mark.row(button('DOWNLOAD ALL' ,callback_data=f'$ST/{profile_id}/A/{index}'))
            mark.row(button('PROFILE' ,url=f"tg://openmessage?user_id={setting['bid']}&message_id={call.message.id}"))
            if not s:
                mark.keyboard[-1] = call.message.reply_markup.keyboard[-1]

            caption = f'Story 🎆 : {storys["cont"]}\n{item.owner_username} \n{item.date}\n.'      
            if  item.is_video: media = types.InputMediaVideo(requests.get(item.video_url).content)
            else: media = types.InputMediaPhoto(requests.get(item.url).content)
                
            if s:
                if item.is_video: await bot.send_video(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                else: await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
            else: return await bot.edit_message_media(media ,u.id ,call.message.id ,reply_markup=mark)

        # f'$ST/{profile_id}/A/0'
        elif len(call_data) == 4:
            profile_id = int(call_data[1])
            b = await bot.send_message(u.id ,text='[Downloading story ...]' ,reply_to_message_id=call.message.id)
            storys = self.get_story(u ,profile_id ,all_=True)
            if not storys['items']: return await bot.edit_message_text('[Not Story In Profile For Download]' ,u.id ,b.message_id)
            medias = []
            for item in storys['items']:
                caption = f'Story 🎆 : {storys["cont"]}\n{item.owner_username} \n{item.date}\n.'
                if  item.is_video:
                    media = requests.get(item.video_url)
                    media = types.InputMediaVideo(media.content ,caption)
                    
                else:
                    media = requests.get(item.url)
                    media = types.InputMediaPhoto(media.content ,caption)
                medias.append(media)
                if len(medias) == 5:
                    await bot.send_media_group(u.id ,medias ,reply_to_message_id=call.message.id)
                    medias = []

            if medias: await bot.send_media_group(u.id ,medias ,reply_to_message_id=call.message.id)
            await self.tabpm(u ,bot)
            return await bot.delete_message(u.id ,b.message_id)

    # f'$SP/{profile_id}' OR '$SP/{profile_id}/{index}' OR f'$SP/{profile_id}/A/0'
    async def menu_saved_post(self ,u ,bot:AsyncTeleBot ,call:types.CallbackQuery):
        call_data = call.data.split("/")
        mark = markup()

        # '$SP/{profile_id}' or '$SP/{profile_id}/{index}'
        if len(call_data) == 2 or len(call_data) == 3:
            s = True if len(call_data) == 2 else False
            if s: profile_id = int(call_data[-1]) ;index = 0
            else: profile_id ,index = map(int ,call_data[1:])

            if s: b = await bot.send_message(u.id ,text='[Downloading Saved Post ...]' ,reply_to_message_id=call.message.id)
            else: await bot.edit_message_caption('[Downloading Post Please Wit...]' ,u.id ,call.message.id)
            posts = self.get_saved_post(u ,profile_id ,index=index)
            if not posts: 
                if s: return await bot.edit_message_text('[Not Saved Post In Profile For Download]' ,u.id ,b.message_id)
                else: return await bot.edit_message_caption('[Not Post In Profile For Download]' ,u.id ,call.message.id)
            n ,_ = divmod(index,5)
            n = n*5
            row_1 = []
            if n >= 5: row_1.append(button('<<' ,callback_data=f'$SP/{profile_id}/{n-5}'))
            for post in posts:
                if post:
                    callback_data = f'$SP/{profile_id}/{n}'
                    if isinstance(post ,list): item:Post = post[0]
                    else: item:Post = post
                    row_1.append(button(f"[{n+1}]" ,callback_data='_'))
                else: row_1.append(button(f"{n+1}" ,callback_data=f'$SP/{profile_id}/{n}'))
                n += 1
            if len(row_1) == 5: row_1.append(button('>>' ,callback_data=f'$SP/{profile_id}/{n+1}'))
            mark.row(*row_1)
            if len(item.caption) > 200: mark.row(button('SEE CAPTION' ,callback_data=callback_data+'/PC'))
            if (item.typename == 'GraphSidecar'): mark.row(button('[DOWNLOAD ALL SLIDE]' ,callback_data=callback_data+'/DS'))
            mark.row(button('DOWNLOAD ALL' ,callback_data=f'$SP/{profile_id}/A/{index}'))
            mark.row(button('PROFILE' ,url=f"tg://openmessage?user_id={setting['bid']}&message_id={call.message.id}"))
            if not s:
                mark.keyboard[-1] = call.message.reply_markup.keyboard[-1]
            caption = f'saved posts💾:\n{item.likes} ❤️     {item.comments} 💬\n_______________________\n{item.caption[:200]}'

            if  item.is_video: media = types.InputMediaVideo(requests.get(item.video_url).content)
            else: media = types.InputMediaPhoto(requests.get(item.url).content)
                
            if s:
                if item.is_video: await bot.send_video(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                else: await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
            else: return await bot.edit_message_media(media ,u.id ,call.message.id ,reply_markup=mark)
        
        # f'$SP/{profile_id}/A/{range}' or '$SP/{profile_id}/{index}' + '/PC' | '/DS'
        elif len(call_data) == 4:
            if (call_data[2] == 'A'):# download all post
                profile_id , range_ = int(call_data[1]) ,int(call_data[3])
                if range_: await bot.delete_message(u.id ,call.message.id)
                b = await bot.send_message(u.id ,text='[Downloading Post ...]' ,reply_to_message_id=call.message.id)
                posts = self.get_post(u ,profile_id ,range_=range_)
                if not posts: return await bot.edit_message_text('[Not Post In Profile For Download]' ,u.id ,b.message_id)
                for item in posts:
                    if isinstance(item ,list):
                        medias = []
                        caption = f'saved posts💾:{item[0].owner_username}\n{item[0].likes} ❤️     {item[0].comments} 💬\n_______________________\n{item[0].caption[:200]}'
                        for it in item:
                            if it.is_video:
                                media = requests.get(it.video_url)
                                media = types.InputMediaVideo(media.content)
                            else:
                                media = requests.get(it.url) # it.display_url
                                media = types.InputMediaPhoto(media.content)
                            medias.append(media)
                        await bot.send_media_group(u.id ,medias)
                        continue
                    caption = f'saved posts💾:{item.owner_username}\n{item.likes} ❤️     {item.comments} 💬\n_______________________\n{item.caption[:200]}'
                    if  item.is_video:
                        media = requests.get(item.video_url)
                        media = types.InputMediaVideo(media.content)
                        await bot.send_video(u.id ,media ,caption=caption)
                    else: 
                        media = requests.get(item.url)
                        media = types.InputMediaPhoto(media.content)
                        await bot.send_photo(u.id ,media ,caption=caption)
                await self.tabpm(u ,bot)
                mark.row(button('+' ,callback_data=f'$SP/{profile_id}/A/{range_+5}'))
                await bot.send_message(u.id ,'[Download More ...]' ,reply_markup=mark)
                return await bot.delete_message(u.id ,b.message_id)
                    
            elif (call_data[3] == 'PC'):# post caption
                profile_id , index = int(call_data[1]) ,int(call_data[2])
                b = await bot.send_message(u.id ,text='[Load Caption Post ...]' ,reply_to_message_id=call.message.id)
                posts = self.get_post(u ,profile_id ,index=index)
                if not posts: return await bot.edit_message_text('[Not Post In Profile For Get CAption]' ,u.id ,b.message_id)
                for post in posts:
                    if post:
                        cap = post.caption
                        break
                if cap: await bot.send_message(u.id ,cap ,reply_to_message_id=call.message.id) ;await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)

            elif (call_data[3] == 'DS'):# download slider
                profile_id , index = int(call_data[1]) ,int(call_data[2])
                b = await bot.send_message(u.id ,text='[Downloading Slides ...]' ,reply_to_message_id=call.message.id)
                posts = self.get_post(u ,profile_id ,index=index)
                if not posts: return await bot.edit_message_text('[Not Post Slider In Profile For Download]' ,u.id ,b.message_id)
                medias = []
                for post in posts:
                    if post and isinstance(post ,list):
                        caption = f'saved posts💾:{post[0].owner_username}\n{post[0].likes} ❤️     {post[0].comments} 💬\n_______________________\n{post[0].caption[:200]}'
                        for item in post:
                            if it.is_video:
                                media = requests.get(it.video_url)
                                media = types.InputMediaVideo(media.content ,caption=caption)
                            else:
                                media = requests.get(it.url) # it.display_url
                                media = types.InputMediaPhoto(media.content ,caption=caption)
                            medias.append(media)
                        break
                if medias: await bot.send_media_group(u.id ,medias ,reply_to_message_id=call.message.id) ;await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
  
    #  '$HI/{profile_id}' 
    async def menu_hilight(self ,u ,bot:AsyncTeleBot ,call:types.CallbackQuery):
        call_data = call.data.split("/")
        mark = markup()

        # '$HI/{profile_id}' or '$SP/{profile_id}/{index}'
        if len(call_data) == 2 or len(call_data) == 3:
            s = True if len(call_data) == 2 else False
            if s: profile_id = int(call_data[-1]) ;index = 0
            else: profile_id ,index = map(int ,call_data[1:])

            if s: b = await bot.send_message(u.id ,text='[Downloading Hilight ...]' ,reply_to_message_id=call.message.id)
            else: await bot.edit_message_caption('[Downloading Hilight Please Wit...]' ,u.id ,call.message.id)

            hilight = self.get_hilight(u ,profile_id ,index=index ,get_cover=True)
            if not hilight['cover']:
                if s: return await bot.edit_message_text('[Not Hilight In Profile For Download]' ,u.id ,b.message_id)
                else: return await bot.edit_message_caption('[Not Hilight In Profile For Download]' ,u.id ,call.message.id)

            n ,_ = divmod(index,5)
            n = n*5
            row_1 = []
            if n >= 5: row_1.append(button('<<' ,callback_data=f'$HI/{profile_id}/{n-5}'))
            for cover in hilight['cover']:
                if isinstance(cover ,list):
                    callback_data = f'$HI/{profile_id}/{n}'
                    item_cover:Highlight= cover[0]
                    row_1.append(button(f"[{item_cover.title}]" ,callback_data='_'))
                else: row_1.append(button(f"{cover.title}" ,callback_data=f'$HI/{profile_id}/{n}'))
                n += 1
            itemcount = item_cover.itemcount    
            if len(row_1) == 5: row_1.append(button('>>' ,callback_data=f'$HI/{profile_id}/{n+1}'))
            mark.row(*row_1)
            mark.row(button(f'[SEE ALL SLIDE ({itemcount})]' ,callback_data=callback_data+'/DS'))
            mark.row(button(f'[DOWNLOAD ALL SLIDE ({itemcount})]' ,callback_data=f'$HI/{profile_id}/{index}/A/0'))
            mark.row(button('PROFILE' ,url=f"tg://openmessage?user_id={setting['bid']}&message_id={call.message.id}"))
            if not s:
                mark.keyboard[-1] = call.message.reply_markup.keyboard[-1]

            caption = f'hilight 🎇 :\n{item_cover.owner_username}\n{item_cover.title}\n[{item_cover.last_seen_utc}]'
            media = requests.get(item_cover.cover_url)
            media = types.InputMediaPhoto(media.content)
            if s:
                await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
            else: return await bot.edit_message_media(media ,u.id ,call.message.id ,reply_markup=mark) 

        # '$HI/{profile_id}/{index}/{index2}'
        elif len(call_data) == 4:
            profile_id , index , index2= map(int ,call_data[1:])
            await bot.edit_message_caption('[Downloading Hilight Please Wit...]' ,u.id ,call.message.id)
            hilight = self.get_hilight(u ,profile_id ,index=index ,index2=0 ,get_item=True)
            if not hilight['cover']: return await bot.edit_message_caption('[Not Hilight In Profile For Download]' ,u.id ,call.message.id)
            
            item_cover:Highlight = [cover[0] for cover in hilight['cover'] if isinstance(cover ,list)][0]
            n ,_ = divmod(index2,5)
            n = n*5
            row_2 = []
            if n >= 5: row_2.append(button('<<' ,callback_data=f'$HI/{profile_id}/{index}/{n-5}'))
            for item in hilight['items']:
                if item:
                    callback_data = f'$HI/{profile_id}/{index}/{n}'
                    item:StoryItem = item
                    row_2.append(button(f"[{n+1}]" ,callback_data='_'))
                else: row_2.append(button(f"{n+1}" ,callback_data=f'$HI/{profile_id}/{index}/{n}'))
                n += 1
            if len(row_2) == 5: row_2.append(button('>>' ,callback_data=f'$HI/{profile_id}/{index}/{n+1}'))
            mark = call.message.reply_markup
            mark.keyboard[1] = row_2
            caption = f'hilight 🎇 :\n{item_cover.owner_username}\n{item_cover.title}\n[{item_cover.last_seen_utc}]\nitem [{index2+1}]\n[{item.date}]'

            if item.is_video: media = types.InputMediaVideo(requests.get(item.video_url).content ,caption)
            else: media = types.InputMediaPhoto(requests.get(item.url).content ,caption)
            return await bot.edit_message_media(media ,u.id ,call.message.id ,reply_markup=mark) 

        # f'$HI/{profile_id}/{index}/A'
        elif len(call_data) == 5:
            profile_id = int(call_data[1])
            b = await bot.send_message(u.id ,text='[Downloading Hilight ...]' ,reply_to_message_id=call.message.id)
            hilight = self.get_hilight(u ,profile_id ,index=index,all_=True)
            if not hilight['items']: return await bot.edit_message_text('[Not Hilight In Profile For Download]' ,u.id ,b.message_id)
            cover:Highlight = [cover[0] for cover in hilight['cover'] if isinstance(cover ,list)][0]
            title = cover.title
            medias = []
            for item in hilight['items']:
                caption = f'hilight 🎇 : {title}\n{item.owner_username} \n[{item.date}]\n.'
                if  item.is_video:
                    media = requests.get(item.video_url)
                    media = types.InputMediaVideo(media.content ,caption)
                    
                else:
                    media = requests.get(item.url)
                    media = types.InputMediaPhoto(media.content ,caption)
                medias.append(media)
                if len(medias) == 5:
                    await bot.send_media_group(u.id ,medias ,reply_to_message_id=call.message.id)
                    medias = []
            if medias: await bot.send_media_group(u.id ,medias ,reply_to_message_id=call.message.id)
            await self.tabpm(u ,bot)
            return await bot.delete_message(u.id ,b.message_id)

    #  '$IG/{profile_id}'
    async def menu_igtv(self ,u ,bot:AsyncTeleBot ,call:types.CallbackQuery):
        call_data = call.data.split("/")
        mark = markup()

        # '$IG/{profile_id}' '$IG/{profile_id}/{index}' 
        if len(call_data) == 2 or len(call_data) == 3:
            s = True if len(call_data) == 2 else False
            if s: profile_id = int(call_data[-1]) ;index = 0
            else: profile_id ,index = map(int ,call_data[1:])

            if s: b = await bot.send_message(u.id ,text='[Downloading Post ...]' ,reply_to_message_id=call.message.id)
            else: await bot.edit_message_caption('[Downloading Post Please Wit...]' ,u.id ,call.message.id)

            igtvs = self.get_igtv(u ,profile_id ,index=index)
            if not igtvs: 
                if s: return await bot.edit_message_text('[Not Post In Profile For Download]' ,u.id ,b.message_id)
                else: return await bot.edit_message_caption('[Not Post In Profile For Download]' ,u.id ,call.message.id)
            n ,_ = divmod(index,5)
            n = n*5
            row_1 = []
            if n >= 5: row_1.append(button('<<' ,callback_data=f'$PS/{profile_id}/{n-5}'))
            for igtv in igtvs:
                if igtv:
                    item:Post = igtv
                    row_1.append(button(f"[{n+1}]" ,callback_data='_'))
                else: row_1.append(button(f"{n+1}" ,callback_data=f'$PS/{profile_id}/{n}'))
                n += 1
            if len(row_1) == 5: row_1.append(button('>>' ,callback_data=f'$PS/{profile_id}/{n+1}'))
            mark.row(*row_1)
            mark.row(button('DOWNLOAD' ,callback_data=f'$PS/{profile_id}/{index}/D'))
            mark.row(button('PROFILE' ,url=f"tg://openmessage?user_id={setting['bid']}&message_id={call.message.id}")) 
            if not s:
                mark.keyboard[-1] = call.message.reply_markup.keyboard[-1]

            caption = f'{item.likes} ❤️     {item.comments} 💬\n[Time : {igtv.video_duration}]\n_______________________\n{item.caption[:200]}'
            media = types.InputMediaPhoto(requests.get(item.url).content ,caption)
            if s: 
                await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=call.message.id)
                await self.tabpm(u ,bot)
                return await bot.delete_message(u.id ,b.message_id)
            else: return await bot.edit_message_media(media ,u.id ,call.message.id ,reply_markup=mark)

        # '$IG/{profile_id}/{index}/D'
        if len(call_data) == 4:
            profile_id ,index = map(int ,call_data[1:-1])
            b = await bot.send_message(u.id ,text='[Downloading Post ...]' ,reply_to_message_id=call.message.id)
            igtv = self.get_igtv(u ,profile_id ,index=index)
            if not igtvs: return await bot.edit_message_text('[Not Post In Profile For Download]' ,u.id ,b.message_id)
            igtv:Post = [i for i in igtv if i][0]

            caption = f'{igtv.likes} ❤️     {igtv.comments} 💬\n[Views : {igtv.video_view_count}]\n[Time : {igtv.video_duration}]'
            media = types.InputMediaVideo(requests.get(igtv.video_url).content ,caption)
            mark.row(button('See igtvs' ,url=f"tg://openmessage?user_id={setting['bid']}&message_id={call.message.id}"))
            mark.row(call.message.reply_markup.keyboard[-1][0])
            s = await bot.send_video(u.id ,media ,reply_markup=mark)
            caption = igtv.caption
            return await bot.send_message(u.id ,caption ,reply_to_message_id=s.message_id)

    # https://www.instagram.com/[tv OR p]/{short_code} <OR> /start  [IG or PS]/{short_code} 
    async def menu_shortcode(self ,u=None ,bot:AsyncTeleBot=None  ,msg:types.Message=None):
        b = await bot.send_message(u.id ,text='[Downloading Post Please Wit...]' ,reply_to_message_id=msg.id)
        shortcode = msg.text.split('/')[-1]
        post:Post = self.get_post(u ,shortcode=shortcode)
        if not post: return await bot.edit_message_text('[Not Post In Profile For Download]' ,u.id ,b.message_id)
        mark = markup()
        if isinstance(post ,list):
            medias = []
            caption = f'{post[0].owner_username}\n{post[0].likes} ❤️     {post[0].comments} 💬'
            for it in post:
                if it.is_video: media = types.InputMediaVideo(requests.get(it.video_url).content ,caption=caption)
                else: media = types.InputMediaPhoto(requests.get(it.url).content ,caption=caption)
                medias.append(media)
            bmsg = await bot.send_media_group(u.id ,medias ,reply_to_message_id=msg.id)
            caption = post[0].caption
            mark.row(button('SEE PROFILE' ,callback_data=f'$PR/{post[0].owner_id}'))
        else:
            caption = f'{post.owner_username}\n{post[0].likes} ❤️     {post.comments} 💬'
            if  post.is_video:
                media = types.InputMediaVideo(requests.get(post.video_url).content)
                bmsg = await bot.send_video(u.id ,media ,caption=caption ,reply_to_message_id=msg.id)
            else:
                media = types.InputMediaPhoto(requests.get(post.url).content)
                bmsg = await bot.send_photo(u.id ,media ,caption=caption ,reply_to_message_id=msg.id)
            caption = post.caption
            mark.row(button('SEE PROFILE' ,callback_data=f'#PRO/{post.owner_id}'))
        await bot.send_message(u.id ,caption ,reply_markup=mark ,reply_to_message_id=bmsg.message_id)
        return await bot.delete_message(u.id ,b.message_id)

    # /start  ST/{profile_id}/{index}    
    async def command_story(self ,u ,bot:AsyncTeleBot=None  ,msg:types.Message=None ):
        profile_id ,index = map(int ,msg.text.split('/')[-2:])
        b = await bot.send_message(u.id ,text='[Downloading story ...]' ,reply_to_message_id=msg.id)
        storys = self.get_story(u ,profile_id ,index=index)
        if not storys['items']: 
            return await bot.edit_message_text('[Not Story In Profile For Download]' ,u.id ,b.message_id)
        item:StoryItem = [item for item in storys['items'] if item][0]
        mark = markup()
        mark.row(button('SEE PROFILE' ,callback_data=f'$PR/{item.owner_id}'))
        caption = f'Story 🎆 : {storys["cont"]}\n{item.owner_username} \n{item.date}\n.'      
        if  item.is_video: media = types.InputMediaVideo(requests.get(item.video_url).content)
        else: media = types.InputMediaPhoto(requests.get(item.url).content)
        if item.is_video: await bot.send_video(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=msg.id)
        else: await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=msg.id)
        await self.tabpm(u ,bot)
        return await bot.delete_message(u.id ,b.message_id)

    # /start  HI/{profile_id}/{index}/{index}
    async def command_hilight(self ,u ,bot:AsyncTeleBot=None  ,msg:types.Message=None ):
        data = msg.text.split('/')
        if len(data) == 5: profile_id ,index ,index2 = map(int ,msg.text.split('/')[-3:])
        else: profile_id ,index = map(int ,msg.text.split('/')[-2:]) ;index2=None
        mark = markup()

        if index2 is None:
            b = await bot.send_message(u.id ,text='[Downloading Hilight ...]' ,reply_to_message_id=msg.id)
            hilight = self.get_hilight(u ,profile_id ,index=index ,get_cover=True)
            if not hilight['cover']:
                return await bot.edit_message_text('[Not Hilight In Profile For Download]' ,u.id ,b.message_id)

            item_cover:Highlight= [i for i in hilight['cover'] if isinstance(i ,list)][0]
            itemcount = item_cover.itemcount 
            mark.row(button(f'[DOWNLOAD ALL SLIDE ({itemcount})]' ,callback_data=f'$HI/{profile_id}/{index}/A/0'))
            mark.row(button('SEE PROFILE' ,callback_data=f'$PR/{item_cover.owner_id}'))

            caption = f'hilight 🎇 :\n{item_cover.owner_username}\n{item_cover.title}\n[{item_cover.last_seen_utc}]'
            media = types.InputMediaPhoto(requests.get(item_cover.cover_url).content)
            await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=msg.id)
            await self.tabpm(u ,bot)
            return await bot.delete_message(u.id ,b.message_id)
        
        else:
            b = await bot.send_message(u.id ,text='[Downloading Hilight ...]' ,reply_to_message_id=msg.id)
            hilight = self.get_hilight(u ,profile_id ,index=index ,index2=0 ,get_item=True)
            if not hilight['cover']: return await bot.edit_message_caption('[Not Hilight In Profile For Download]' ,u.id ,b.message_id)
            item_cover:Highlight = [cover[0] for cover in hilight['cover'] if isinstance(cover ,list)][0]
            item:StoryItem = [i for i in hilight['items'] if i][0]
            caption = f'hilight 🎇 :\n{item_cover.owner_username}\n{item_cover.title}\n[{item_cover.last_seen_utc}]\nitem [{index2+1}]\n[{item.date}]'
            mark.row(button('SEE PROFILE' ,callback_data=f'$PR/{item_cover.owner_id}'))
            if item.is_video: 
                media = types.InputMediaVideo(requests.get(item.video_url).content ,caption)
                await bot.send_video(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=msg.id)
            else: 
                media = types.InputMediaPhoto(requests.get(item.url).content ,caption)
                await bot.send_photo(u.id ,media ,caption=caption ,reply_markup=mark ,reply_to_message_id=msg.id)
            await self.tabpm(u ,bot)
            return await bot.delete_message(u.id ,b.message_id)
    
    # inline sho tab
    async def inline_tab(self ,bot:AsyncTeleBot ,inline_query:types.InlineQuery):
        if self.inline_data.get('tab_inline'):pass
        else: self.inline_data['tab_inline'] = tablig_db.get_value('tab_inline')

        if self.inline_data.get('tab_inline_button'):pass
        else: 
            d = self.inline_data['tab_inline']
            self.inline_data['tab_inline_button']# = mark
    
    # @minstabot
    async def inline_help_pro(self ,bot:AsyncTeleBot ,inline_query:types.InlineQuery):pass
    
    # @minstabot {username}/p/
    async def inline_help_post(self ,bot:AsyncTeleBot ,inline_query:types.InlineQuery):pass
    
    # @minstabot {username}/s/
    async def inline_help_story(self ,bot:AsyncTeleBot ,inline_query:types.InlineQuery):pass
    
    # @minstabot {username}/h/
    async def inline_help_hilight(self ,bot:AsyncTeleBot ,inline_query:types.InlineQuery):pass
 
    # @minstabot {username}/
    async def inline_profile(self ,u ,bot:AsyncTeleBot ,inline_query:types.InlineQuery ,data):pass
    
    # @minstabot {username}/p/{index}/
    async def inline_post(self ,u ,bot:AsyncTeleBot ,inline_query:types.InlineQuery ,data):pass
    
    # @minstabot {username}/s/{index}/
    async def inline_story(self ,u ,bot:AsyncTeleBot ,inline_query:types.InlineQuery ,data):pass
    
    # @minstabot {username}/h/{index}/ <or> @minstabot {username}/h/{index}/{index2}
    async def inline_hilight(self ,u ,bot:AsyncTeleBot ,inline_query:types.InlineQuery ,data ,item=False):pass