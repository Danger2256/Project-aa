import json
import telebot
from checker import check_domains, take_screenshot

# خواندن پیکربندی
with open('config.json', 'r') as f:
    config = json.load(f)

bot = telebot.TeleBot(config['telegram_token'])

# خواندن کاربران مجاز
with open('users.json', 'r') as f:
    authorized_users = json.load(f)["users"]

def is_authorized(user_id):
    return str(user_id) in authorized_users

@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    if is_authorized(message.from_user.id):
        bot.reply_to(message, "خوش آمدید! برای استفاده از ربات از دستورات استفاده کنید.")
    else:
        bot.reply_to(message, "شما مجاز به استفاده از این ربات نیستید.")

@bot.message_handler(commands=['add'])
def add_domain(message):
    if not is_authorized(message.from_user.id):
        return
    domain = message.text.split(' ', 1)[-1]
    with open('domains.json', 'r') as f:
        domains = json.load(f)
    if domain not in domains:
        domains.append(domain)
        with open('domains.json', 'w') as f:
            json.dump(domains, f, indent=2)
        bot.reply_to(message, f"دامنه {domain} اضافه شد.")
    else:
        bot.reply_to(message, "این دامنه قبلا اضافه شده.")

@bot.message_handler(commands=['remove'])
def remove_domain(message):
    if not is_authorized(message.from_user.id):
        return
    domain = message.text.split(' ', 1)[-1]
    with open('domains.json', 'r') as f:
        domains = json.load(f)
    if domain in domains:
        domains.remove(domain)
        with open('domains.json', 'w') as f:
            json.dump(domains, f, indent=2)
        bot.reply_to(message, f"دامنه {domain} حذف شد.")
    else:
        bot.reply_to(message, "دامنه پیدا نشد.")

@bot.message_handler(commands=['list'])
def list_domains(message):
    if not is_authorized(message.from_user.id):
        return
    with open('domains.json', 'r') as f:
        domains = json.load(f)
    if domains:
        bot.reply_to(message, "\n".join(domains))
    else:
        bot.reply_to(message, "هیچ دامنه‌ای ثبت نشده.")

@bot.message_handler(commands=['screenshot'])
def send_screenshot(message):
    if not is_authorized(message.from_user.id):
        return
    domain = message.text.split(' ', 1)[-1]
    path = take_screenshot(domain)
    if path:
        with open(path, 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    else:
        bot.reply_to(message, "خطا در گرفتن اسکرین‌شات.")

@bot.message_handler(commands=['check'])
def manual_check(message):
    if not is_authorized(message.from_user.id):
        return
    changes = check_domains()
    if changes:
        for change in changes:
            bot.send_message(message.chat.id, change)
    else:
        bot.reply_to(message, "همه دامنه‌ها در دسترس هستند.")

bot.polling()
