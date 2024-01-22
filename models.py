import telebot

import sqlite3
import json
import re

from quest import *


token = ''
bot = telebot.TeleBot(token, skip_pending=True)

commands = [telebot.types.BotCommand("/start", "Перезапуск бота"),
            telebot.types.BotCommand("/quest", "Начать квест")]
bot.set_my_commands(commands) 

engine = QuestEngine()

with sqlite3.connect('data.db') as conn:
    cur = conn.cursor() 
    cur.execute("""CREATE TABLE IF NOT EXISTS users( 
        user_id INTEGER, 
        scene_num TEXT,
        save_data TEXT);
    """) 
    conn.commit() 




def create_user(id):
    with sqlite3.connect('data.db') as conn: # Один раз объявить нельзя, из-за того что бот синхронный
        cur = conn.cursor()
        cur.execute(f"SELECT * FROM users WHERE user_id = {id}")
        if cur.fetchone() is None:
            save_data = {}
            save_data = json.dumps(save_data)
            cur.execute(f"INSERT INTO users VALUES ({id}, 1.1, ?)", ("{}",))
            conn.commit()
        else: 
            cur.execute(f"UPDATE users SET scene_num = 1.1 WHERE user_id = {id}")
            conn.commit()


# Генерация кнопок ответов   
def generate_markup(options): 
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True) 
    if options == []:
        markup = telebot.types.ReplyKeyboardRemove()
        
    for option  in options: 
        markup.add(option) 
    return markup


def show_scene(message):
    with sqlite3.connect('data.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT scene_num FROM users WHERE user_id = {message.chat.id}")
        scene_num = cur.fetchone()[0]

    name, description, image, options = engine.get_scene(scene_num)
    if name == 'END':
        return name, None, None, None
    markup = generate_markup(options) 
    
    
    pattern = r"{{(\w+)}}"
    placeholders = re.findall(pattern, description)

    cur.execute(f"SELECT save_data FROM users WHERE user_id={message.chat.id}")
    save_data = cur.fetchone()[0]
    
    save_items = json.loads(save_data)

    if placeholders: # в description можно брать сохраненные данные ("save_data": {"key": "value"}) с помощью {{key}}, в своем квесте не использовал, но возможность такую сделал (можно использовать например для имени)
        for ph in placeholders:
            if ph in save_items:
                value = save_items[ph]
                description = description.replace("{{" + ph + "}}", value)
    
    return name, description, image, markup


def update_scene(message):
    with sqlite3.connect('data.db') as conn:
        cur = conn.cursor()
        cur.execute(f"SELECT scene_num FROM users WHERE user_id = {message.chat.id}")
        scene_num = cur.fetchone()[0]
        
        options = engine.get_options(scene_num)
        save_data = engine.get_save_data(scene_num) 
        
        if save_data != 'None':
            cur.execute(f"SELECT save_data FROM users WHERE user_id = {message.chat.id}")
            save_data_db = cur.fetchone()[0]
            save_data_db = json.loads(save_data_db)
            for key, value in save_data.items():
                save_data_db[key] = value
            save_data_db = json.dumps(save_data_db)
            cur.execute(f"UPDATE users SET save_data = '{save_data_db}' WHERE user_id = {message.chat.id}")
            conn.commit()
        
        if message.text in options:
            next_scene = engine.get_transition(scene_num, message.text)
            cur.execute(f'UPDATE users SET scene_num = "{next_scene}" WHERE user_id = {message.chat.id}')
            conn.commit()
            return show_scene(message)
        else:
            bot.send_message(message.chat.id, 'Такого варианта нет')
            return
    
    
    