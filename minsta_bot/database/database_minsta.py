import os
from time import time
try:
    import mysql.connector as sql
except:
    os.system('python -m pip install mysql-connector')
    os.system('python -m pip install wheel')
    os.system('python -m pip install mysql-connector-python')
finally:
    import mysql.connector as sql
import secrets
import random

from telebot import TeleBot
from .. import config as CF
bot = TeleBot(CF.adimin_bot_token,threaded=False)
RUNFUNC = True # for creat tabel and set value
connect = lambda : sql.connect(user=CF.db_user,password=CF.db_password,host=CF.db_host,database=CF.db_database)  #test

def cur(commit:bool=False ,fetchall:bool=False ,fetchone:bool=False ,execute:str=None):
    '''
    Query In DataBase
    '''
    conn = connect()
    try:
        
        cur_ = conn.cursor()
        cur_.execute(execute)
        if commit:
            val = True
            conn.commit()
        elif fetchall:
            val = cur_.fetchall()
        elif fetchone:
            val = cur_.fetchone()
    except Exception as e:
        #print(e)
        bot.send_message(CF.admin_id ,f"{execute}\n#Error minsta DataBase : {e}")
        conn.rollback()
        val = False
    conn.close()
    return val

################################################################################
### Setting
################################################################################
class Setting:
    '''
    setting minstabot
    load data setting => MinstaDataBase.db => table setting
    '''
    d = ('token' ,'join_agbary_msg' ,
            'join_agbary' ,'channel_id' ,
            'tab_pv' ,'tab_inline',
            'hlp_pv' ,'hlp_inline' ,
            'setting_channel','unlimited','day')

    def __init__(self) -> None:
        self.setting = {}
        if RUNFUNC: return self.creat_table()

    def __repr__(self) -> str: return repr(self.setting)

    def __getitem__(self, key):
        if self.setting.get(key ,False): return self.setting[key]
        else: 
            val =cur(fetchall=True 
            ,execute=f'SELECT option_name,option_data FROM setting WHERE 1') # option_name="{key}"
            self.setting = dict(val)
            if self.setting.get(key ,False): return self.setting[key]
            else:
                cur(commit=True 
                ,execute=f"""INSERT INTO setting(option_name) VALUES('{key}') 
                ON DUPLICATE KEY UPDATE option_name = '{key}';""")
                self.setting[key] = 0
                return 0

    def __setitem__(self, key, item):
        self[key]
        cur(commit=True 
            ,execute=f"""UPDATE setting SET option_data = '{item}' where option_name = '{key}';""")
        self.setting[key] = item
        return

    def creat_table(self):
        cur(commit=True ,
        execute='''CREATE TABLE IF NOT EXISTS `setting` (
            `option_name` TEXT(30) NOT NULL , 
            `option_data` TEXT(100) NULL , 
            PRIMARY KEY (`option_name`(15))) ENGINE = InnoDB;''')
        return 
           
################################################################################
### Admin
################################################################################    
class Admin:
    '''
    admin minstabot
    load data admin => MinstaDataBase.db => table admin
    '''
    def __init__(self) -> None:
        self.admin = set()
        self.DATA = {}
        if RUNFUNC: self.creat_table()

    def __repr__(self): return repr(self.DATA) 

    def __iter__(self): return iter(self.DATA)

    def __setitem__(self, key, item):
        if isinstance(key,str):
            if key.isdigit():
                key = int(key)
        self.DATA[key] = item
        self.admin.add(key)
        return self.insert_init(key ,item)

    def __getitem__(self, key):
        try:
            return self.DATA[key]
        except:
            return 0

    def __delitem__(self, key):# Delete item as => Table admin
        self.admin.remove(key)
        self.del_data(key)
        del self.DATA[key]
        return

    def creat_table(self):# creat_table admin
        cur(commit=True ,
        execute="""CREATE TABLE IF NOT EXISTS admin(
                            id INT,
                            option_name TEXT,
                            option_data TEXT)
                            ENGINE = InnoDB CHARSET=utf8 COLLATE utf8_persian_ci;""")
        return

    def insert_admin(self ,id_):# INSERT INTO admin(id ,option_name)
        val = cur(fetchall=True ,
            execute=f'SELECT option_data FROM {self.table} where id = {id_}')
        if val: return 0
        setting_admin =("name" ,"username","ok" ,"day_run" ,"rejester" ,"Database" ,"poshtibani" ,"Help" ,
        "User" ,"all_sends_message" ,"send_message_for_user" ,"ban/undan" ,"Propaganda" ,"Forced_to_join" ,"tabliq_bot_msg" ,
        "tab_Send_Message" ,"tab_Send_Message_day")
        for i in setting_admin:
            cur(commit=True ,execute=f"INSERT INTO admin(id ,option_name) VALUES ({id_},'{i}');")
        self.set_value()
        return

    def set_value(self):# set value in class from => Table admin
        val = cur(fetchall=True ,
        execute=f'SELECT id,option_name,option_data FROM admin')
        if val:
            for i in val:
                self.admin.add(i[0])
                self.DATA.setdefault(i[0] ,{})
                self.DATA[i[0]][i[1]] = i[2] if not i[2].isdigit() else int(i[2])
        return
        
    def update_self(self,id_:int,option_name:str ,data:str=0):# Update admin from => table admin
        cur(commit=True ,
        execute=f"""UPDATE admin SET option_data = '{data}' where id = {id_} AND option_name = '{option_name}' ;""")
        self.DATA[id_][option_name] = data if not data.isdigit() else int(data)
        return

    def del_data(self ,key):# delete row from admin => Table admin
        cur(commit=True ,
        execute="DELETE FROM admin WHERE id={key};")
        del self.DATA[key] 
        self.admin.remove(key)
        return   
       
    def data(self ,arg1=None,arg2=None,arg3=None):# excpet handelr for self.DATA => class admin 
        if arg3:
            try:
                return self.DATA[arg1][arg2][arg3]
            except:
                return 0
        if arg2:
            try:
                return self.DATA[arg1][arg2]
            except:
                return 0
        if arg1:
            try:
                return self.DATA[arg1]
            except:
                return 0
        return self.DATA

################################################################################
### Watch List
################################################################################
class WatchList:
    '''
    insta_id = username,insta_id - username,insta_id >len(10)
    '''
    def __init__(self):
        if RUNFUNC: self.creat_table()

    def creat_table(self):# creat_Table WatchList
        cur(commit=True ,
            execute="""
            CREATE TABLE IF NOT EXISTS CREATE TABLE `watchlist` (
                `uid` BIGINT(20) NOT NULL ,
                `watch` TEXT(400) NULL , 
                PRIMARY KEY (`uid`)) ENGINE = InnoDB; """)
        return
    
    def uptoin(self ,uid ,insta_username_id):  # 'username~id -'
        watch = f'{insta_username_id}-'
        return cur(commit=True ,
            execute=f"""INSERT INTO `watchlist`(`uid` ,`watch`) 
            VALUES ({uid} ,'{watch}') 
            ON DUPLICATE KEY UPDATE `watch`= IF(`watch` LIKE '%{watch}%' ,`watch`,CONCAT(`watch`,'{watch}'))
            ;""")
    
    def get_watch(self ,uid):
        return cur(fetchone=True ,
            execute=f"""SELECT `watch` FROM `watchlist` WHERE `uid`={uid};""")[0]
    
    def edit(self ,uid ,watch_list):
        return cur(commit=True ,
            execute=f"""UPDATE `watchlist` SET `watch`={watch_list} WHERE `uid`={uid};""")

################################################################################
### Accounts Instagram
################################################################################
class Accounts:
    '''
    Instagram Accounts mangers

    active mode:
        0 = ban insta;
        1 = online;
        2 = offline;
        3 = Exit;
        5 = Error;
    '''
    def __init__(self):
        if RUNFUNC: self.creat_table()

    def creat_table(self):# creat_Table Accounts 
        cur(commit=True ,
            execute="""
            CREATE TABLE IF NOT EXISTS `accounts` (
                `rowid` INT(7) NOT NULL AUTO_INCREMENT , 
                `uid` BIGINT(20) NOT NULL , 
                `username` TEXT(50) NULL , 
                `password` TEXT(50) NULL , 
                `active` INT(1) NULL , 
                PRIMARY KEY (`rowid`), 
                INDEX `uid` (`uid`) ,
                UNIQUE `username` (`username`)) ENGINE = InnoDB;""")
        return
    
    def insert_into(self ,uid:int ,username:str ,password:str ,active:int):
        return cur(commit=True ,
            execute=f"""INSERT INTO accounts(`uid`,`username`,`password`,`active`)
            VALUES ({uid} ,'{username}' ,'{password}' ,{active});""")
        
    def selcet_user_ac_wu(self ,uid:int):
        return cur(fetchall=True ,
            execute=f"""SELECT usename,active FROM accounts 
            WHERE uid = {uid};""")
    
    def selcet_user_ac_one(self ,uid:int ,username:str):
        return cur(fetchone=True ,
            execute=f"""SELECT usename FROM accounts 
            WHERE uid = {uid} AND usename={username};""")

    def select_rand_user_ac(self ,uid:int):
        val = cur(fetchall=True ,
            execute=f"""SELECT username,active FROM accounts 
            WHERE uid = {uid} AND active = 1 ;""")
        return random.choice(val)

    def select_ac(self):
        return cur(fetchall=True ,
            execute=f"""SELECT username,uid,rowid FROM accounts WHERE active = 1 or active = 2 or active = 3;""")

    def update_avtive(self ,uid:int=None ,rowid:int=None ,username:int=None ,active:int=None):
        if uid:
            return cur(commit=True ,
            execute=f"""UPDATE TABLE accounts active = {active} WHERE uid = {uid} AND username={username}""")
        else:
            return cur(commit=True ,
            execute=f"""UPDATE TABLE accounts active = {active} WHERE rowid = {rowid}""")
            
################################################################################
### UserDict deque whit maxlen
################################################################################
class UserDict:
    '''
    dict for load online user
    User Info
    load User Info => database => Table User
    '''
    def __init__(self, maxlen = 200):
        self.data = {}
        self.maxlen = maxlen
        if RUNFUNC: self.creat_table()
        
    def __len__(self): return len(self.data)
    
    def __repr__(self): return repr(self.data)

    def __iter__(self): return iter(self.data)

    def __setitem__(self, key, item):
        self.lenmax()
        self.data[key] = item

    def __getitem__(self, key):
        try: return self.data[key]
        except: return self.load_user(key)
      
    def lenmax(self):
        if self.maxlen :
            if self.maxlen == len(self.data):           
                for i in self.data.keys():
                    self.data.pop(i)
                    return
                return    
            return
        return

    def creat_table(self):# creat_Table Users & Info_User in 
        cur(commit=True ,
        execute="""CREATE TABLE IF NOT EXISTS `users` (
            `uid` BIGINT(20) NOT NULL , 
            `lan` TEXT(3) , 
            `invite` INT(7) DEFAULT '0' , 
            `active` INT(1) DEFAULT '0' , 
            `try` INT(3) UNSIGNED DEFAULT '4' , 
            PRIMARY KEY (`uid`)) ENGINE = InnoDB;""")
        return

    @staticmethod
    def update(key ,item ,uid):# update Users from => Table Users
        print(key ,item ,uid)
        if isinstance(item ,str):
            cur(commit=True ,execute=f"""UPDATE users SET {key} = '{item}' where `uid` = "{uid}";""")
        else:
            cur(commit=True ,execute=f"""UPDATE users SET {key} = {item} where `uid` = "{uid}";""")
        return 

    def insert_users(self ,uid : int ):# insert user from => Table Users
        cur(commit=True ,execute=f"""INSERT INTO `users`(`uid`) VALUES ({uid})""")
        t = (uid ,0 ,0 ,0 ,4)
        u = UserRead(*t)
        self[uid] = u
        return u
        
    def load_user(self ,uid):# get values from => Table Users
        user = cur(fetchone=True ,
            execute=f"""SELECT `uid`,`lan`,`invite`,`active`,`try` FROM `users` WHERE `uid`='{uid}'""")
        if not user: return self.insert_users(uid)
        u = UserRead(*user)
        self[uid] = u
        return u

    @staticmethod
    def get_all_user(lan = None):# selct user from => Table Users
        if lan: 
            return cur(fetchall=True ,
                execute=f"select `uid`,`lan` from `users` WHERE `lan` = '{lan}';")
        else: return cur(fetchall=True ,execute="select `uid`,`lan` from `users`;")
          
################################################################################
### UserRead
################################################################################
class UserRead:
    '''
    read user data => database => minstabot_user_db.db => Table User
    '''
    def __init__(self ,id_ ,lan ,invite ,active ,_try) -> None:
        self.__dict__['insta'] = None
        self.__dict__['com'] = None
        self.__dict__['id']= id_
        self.__dict__['lan'] = lan
        self.__dict__['invite'] = invite
        self.__dict__['active'] = active
        self.__dict__['_try'] = _try


    def __repr__(self): return repr(self.id)

    def __eq__(self, o): return self.id == o

    def __setitem__(self, key, item): 
        self.__dict__[key] = item 
        if key in ('lan','invite','active','try'):
            if self.__dict__[key] :return UserDict.update(key ,item ,self.id)
            else: return
        else: self.__dict__[key] = item

    def __setattr__(self, __name: str, __value): return self.__setitem__(__name ,__value)
        
################################################################################
### Support
################################################################################
class Support:
    '''
    Support minstabot
    load data Support => MinstaDataBase.db => table Support
    '''
    def __init__(self) -> None:
        self.data = set()
        if RUNFUNC: self.creat_table()

    def creat_table(self):# creat_table Support AND Answer in 
        cur(commit=True ,
            execute='''
            CREATE TABLE IF NOT EXISTS `support` (
                `rowid` INT(3) NOT NULL AUTO_INCREMENT , 
                `uid` BIGINT(20) NOT NULL , 
                `uesrname` TEXT(20) NOT NULL , 
                `msg_ig` INT(6) NOT NULL , 
                PRIMARY KEY (`row_id`)) ENGINE = InnoDB;''')
        cur(commit=True ,
            execute='''
            CREATE TABLE IF NOT EXISTS `answer` (
                `rowid` INT(3) NOT NULL AUTO_INCREMENT , 
                `aid` BIGINT(20) NOT NULL , 
                `uid` BIGINT(20) NOT NULL , 
                `a_msg_id` INT(6) NOT NULL , 
                `u_msg_id` INT(6) NOT NULL , 
                `score` INT(1) NOT NULL , 
                PRIMARY KEY (`row_id`)) ENGINE = InnoDB;''')
        return

    def insert(self ,uid ,username ,msg_id):# Insert qustion in Table Support  
        cur(commit=True ,
            execute=f"INSERT INTO `support`(`uid`,`uesrname`,`msg_ig`) VALUES ({uid},'{username}',{msg_id});")
        return

    def insert_answer(self ,aid ,uid ,a_msg_id ,u_msg_id):# Insert Answer in Table Answer 
        cur(commit=True ,
            execute=f"""INSERT INTO `answer`(`aid` ,`uid` ,`a_msg_id` ,`u_msg_id`) 
            VALUES ({aid},{uid},{a_msg_id},{u_msg_id});""")
        return

    def get_all(self):# Select all Requst in Table Support
        return cur(fetchall=True ,
            execute=f'SELECT `rowid` FROM `support`;')
        

    def select_id(self ,rowid):# Select all Requst in Table Support
        return cur(fetchone=True ,
            execute=f'SELECT id ,name ,username ,msg_id FROM `support` WHERE `rowid` = {rowid};')
    
    def delete_row(self ,rowid):# Delete Requst in Table Support
        cur(commit=True ,
            execute=f'DELETE FROM `support` WHERE `rowid` = {rowid};')
        return

    def set_score(self ,rowid ,score):# Delete Requst in Table Support
        cur(commit=True ,
            execute=f"""UPDATE `answer` SET `score`={score} WHERE `rowid` = {rowid};""")
        return
    
################################################################################
### NextPm
################################################################################
class NextPm:
    '''
    next msg(pm) handeller
    '''
    def __init__(self ,end_time:int=600) -> None:
        if RUNFUNC: self.run()
        self.data = {}
        self.end_time = end_time
        self.select_bot()
        self.del_auto()
        return 
        
    def __getitem__(self, uid): return self.data.get(uid ,False)

    def Table(self):
        cur(commit=True ,
        execute=f"""CREATE TABLE IF NOT EXISTS `nextpm` (`rowid` INT NOT NULL AUTO_INCREMENT ,
                                                                `uid` BIGINT(15) NOT NULL ,
                                                                `mod` TEXT NOT NULL ,
                                                                `bmsg_id` INT(10) NOT NULL ,
                                                                `time` BIGINT(15) NOT NULL , 
                                                                PRIMARY KEY (`rowid`)
                                                                ) ENGINE = InnoDB;""")
        return 

    def select_bot(self):
        val = cur(fetchall=True ,
        execute=f"SELECT `uid`, `mod`, `bmsg_id` FROM `nextpm`;")
        for i in val:
                self.data[i[0]] = {'mod':i[1] ,'bmsg_id':i[2]}
        return

    def delete_pm(self ,uid):
        val = cur(commit=True ,
        execute=f"DELETE FROM nextpm WHERE uid={uid};")
        if self.data.get(uid ,False) and val : del self.data[uid]
        return

    def insert(self ,uid:int ,mod:str ,bmsg_id:int):
        tend = int(time())
        val = cur(commit=True ,
            execute=f"""INSERT INTO `nextpm`(`uid`, `mod`, `bmsg_id`, `time`) 
                VALUES ({uid} ,'{mod}' ,{bmsg_id} ,{tend});""")
        if val: self.data[uid] = {'mod':mod ,'bmsg_id':bmsg_id}
        return

    def del_auto(self):
        tend = int(time()-self.end_time)
        return cur(commit=True ,
        execute=f"""DELETE FROM `nextpm` WHERE `time` <{tend};""")

    def run(self):
        self.Table()
        return

################################################################################
### Tabliq
################################################################################
class Tabliq:

    def __init__(self) -> None:
            if RUNFUNC: return self.creat_table()

    def __repr__(self): return repr(self.tab)

    def creat_table(self):
        cur(commit=True ,
        execute=''' CREATE TABLE IF NOT EXISTS `tabliq` (
            `name` TEXT(10) UNSIGNED NOT NULL AUTO_INCREMENT ,
            `text` TEXT(400) NULL DEFAULT NULL ,
            `button` TEXT(400) NULL DEFAULT NULL , 
            `msg_id` INT(7) NULL , 
            `hour` BIGINT(7) NULL DEFAULT '0', 
            `online` TINYINT(1) UNSIGNED NOT NULL DEFAULT '0' , 
            PRIMARY KEY (`name`(10))) ENGINE = InnoDB;''')
        return 
    
    def get_value(self ,name):
        t = int(time())
        val = cur(fetchall=True ,
                execute=f"""
                SELECT `name`,`text`,`button`,`msg_id`,`hour`,`online` 
                FROM tabliq WHERE online = 1 AND `name` = {name} FOR UPDATE;
                UPDATE tabliq SET 
                `hour`=IF(`hour`>{t} ,`hour`,0),
                `online`=IF(`hour`= 0 ,0,1)
                WHERE online = 1;
                COMMIT;""")
        if val:return {'name':val[0],'text':val[1],'button':val[2],'msg_id':val[3],'hour':val[4],'online':val[5]}
        return None

    def insert_msg(self ,msg_id ,button=None ):
        cur(commit=True ,
                execute=f"INSERT INTO tabliq(msg_id) VALUES({msg_id});")
        if button:
            cur(commit=True ,
                execute=f"UPDATE tabliq SET button = '{button}' WHERE msg_id = {msg_id};")
        return
    
    def update_time(self ,name ,hour=None):
        hour =int(time()+hour*60*60)
        return cur(commit=True ,
            execute=f"UPDATE tabliq SET `hour` = {hour} WHERE `name` = '{name}';")

    def update_online(self ,name):
        return cur(commit=True ,
                execute=f"UPDATE tabliq SET `online` = IF(`online` ,0,1) WHERE `name` = '{name}';")

    def del_row(self,name):
        return cur(commit=True ,
                execute=f"DELETE FROM tabliq WHERE `name` = '{name}';")

################################################################################
### Help
################################################################################
class Helps:
    '''
    Helps minstabot
    load data helps => table helps
    '''
    d = ()

    def __init__(self) -> None:
        self.helps = {}
        if RUNFUNC: return self.creat_table()

    def __repr__(self) -> str: return repr(self.helps)

    def __getitem__(self, key):
        if self.helps.get(key ,False): return self.helps[key]
        else: 
            val =cur(fetchone=True 
            ,execute=f'SELECT help_data,help_msgid FROM helps WHERE 1') # help_name="{key}"
            if val: 
                self.helps[key] = {'data':val[0] ,'msgid':val[1]}
                return self.helps[key]
            else:
                cur(commit=True 
                ,execute=f"""INSERT INTO helps(help_name) VALUES('{key}') 
                ON DUPLICATE KEY UPDATE help_name = '{key}';""")
                self.helps[key] = 0
                return 0

    def update(self, key, data ,msgid):
        self[key]
        cur(commit=True 
            ,execute=f"""UPDATE helps SET 
                            help_data = '{data}',
                            help_msgid = {msgid} 
                            where help_name = '{key}';""")
        self.helps[key] = {'data':data ,'msgid':msgid}
        return

    def creat_table(self):
        cur(commit=True ,
        execute='''CREATE TABLE IF NOT EXISTS `helps` (
            `help_name` TEXT(15) NOT NULL , 
            `help_data` TEXT(100) NULL , 
            `help_msgid` INT(7) NULL , 
            PRIMARY KEY (`help_name`(15))) ENGINE = InnoDB;''')
        return 