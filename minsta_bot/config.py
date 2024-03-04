from database import database_minsta

setting = database_minsta.Setting() # setting minstabot
users_db = database_minsta.UserDict()
admin_db = database_minsta.Admin()
next_msg_db =  database_minsta.NextPm()
support_db = database_minsta.Support() # poshtibani
accounts_db = database_minsta.Accounts()
watch_list_db = database_minsta.WatchList()
support_db = database_minsta.Support()
tablig_db = database_minsta.Tabliq()
helps_db = database_minsta.Helps()

adimin_bot_token = "<TOKEN>"
minsta_bot_token = "<TOKEN>"
admin_id = 10101010 # root admin
setting_channel_id = -10010101010 # channel setting bots
path_webhook = 'https://userDomin.Name'

db_user = "root"
db_password = ''
db_host = '127.0.0.1'
db_database = ''

# sys.path.append('/home/botcodeu/Telegram-Bot/database')
# import database_minsta