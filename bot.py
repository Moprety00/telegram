import telebot
from telebot import types
import random
import logging
import threading
import http.server
import os

# ========================
# СЕРВЕР ДЛЯ RENDER (АНТИ-СОН)
# ========================
def run_dummy_server():
    port = int(os.environ.get("PORT", 8080))
    server_address = ('', port)
    httpd = http.server.HTTPServer(server_address, http.server.SimpleHTTPRequestHandler)
    httpd.serve_forever()

threading.Thread(target=run_dummy_server, daemon=True).start()

# ========================
# НАСТРОЙКИ БОТА
# ========================
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
log = logging.getLogger(__name__)

TOKEN = '8757257581:AAGyOvdsgdqv-Ko3ZTQ-rTfBH8QLisIwkGs'
bot = telebot.TeleBot(TOKEN)

lobbies = {}
user_lobbies = {}
user_states = {}
offline_games = {}

# ========================
# БАЗА ДАННЫХ ТЕМ
# ========================

# 1. Майнкрафт (Основы) - ~65 самых известных + боссы
MC_BASICS = [
    "Зомби", "Скелет", "Крипер", "Паук", "Эндермен", "Слизень", "Ведьма", "Гаст", "Блейз", 
    "Свинья", "Корова", "Овца", "Курица", "Деревенский житель", "Железный голем", "Волк", 
    "Кролик", "Лошадь", "Кошка", "Оцелот", "Попугай", "Черепаха", "Дельфин", "Панда", 
    "Лиса", "Аксолотль", "Пчела", "Кальмар", "Снежный голем", "Фантом", "Дракон Края", 
    "Визер", "Разбойник", "Поборник", "Вызыватель", "Разоритель", "Пиглин", "Хоглин", 
    "Магмовый куб", "Пещерный паук", "Чешуйница", "Зомби-житель", "Утопленник", 
    "Бродяга", "Кадавр", "Свинозомби", "Скелет-иссушитель", "Лама", "Белый медведь", 
    "Летучая мышь", "Страйдер", "Шалкер", "Страж", "Вредина", "Хранитель (Варден)", 
    "Лягушка", "Верблюд", "Нюхач", "Бриз", "Осёл", "Мул",
]

# 2. Майнкрафт (Вообще все) - Полный список
MC_ALL = sorted(list(set(MC_BASICS + [
    "Древний страж", "Зоглин", "Пиглин-дикарь", "Надзиратель", "Броненосец", 
    "Странствующий торговец", "Лама торговца", "Светящийся кальмар", 
    "Лошадь-скелет", "Лошадь-зомби", "Тропическая рыба", "Иглобрюх", "Треска", 
    "Лосось", "Грибная корова", "Козёл", "Снифер", "Болотный зомби", "Иллюзионист", 
    "Гигант", "Зомби-ребенок", "Курица-наездник", "Паучий наездник"
])))

CS_MAPS = ["Dust 2", "Mirage", "Inferno", "Nuke", "Overpass", "Ancient", "Anubis", "Vertigo", "Train", "Cache", "Cobblestone", "Office", "Italy", "AWP Lego", "2000$"]

CS_WEAPONS = ["Glock-18", "USP-S", "P2000", "P250", "Five-SeveN", "Tec-9", "CZ75-Auto", "Dual Berettas", "Desert Eagle", "R8 Revolver", "Nova", "XM1014", "MAG-7", "Sawed-Off", "MAC-10", "MP9", "MP7", "MP5-SD", "UMP-45", "PP-Bizon", "P90", "AK-47", "M4A4", "M4A1-S", "Galil AR", "FAMAS", "SG 553", "AUG", "AWP", "SSG 08", "SCAR-20", "G3SG1", "M249", "Negev", "Zeus x27", "Нож", "Дымовая граната", "Осколочная граната", "Молотов", "Зажигательная граната", "Световая граната", "Декой"]

PROFESSIONS = ["Врач", "Учитель", "Программист", "Дизайнер", "Повар", "Полицейский", "Судья", "Адвокат", "Пожарный", "Пилот", "Космонавт", "Журналист", "Блогер", "Актёр", "Певец", "Архитектор", "Строитель", "Водитель", "Таксист", "Фермер", "Менеджер", "Модель", "Футболист", "Киберспортсмен", "Президент", "Сантехник", "Электрик", "Сварщик", "Шахтёр", "Психолог", "Ветеринар", "Библиотекарь", "Гид", "Официант", "Бариста", "Банкир", "Режиссёр", "Фотограф", "Охранник", "Детектив", "Клоун", "Фокусник", "Каскадёр", "Стюардесса", "Снайпер", "Танкист", "Капитан корабля", "Хакер", "Учёный"]

RANDOM_THINGS = ["Нога", "Рука", "Голова", "Глаз", "Зуб", "Язык", "Хлеб", "Сыр", "Пицца", "Бургер", "Шаурма", "Сало", "Огурец", "Помидор", "Яблоко", "Банан", "Торт", "Шоколад", "Мороженое", "Вода", "Чай", "Кофе", "Собака", "Кошка", "Слон", "Акула", "Стул", "Стол", "Кровать", "Шкаф", "Лампа", "Дверь", "Окно", "Холодильник", "Ложка", "Футболка", "Джинсы", "Шапка", "Носки", "Кроссовки", "Часы", "Машина", "Автобус", "Поезд", "Самолёт", "Велосипед", "Ракета", "Ручка", "Тетрадь", "Телефон", "Ноутбук", "Наушники", "Телевизор", "Дерево", "Цветок", "Камень", "Река", "Море", "Солнце", "Звезда", "Мяч", "Кукла", "Лего", "Молоток", "Пила", "Гитара", "Школа", "Больница", "Магазин", "Какашка", "Ничего", "Пустота", "Воздух", "Огонь", "Дым", "Жвачка", "Сопли", "Слеза", "Кровь", "Прыщ", "Смех", "Книга", "Фото", "Флаг", "Спички", "Коробка", "Кошелёк", "Зонт", "Чипсы", "Сникерс", "Вареники", "НЛО", "Ёлка", "Подарок", "Меч", "Дракон", "Мыло", "Бинт", "Таблетка", "Наручники", "Люк", "Урна", "Маяк", "Якорь", "Весло", "Руль", "Колесо"]

HUMOR = [
    "Какашка", "Понос", "Пердёж", "Сопля", "Козявка", "Блевотина", "Жопа", "Говнюк", "Лох", "Даун", "Дебил", "Идиот", 
    "Халяль", "Харам", "Аллах акбар", "Алла Семенновна", "Ирина Леонидовна", "Сестра Келеша", "Анус", "Хиджаб", "Мечеть", "Никита Богданов", "Коран", 
    "Гроб", "Могила", "Кладбище", "Скелет", "Призрак", "Ядерная бомба", "Геморой", "ЕГЭ", "Бак", "Доширак", 
    "Шаурма", "Запор", "Мутант", "Вагинальный узбек", "Кортавый Француз", "крыса", "Летающий тапок", 
    "Арбуз", "Чудо Оолаха", "Оолах ", "Благословение Оолаха", "Скибиди туалет", "Абобус", "Конча", "шлюха", 
    "Скуф", "Альтушка", "Тюбик", "Казах", "Сигма", "Подкрадули", "Бархатные тяги", "Анонимус", "Золотой дождь", 
    "Шиза", "Даун", "Таракан", "Монгол", "Бырга", "67", "Гуль", "Пов: ты шпион", 
    "Анальная трешина", "свинина", "Харамная свинья"
]

THEMES = {
    "🌱 Майнкрафт (основы)": MC_BASICS,
    "💀 Майнкрафт (вообще все)": MC_ALL,
    "🗺 КС2 (карты)": CS_MAPS,
    "🔫 КС2 (оружие)": CS_WEAPONS,
    "👷 Профессии": PROFESSIONS,
    "🎲 Рандом": RANDOM_THINGS,
    "😂 Юмор": HUMOR
}
THEME_KEYS = list(THEMES.keys())

# ========================
# ЛОГИКА
# ========================
def safe_delete(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass

def track_msg(lobby_id, msg):
    if msg and lobby_id in lobbies:
        lobbies[lobby_id].setdefault('msgs', []).append((msg.chat.id, msg.message_id))

def clear_lobby_messages(lobby_id):
    if lobby_id not in lobbies: return
    for cid, mid in lobbies[lobby_id].get('msgs', []): safe_delete(cid, mid)
    lobbies[lobby_id]['msgs'] = []

def track_system_msg(lobby_id, msg):
    if msg and lobby_id in lobbies:
        lobbies[lobby_id].setdefault('system_msgs', []).append((msg.chat.id, msg.message_id))

def clear_system_messages(lobby_id):
    if lobby_id not in lobbies: return
    for cid, mid in lobbies[lobby_id].get('system_msgs', []): safe_delete(cid, mid)
    lobbies[lobby_id]['system_msgs'] = []

def get_real_lobby(user_id):
    lid = user_lobbies.get(user_id)
    if lid and lid in lobbies: return lid
    return None

def dissolve_lobby(lobby_id):
    if lobby_id not in lobbies: return
    players = list(lobbies[lobby_id]['players'].keys())
    clear_lobby_messages(lobby_id)
    clear_system_messages(lobby_id)
    for p_id in players:
        user_lobbies.pop(p_id, None)
        user_states.pop(p_id, None)
    del lobbies[lobby_id]

# ========================
# КЛАВИАТУРЫ
# ========================
def kb_main():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("📱 Оффлайн (1 телефон)", callback_data="offline_mode"),
          types.InlineKeyboardButton("🌐 Онлайн (по коду)", callback_data="online_mode"))
    return m

def kb_online_menu():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("Создать ➕", callback_data="create_game"),
          types.InlineKeyboardButton("Войти 🤝", callback_data="join_game"))
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="go_main"))
    return m

def kb_game_controls():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(types.InlineKeyboardButton("🔄 Новый раунд", callback_data="restart_game"),
          types.InlineKeyboardButton("🏠 Выйти", callback_data="main_menu"))
    return m

# ========================
# КОМАНДЫ
# ========================
@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.from_user.id
    user_states.pop(uid, None)
    offline_games.pop(uid, None)
    start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(types.KeyboardButton("/start"))
    bot.send_message(message.chat.id, "⬇️ Кнопка старта всегда под рукой", reply_markup=start_kb)
    bot.send_message(message.chat.id, "🎭 *Добро пожаловать в Чудо Оолаха!*", parse_mode="Markdown", reply_markup=kb_main())

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) != 'entering_code' and not m.text.startswith('/'))
def block_text(message):
    safe_delete(message.chat.id, message.message_id)

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'entering_code')
def handle_code(message):
    uid = message.from_user.id
    code = message.text.strip()
    safe_delete(message.chat.id, message.message_id)
    if code in lobbies:
        lobby = lobbies[code]
        if len(lobby['players']) < lobby['settings']['players_count']:
            lobby['players'][uid] = message.from_user.first_name
            user_lobbies[uid] = code
            user_states.pop(uid, None)
            for p_id in lobby['players']:
                msg = bot.send_message(p_id, f"➕ {message.from_user.first_name} зашёл! ({len(lobby['players'])}/{lobby['settings']['players_count']})")
                track_system_msg(code, msg)
            if len(lobby['players']) == lobby['settings']['players_count']:
                clear_system_messages(code)
                clear_lobby_messages(code)
                start_distribution(code)
        else: bot.send_message(message.chat.id, "❌ Лобби заполнено!")
    else: bot.send_message(message.chat.id, "❌ Неверный код!")

# ========================
# ОБРАБОТКА КНОПОК
# ========================
@bot.callback_query_handler(func=lambda call: True)
def handle_cb(call):
    chat_id, uid, mid, data = call.message.chat.id, call.from_user.id, call.message.message_id, call.data
    try: bot.answer_callback_query(call.id)
    except: pass

    if data == "go_main":
        offline_games.pop(uid, None); lid = get_real_lobby(uid)
        if lid: dissolve_lobby(lid)
        safe_delete(chat_id, mid)
        bot.send_message(chat_id, "🎭 *Чудо Оолаха*", parse_mode="Markdown", reply_markup=kb_main())

    elif data == "online_mode":
        safe_delete(chat_id, mid)
        bot.send_message(chat_id, "🌐 *Онлайн режим*", parse_mode="Markdown", reply_markup=kb_online_menu())

    elif data == "create_game":
        lid = str(random.randint(100000, 999999))
        lobbies[lid] = {'host_id': uid, 'players': {uid: call.from_user.first_name}, 'settings': {'players_count': 3, 'spies_count': 1, 'theme': THEME_KEYS[0]}, 'data': {}, 'msgs': [], 'system_msgs': [], 'started': False}
        user_lobbies[uid] = lid
        safe_delete(chat_id, mid)
        m = types.InlineKeyboardMarkup(row_width=4)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_p_{i}") for i in range(3, 11)])
        msg = bot.send_message(chat_id, f"🎲 *Комната `{lid}`*\n\n1️⃣ Сколько игроков?", parse_mode="Markdown", reply_markup=m)
        track_msg(lid, msg)

    elif data.startswith("set_p_"):
        n = int(data.split("_")[2]); lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['players_count'] = n
            safe_delete(chat_id, mid)
            m = types.InlineKeyboardMarkup(row_width=3)
            m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_s_{i}") for i in range(1, min(n, 5))])
            msg = bot.send_message(chat_id, "2️⃣ Сколько шпионов?", reply_markup=m); track_msg(lid, msg)

    elif data.startswith("set_s_"):
        n = int(data.split("_")[2]); lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['spies_count'] = n
            safe_delete(chat_id, mid)
            m = types.InlineKeyboardMarkup()
            for i, t in enumerate(THEME_KEYS): m.add(types.InlineKeyboardButton(t, callback_data=f"set_t_{i}"))
            msg = bot.send_message(chat_id, "3️⃣ Выбери тему:", reply_markup=m); track_msg(lid, msg)

    elif data.startswith("set_t_"):
        idx = int(data.split("_")[2]); lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['theme'] = THEME_KEYS[idx]
            safe_delete(chat_id, mid)
            m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_lobby"))
            msg = bot.send_message(chat_id, f"✅ *Лобби `{lid}` готово!*\nОжидание игроков...", parse_mode="Markdown", reply_markup=m)
            track_msg(lid, msg)

    elif data == "join_game":
        user_states[uid] = 'entering_code'; safe_delete(chat_id, mid)
        bot.send_message(chat_id, "🔑 Введи 6-значный код лобби:")

    elif data == "show_card":
        lid = get_real_lobby(uid)
        if not lid: return
        pd = lobbies[lid]['data'].get(uid); safe_delete(chat_id, mid)
        txt = "🕵️ *ТЫ ШПИОН!*" if pd['is_spy'] else f"✅ *Ты мирный*\n\n📂 Тема: {pd['theme_name']}\n🎯 Загадано: *{pd['card_name']}*"
        m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="hide_card"))
        msg = bot.send_message(chat_id, txt, parse_mode="Markdown", reply_markup=m); track_msg(lid, msg)

    elif data == "hide_card":
        safe_delete(chat_id, mid); lid = get_real_lobby(uid)
        m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("👁️ Показать", callback_data="show_card"))
        msg = bot.send_message(chat_id, "🔒 Скрыто.", reply_markup=m)
        if lid: track_msg(lid, msg)

    elif data == "restart_game":
        lid = get_real_lobby(uid)
        if lid and lobbies[lid]['host_id'] == uid: clear_lobby_messages(lid); start_distribution(lid)

    elif data == "main_menu" or data == "cancel_lobby":
        lid = get_real_lobby(uid); if lid: dissolve_lobby(lid)
        safe_delete(chat_id, mid); bot.send_message(chat_id, "🎭 *Чудо Оолаха*", parse_mode="Markdown", reply_markup=kb_main())

    # --- ОФФЛАЙН РЕЖИМ ---
    elif data == "offline_mode":
        offline_games[uid] = {'players': 3, 'spies': 1, 'theme': THEME_KEYS[0], 'cur': 0}
        safe_delete(chat_id, mid)
        m = types.InlineKeyboardMarkup(row_width=4)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_p_{i}") for i in range(3, 11)])
        bot.send_message(chat_id, "📱 *Оффлайн*\nСколько игроков?", parse_mode="Markdown", reply_markup=m)

    elif data.startswith("off_p_"):
        offline_games[uid]['players'] = int(data.split("_")[2]); safe_delete(chat_id, mid)
        m = types.InlineKeyboardMarkup()
        for i, t in enumerate(THEME_KEYS): m.add(types.InlineKeyboardButton(t, callback_data=f"off_t_{i}"))
        bot.send_message(chat_id, "Выбери тему:", reply_markup=m)

    elif data.startswith("off_t_"):
        og = offline_games[uid]; og['theme'] = THEME_KEYS[int(data.split("_")[2])]
        word = random.choice(THEMES[og['theme']])
        spy_idx = random.sample(range(og['players']), og['spies'])
        og['roles'] = [{'is_spy': i in spy_idx, 'word': word} for i in range(og['players'])]
        off_show_turn(uid, chat_id, mid)

    elif data == "off_show":
        og = offline_games[uid]; role = og['roles'][og['cur']]; safe_delete(chat_id, mid)
        txt = "🕵️ *ШПИОН!*" if role['is_spy'] else f"✅ *Мирный*\n\nЗагадано: *{role['word']}*"
        m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="off_next"))
        bot.send_message(chat_id, txt, parse_mode="Markdown", reply_markup=m)

    elif data == "off_next":
        offline_games[uid]['cur'] += 1; off_show_turn(uid, chat_id, mid)

def off_show_turn(uid, chat_id, mid):
    og = offline_games[uid]; safe_delete(chat_id, mid)
    if og['cur'] < og['players']:
        m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton(f"👁️ Игрок {og['cur']+1}", callback_data="off_show"))
        bot.send_message(chat_id, f"📱 Передай телефон Игроку {og['cur']+1}", reply_markup=m)
    else:
        m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("🏠 В меню", callback_data="go_main"))
        bot.send_message(chat_id, "✅ Все посмотрели роли! Начинайте игру.", reply_markup=m)

def start_distribution(lobby_id):
    lobby = lobbies[lobby_id]; lobby['started'] = True
    player_ids = list(lobby['players'].keys())
    spies = set(random.sample(player_ids, lobby['settings']['spies_count']))
    theme = lobby['settings']['theme']; word = random.choice(THEMES[theme])
    for p_id in player_ids:
        lobby['data'][p_id] = {'is_spy': p_id in spies, 'card_name': word, 'theme_name': theme}
        m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("👁️ Показать роль", callback_data="show_card"))
        msg = bot.send_message(p_id, "🎮 *Раунд начался!*", parse_mode="Markdown", reply_markup=m); track_msg(lobby_id, msg)
        msg2 = bot.send_message(p_id, "⬇️ Управление раундом:", reply_markup=kb_game_controls()); track_msg(lobby_id, msg2)

if __name__ == '__main__':
    try:
        bot.remove_webhook()
        print("Чудо Оолаха онлайн!", flush=True)
        bot.infinity_polling(timeout=10, long_polling_timeout=5)
    except Exception as e:
        print(f"Ошибка: {e}", flush=True)
