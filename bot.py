from models import *
import api

import os


@bot.message_handler(commands=['start'])
def start(message):
    markup = generate_markup(['/quest'])
    bot.send_message(message.chat.id, 'Добро пожаловать в квест «От Windows до Linux»', reply_markup=markup)
        

@bot.message_handler(commands=['quest'])
def quest(message):
    create_user(message.chat.id)
    
    name, description, image, markup = show_scene(message)
    bot.send_message(message.chat.id, 'Привет, начинаем квест')
    
    text = f'{name}\n\n{description}'
    
    bot.send_message(message.chat.id, text, reply_markup=markup)
    if image != 'None' and image != None:
        if 'http://' in image or 'https://' in image:
            try:
                bot.send_photo(message.chat.id, image)
            except:
                pass
        else: 
            bot.send_photo(message.chat.id, open(image, 'rb'))
            # Код работает, но картинка генерируется ~30 секунд, по этому закоментировал (в script.json в image надо поставить промт вместо ссылки)
            
            # path = api.gen_img(message.chat.id, image)
            # bot.send_photo(message.chat.id, open(path, 'rb'))

            # os.remove(path)
    

@bot.message_handler(content_types=['text'])
def handle_text(message):
    name, description, image, markup = update_scene(message)
    
    text = f'{name}\n\n{description}'
    bot.send_message(message.chat.id, text, reply_markup=markup)
    if image != 'None' and image != None:
        if 'http://' in image or 'https://' in image:
            try:
                bot.send_photo(message.chat.id, image)
            except:
                pass
        else:
            bot.send_photo(message.chat.id, open(image, 'rb'))
            # Код работает, но картинка генерируется ~30 секунд, по этому закоментировал (в script.json в image надо поставить промт вместо ссылки)
            
            # path = api.gen_img(message.chat.id, image)
            # bot.send_photo(message.chat.id, open(path, 'rb'))

            # os.remove(path)



bot.polling(none_stop=True)