#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import requests
import json
import time
import os
from dotenv import load_dotenv

# Завантаження змінних середовища
load_dotenv()

TOKEN = os.getenv('BOT_TOKEN', 'YOUR_BOT_TOKEN_HERE')
BASE_URL = f'https://api.telegram.org/bot{TOKEN}/'

# Теоретичні матеріали
THEORY = {
    "basics": """📚 **Основи C/C++**

**Історія:**
• C створена в 1972 році Денісом Рітчі
• C++ створена в 1985 році Б'ярном Страуструпом

**Приклад програми:**
```c
#include <stdio.h>
int main() {
    printf("Hello, World!\\n");
    return 0;
}
```""",
    
    "variables": """📊 **Змінні та типи даних**

**Основні типи:**
• `int` - цілі числа
• `float` - дійсні числа  
• `char` - символи
• `double` - подвійна точність

**Приклад:**
```c
int age = 25;
float pi = 3.14f;
char grade = 'A';
```""",
    
    "operators": """🔢 **Оператори**

**Арифметичні:**
• `+` - додавання
• `-` - віднімання
• `*` - множення
• `/` - ділення

**Порівняння:**
• `==` - рівність
• `!=` - нерівність
• `>`, `<` - більше, менше"""
}

# Тестові питання
QUESTIONS = [
    {"q": "Хто створив C?", "opts": ["Деніс Рітчі", "Б'ярн Страуструп", "Білл Гейтс"], "ans": 0},
    {"q": "Тип для цілих чисел?", "opts": ["float", "int", "char"], "ans": 1},
    {"q": "Кінець рядка в C?", "opts": ["\\0", "\\n", ";"], "ans": 0},
    {"q": "Функція виводу в C?", "opts": ["print()", "printf()", "cout"], "ans": 1},
    {"q": "Розмір char?", "opts": ["1 байт", "2 байти", "4 байти"], "ans": 0}
]

# Стан користувачів
user_states = {}

def send_message(chat_id, text, reply_markup=None):
    """Відправити повідомлення"""
    data = {
        'chat_id': chat_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(BASE_URL + 'sendMessage', data=data)
    return response.json()

def edit_message(chat_id, message_id, text, reply_markup=None):
    """Редагувати повідомлення"""
    data = {
        'chat_id': chat_id,
        'message_id': message_id,
        'text': text,
        'parse_mode': 'Markdown'
    }
    if reply_markup:
        data['reply_markup'] = json.dumps(reply_markup)
    
    response = requests.post(BASE_URL + 'editMessageText', data=data)
    return response.json()

def get_main_keyboard():
    """Головне меню"""
    return {
        'inline_keyboard': [
            [{'text': '📚 Теорія', 'callback_data': 'theory'}],
            [{'text': '📝 Тест', 'callback_data': 'test'}],
            [{'text': '🔗 Посилання', 'callback_data': 'links'}]
        ]
    }

def get_theory_keyboard():
    """Меню теорії"""
    return {
        'inline_keyboard': [
            [{'text': '🔤 Основи C/C++', 'callback_data': 't_basics'}],
            [{'text': '📊 Змінні та типи', 'callback_data': 't_variables'}],
            [{'text': '🔢 Оператори', 'callback_data': 't_operators'}],
            [{'text': '⬅️ Назад', 'callback_data': 'menu'}]
        ]
    }

def get_back_keyboard(callback_data='menu'):
    """Кнопка назад"""
    return {
        'inline_keyboard': [
            [{'text': '⬅️ Назад', 'callback_data': callback_data}]
        ]
    }

def handle_start(chat_id):
    """Обробка команди /start"""
    text = """🤖 **Вітаю в C/C++ Trainer!**

Я допоможу вам вивчити основи програмування на C та C++.

**Що я можу:**
📚 Надати теоретичні матеріали
📝 Провести тестування знань  
🔗 Поділитися корисними ресурсами

Оберіть розділ:"""
    
    send_message(chat_id, text, get_main_keyboard())

def handle_callback(chat_id, message_id, callback_data, user_id):
    """Обробка callback запитів"""
    
    if callback_data == 'menu':
        text = "🤖 **C/C++ Trainer**\\n\\nОберіть розділ:"
        edit_message(chat_id, message_id, text, get_main_keyboard())
    
    elif callback_data == 'theory':
        text = "📚 **Оберіть тему для вивчення:**"
        edit_message(chat_id, message_id, text, get_theory_keyboard())
    
    elif callback_data.startswith('t_'):
        topic = callback_data[2:]
        if topic in THEORY:
            edit_message(chat_id, message_id, THEORY[topic], get_back_keyboard('theory'))
    
    elif callback_data == 'test':
        import random
        # Початок тесту
        questions = random.sample(QUESTIONS, min(3, len(QUESTIONS)))
        user_states[user_id] = {
            'questions': questions,
            'current': 0,
            'score': 0
        }
        show_question(chat_id, message_id, user_id)
    
    elif callback_data.startswith('ans_'):
        answer = int(callback_data[4:])
        if user_id in user_states:
            state = user_states[user_id]
            current_q = state['questions'][state['current']]
            
            if answer == current_q['ans']:
                state['score'] += 1
                result = "✅ Правильно!"
            else:
                correct = current_q['opts'][current_q['ans']]
                result = f"❌ Неправильно! Відповідь: {correct}"
            
            state['current'] += 1
            
            if state['current'] < len(state['questions']):
                keyboard = {
                    'inline_keyboard': [
                        [{'text': '➡️ Далі', 'callback_data': 'next'}]
                    ]
                }
                text = f"{result}\\n\\nНатисни 'Далі' для продовження"
                edit_message(chat_id, message_id, text, keyboard)
            else:
                # Кінець тесту
                score = state['score']
                total = len(state['questions'])
                percent = (score / total) * 100
                
                text = f"""🎉 **Тест завершено!**

Результат: {score}/{total} ({percent:.0f}%)
{result}

{"🏆 Відмінно!" if percent >= 80 else "📚 Треба вчити більше!"}"""
                
                keyboard = {
                    'inline_keyboard': [
                        [{'text': '🔄 Ще раз', 'callback_data': 'test'}],
                        [{'text': '🏠 Меню', 'callback_data': 'menu'}]
                    ]
                }
                edit_message(chat_id, message_id, text, keyboard)
                del user_states[user_id]
    
    elif callback_data == 'next':
        show_question(chat_id, message_id, user_id)
    
    elif callback_data == 'links':
        text = """🔗 **Корисні ресурси:**

📖 **Документація:**
• [cppreference.com](https://cppreference.com)
• [learn-c.org](https://www.learn-c.org/)

💻 **Онлайн компілятори:**
• [OnlineGDB](https://www.onlinegdb.com/online_c_compiler)
• [Replit](https://replit.com/languages/c)

📚 **Книги:**
• "C Programming Language" - K&R
• "C++ Primer" - Lippman"""
        
        edit_message(chat_id, message_id, text, get_back_keyboard())

def show_question(chat_id, message_id, user_id):
    """Показати питання"""
    if user_id in user_states:
        state = user_states[user_id]
        current = state['current']
        q = state['questions'][current]
        
        text = f"📝 **Питання {current + 1}/{len(state['questions'])}**\\n\\n❓ {q['q']}"
        
        keyboard = {
            'inline_keyboard': [
                [{'text': f"{chr(65+i)}. {opt}", 'callback_data': f'ans_{i}'}] 
                for i, opt in enumerate(q['opts'])
            ]
        }
        
        edit_message(chat_id, message_id, text, keyboard)

def get_updates(offset=None):
    """Отримати оновлення"""
    params = {'timeout': 30}
    if offset:
        params['offset'] = offset
    
    response = requests.get(BASE_URL + 'getUpdates', params=params)
    return response.json()

def main():
    """Головна функція"""
    print("🤖 Запуск C/C++ Trainer Bot...")
    print(f"Токен: {TOKEN[:10]}..." if TOKEN != 'YOUR_BOT_TOKEN_HERE' else "❌ Токен не знайдено!")
    
    # Перевірка токена
    response = requests.get(BASE_URL + 'getMe')
    if response.status_code == 200:
        bot_info = response.json()
        if bot_info['ok']:
            print(f"✅ Бот @{bot_info['result']['username']} успішно запущений!")
        else:
            print("❌ Помилка токена!")
            return
    else:
        print("❌ Не вдалося підключитися до Telegram API!")
        return
    
    offset = None
    print("🔄 Очікування повідомлень... (Ctrl+C для зупинки)")
    
    try:
        while True:
            updates = get_updates(offset)
            
            if updates['ok']:
                for update in updates['result']:
                    offset = update['update_id'] + 1
                    
                    # Обробка звичайних повідомлень
                    if 'message' in update:
                        message = update['message']
                        chat_id = message['chat']['id']
                        
                        if 'text' in message and message['text'] == '/start':
                            handle_start(chat_id)
                    
                    # Обробка callback запитів
                    elif 'callback_query' in update:
                        callback = update['callback_query']
                        chat_id = callback['message']['chat']['id']
                        message_id = callback['message']['message_id']
                        callback_data = callback['data']
                        user_id = callback['from']['id']
                        
                        # Відповідь на callback
                        requests.post(BASE_URL + 'answerCallbackQuery', 
                                    data={'callback_query_id': callback['id']})
                        
                        handle_callback(chat_id, message_id, callback_data, user_id)
            
            time.sleep(1)
    
    except KeyboardInterrupt:
        print("\\n🛑 Бот зупинено!")
    except Exception as e:
        print(f"❌ Помилка: {e}")

if __name__ == '__main__':
    main()