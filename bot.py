import telebot
from telebot import types
import random
import logging
import threading
import http.server
import os

# ========================
# СЕРВЕР ДЛЯ RENDER
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
TOKEN = '8757257581:AAGyOvdsgdqv-Ko3ZTQ-rTfBH8QLisIwkGs'
bot = telebot.TeleBot(TOKEN)

lobbies = {}
user_lobbies = {}
user_states = {}
offline_games = {}
last_messages = {}

# ========================
# ТЕМЫ
# ========================
MC_BASICS = ["Зомби", "Скелет", "Крипер", "Паук", "Эндермен", "Слизень", "Ведьма", "Гаст", "Блейз", "Свинья", "Корова", "Овца", "Курица", "Житель", "Железный голем", "Волк", "Кролик", "Лошадь", "Кошка", "Оцелот", "Попугай", "Черепаха", "Дельфин", "Панда", "Лиса", "Аксолотль", "Пчела", "Кальмар", "Снежный голем", "Фантом", "Дракон Края", "Визер", "Разбойник", "Поборник", "Вызыватель", "Разоритель", "Пиглин", "Хоглин", "Магмовый куб", "Пещерный паук", "Чешуйница", "Зомби-житель", "Утопленник", "Бродяга", "Кадавр", "Свинозомби", "Скелет-иссушитель", "Лама", "Белый медведь", "Страйдер", "Шалкер", "Страж", "Вредина", "Хранитель (Варден)", "Лягушка", "Аллай", "Верблюд", "Нюхач", "Бриз"]

MC_ALL = sorted(list(set(MC_BASICS + ["Древний страж", "Зоглин", "Пиглин-дикарь", "Надзиратель", "Броненосец", "Странствующий торговец", "Лама торговца", "Светящийся кальмар", "Лошадь-скелет", "Лошадь-зомби", "Тропическая рыба", "Иглобрюх", "Треска", "Лосось", "Грибная корова", "Козёл", "Снифер", "Болотный зомби"])))

CS_MAPS = ["Dust 2", "Mirage", "Inferno", "Nuke", "Overpass", "Ancient", "Anubis", "Vertigo", "Train", "Cache", "Cobblestone", "Office", "Italy", "AWP Lego", "2000$"]

CS_WEAPONS = ["Glock-18", "USP-S", "P2000", "P250", "Five-SeveN", "Tec-9", "CZ75-Auto", "Dual Berettas", "Desert Eagle", "R8 Revolver", "Nova", "XM1014", "MAG-7", "Sawed-Off", "MAC-10", "MP9", "MP7", "MP5-SD", "UMP-45", "PP-Bizon", "P90", "AK-47", "M4A4", "M4A1-S", "Galil AR", "FAMAS", "SG 553", "AUG", "AWP", "SSG 08", "SCAR-20", "G3SG1", "M249", "Negev", "Zeus x27", "Нож"]

PROFESSIONS = ["Врач", "Учитель", "Программист", "Дизайнер", "Повар", "Полицейский", "Судья", "Адвокат", "Пожарный", "Пилот", "Космонавт", "Журналист", "Актёр", "Певец", "Архитектор", "Строитель", "Водитель", "Таксист", "Фермер", "Менеджер", "Модель", "Киберспортсмен", "Президент", "Хакер"]

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
    "🌱 Майн (основы)": MC_BASICS,
    "💀 Майн (вообще все)": MC_ALL,
    "🗺 КС2 (карты)": CS_MAPS,
    "🔫 КС2 (оружие)": CS_WEAPONS,
    "👷 Профессии": PROFESSIONS,
    "🎲 Рандом": RANDOM_THINGS,
    "😂 Юмор": HUMOR
}
THEME_KEYS = list(THEMES.keys())

# ========================
# УТИЛИТЫ
# ========================
def safe_delete(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

def send_new(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    if chat_id in last_messages:
        safe_delete(chat_id, last_messages[chat_id])
    msg = bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
    last_messages[chat_id] = msg.message_id
    return msg

def get_real_lobby(user_id):
    lid = user_lobbies.get(user_id)
    if lid and lid in lobbies:
        return lid
    return None

def dissolve_lobby(lobby_id):
    if lobby_id not in lobbies:
        return
    players = list(lobbies[lobby_id]['players'].keys())
    for p_id in players:
        user_lobbies.pop(p_id, None)
        user_states.pop(p_id, None)
        if p_id in last_messages:
            safe_delete(p_id, last_messages[p_id])
        try:
            bot.send_message(p_id, "❌ Лобби закрыто.")
        except:
            pass
    del lobbies[lobby_id]

# ========================
# КЛАВИАТУРЫ
# ========================
def kb_main():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(types.InlineKeyboardButton("📱 Оффлайн (1 телефон)", callback_data="off_start"),
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
# ОБРАБОТЧИКИ
# ========================
@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.from_user.id
    user_states.pop(uid, None)
    offline_games.pop(uid, None)
    start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(types.KeyboardButton("/start"))
    bot.send_message(message.chat.id, "✨ Меню обновлено", reply_markup=start_kb)
    send_new(message.chat.id, "🎭 *Чудо Оолаха приветствует тебя!*", reply_markup=kb_main())

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'entering_code')
def handle_code(message):
    uid = message.from_user.id
    code = message.text.strip()
    safe_delete(message.chat.id, message.message_id)
    if code in lobbies:
        l = lobbies[code]
        if len(l['players']) < l['settings']['players_count']:
            l['players'][uid] = message.from_user.first_name
            user_lobbies[uid] = code
            user_states.pop(uid, None)
            for p_id in l['players']:
                msg = bot.send_message(p_id, f"➕ {message.from_user.first_name} зашёл! ({len(l['players'])}/{l['settings']['players_count']})")
                l.setdefault('system_msgs', []).append((p_id, msg.message_id))
            if len(l['players']) == l['settings']['players_count']:
                start_distribution(code)
        else:
            bot.send_message(uid, "❌ Мест нет!")
    else:
        bot.send_message(uid, "❌ Код не найден!")

@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def block_text(message):
    safe_delete(message.chat.id, message.message_id)

@bot.callback_query_handler(func=lambda call: True)
def handle_cb(call):
    chat_id = call.message.chat.id
    uid = call.from_user.id
    mid = call.message.message_id
    data = call.data
    
    try:
        bot.answer_callback_query(call.id)
    except:
        pass

    if data == "go_main":
        offline_games.pop(uid, None)
        lid = get_real_lobby(uid)
        if lid:
            dissolve_lobby(lid)
        send_new(chat_id, "🎭 *Главное меню*", reply_markup=kb_main())

    elif data == "online_mode":
        send_new(chat_id, "🌐 *Онлайн режим*", reply_markup=kb_online_menu())

    elif data == "create_game":
        lid = str(random.randint(100000, 999999))
        lobbies[lid] = {
            'host_id': uid, 
            'players': {uid: call.from_user.first_name}, 
            'settings': {'players_count': 3, 'spies_count': 1, 'theme': THEME_KEYS[0]}, 
            'data': {}, 'msgs': [], 'system_msgs': [], 'started': False
        }
        user_lobbies[uid] = lid
        m = types.InlineKeyboardMarkup(row_width=4)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_p_{i}") for i in range(3, 11)])
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="online_mode"))
        send_new(chat_id, f"🎲 *Лобби `{lid}`*\n\n1️⃣ Сколько игроков?", reply_markup=m)

    elif data.startswith("set_p_"):
        n = int(data.split("_")[2])
        lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['players_count'] = n
            m = types.InlineKeyboardMarkup(row_width=3)
            m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_s_{i}") for i in range(1, min(n, 5))])
            m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="create_game"))
            send_new(chat_id, "2️⃣ Сколько шпионов?", reply_markup=m)

    elif data.startswith("set_s_"):
        n = int(data.split("_")[2])
        lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['spies_count'] = n
            m = types.InlineKeyboardMarkup()
            for i, t in enumerate(THEME_KEYS):
                m.add(types.InlineKeyboardButton(t, callback_data=f"set_t_{i}"))
            m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="create_game"))
            send_new(chat_id, "3️⃣ Выбери тему:", reply_markup=m)

    elif data.startswith("set_t_"):
        idx = int(data.split("_")[2])
        lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['theme'] = THEME_KEYS[idx]
            m = types.InlineKeyboardMarkup()
            m.add(types.InlineKeyboardButton("❌ Отмена", callback_data="go_main"))
            send_new(chat_id, f"✅ *Лобби `{lid}` готово!*\nДай код друзьям. Ждем игроков...", reply_markup=m)

    elif data == "join_game":
        user_states[uid] = 'entering_code'
        send_new(chat_id, "🔑 *Введи код лобби:*")

    elif data == "show_card":
        lid = get_real_lobby(uid)
        if lid:
            pd = lobbies[lid]['data'].get(uid)
            if pd:
                txt = "🕵️ *ТЫ ШПИОН!*" if pd['is_spy'] else f"✅ *Мирный*\n\n📂 {pd['theme_name']}\n🎯 *{pd['card_name']}*"
                m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="hide_card"))
                send_new(chat_id, txt, reply_markup=m)

    elif data == "hide_card":
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("👁️ Роль", callback_data="show_card"))
        send_new(chat_id, "🔒 Скрыто.", reply_markup=m)

    elif data == "restart_game":
        lid = get_real_lobby(uid)
        if lid:
            if lobbies[lid]['host_id'] == uid:
                start_distribution(lid)

    elif data == "main_menu" or data == "cancel_lobby":
        lid = get_real_lobby(uid)
        if lid:
            dissolve_lobby(lid)
        else:
            send_new(chat_id, "🎭 *Чудо Оолаха*", reply_markup=kb_main())

    elif data == "off_start":
        offline_games[uid] = {'players': 3, 'spies': 1, 'theme': THEME_KEYS[0], 'cur': 0}
        m = types.InlineKeyboardMarkup(row_width=4)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_p_{i}") for i in range(3, 11)])
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="go_main"))
        send_new(chat_id, "📱 *Оффлайн*\nСколько игроков?", reply_markup=m)

    elif data.startswith("off_p_"):
        offline_games[uid]['players'] = int(data.split("_")[2])
        p = offline_games[uid]['players']
        m = types.InlineKeyboardMarkup(row_width=3)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_s_{i}") for i in range(1, min(p, 5))])
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="off_start"))
        send_new(chat_id, "Сколько шпионов?", reply_markup=m)

    elif data.startswith("off_s_"):
        offline_games[uid]['spies'] = int(data.split("_")[2])
        m = types.InlineKeyboardMarkup()
        for i, t in enumerate(THEME_KEYS):
            m.add(types.InlineKeyboardButton(t, callback_data=f"off_t_{i}"))
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="off_start"))
        send_new(chat_id, "Выбери тему:", reply_markup=m)

    elif data.startswith("off_t_"):
        og = offline_games[uid]
        og['theme'] = THEME_KEYS[int(data.split("_")[2])]
        word = random.choice(THEMES[og['theme']])
        spy_idx = random.sample(range(og['players']), og['spies'])
        og['roles'] = [{'is_spy': i in spy_idx, 'word': word} for i in range(og['players'])]
        og['cur'] = 0
        off_show_turn(uid, chat_id)

    elif data == "off_show":
        og = offline_games[uid]
        role = og['roles'][og['cur']]
        txt = "🕵️ *ТЫ ШПИОН!*" if role['is_spy'] else f"✅ *Мирный*\n\nЗагадано: *{role['word']}*"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="off_next"))
        send_new(chat_id, txt, reply_markup=m)

    elif data == "off_next":
        offline_games[uid]['cur'] += 1
        off_show_turn(uid, chat_id)

    elif data == "off_restart":
        og = offline_games[uid]
        word = random.choice(THEMES[og['theme']])
        spy_idx = random.sample(range(og['players']), og['spies'])
        og['roles'] = [{'is_spy': i in spy_idx, 'word': word} for i in range(og['players'])]
        og['cur'] = 0
        off_show_turn(uid, chat_id)

def off_show_turn(uid, chat_id):
    og = offline_games[uid]
    if og['cur'] < og['players']:
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"👁️ Игрок {og['cur']+1}", callback_data="off_show"))
        send_new(chat_id, f"📱 Передай Игроку {og['cur']+1}", reply_markup=m)
    else:
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Заново", callback_data="off_restart")).add(types.InlineKeyboardButton("🏠 Меню", callback_data="go_main"))
        send_new(chat_id, "✅ Начинайте игру!", reply_markup=m)

def start_distribution(lid):
    l = lobbies[lid]
    l['started'] = True
    p_ids = list(l['players'].keys())
    spies = set(random.sample(p_ids, l['settings']['spies_count']))
    word = random.choice(THEMES[l['settings']['theme']])
    for p_id in p_ids:
        l['data'][p_id] = {'is_spy': p_id in spies, 'card_name': word, 'theme_name': l['settings']['theme']}
        msg = bot.send_message(p_id, "🎮 *Раунд начался!*", parse_mode="Markdown", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("👁️ Роль", callback_data="show_card")))
        l.setdefault('msgs', []).append((p_id, msg.message_id))
        msg2 = bot.send_message(p_id, "⬇️ Меню:", reply_markup=kb_game_controls())
        l.setdefault('msgs', []).append((p_id, msg2.message_id))

if __name__ == '__main__':
    bot.remove_webhook()
    bot.infinity_polling(timeout=20)
