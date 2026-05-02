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
TOKEN = '8757257581:AAGQ3m4j-TOfX8ec-_XdB9mQ9pcrP6L_cCM'
bot = telebot.TeleBot(TOKEN)

lobbies = {}
user_lobbies = {}
user_states = {}
offline_games = {}
last_messages = {} # Для чистки меню

# ========================
# БАЗА ТЕМ
# ========================
MC_BASICS = ["Зомби", "Скелет", "Крипер", "Паук", "Эндермен", "Слизень", "Ведьма", "Гаст", "Блейз", "Свинья", "Корова", "Овца", "Курица", "Житель", "Железный голем", "Волк", "Кролик", "Лошадь", "Кошка", "Оцелот", "Попугай", "Черепаха", "Дельфин", "Панда", "Лиса", "Аксолотль", "Пчела", "Кальмар", "Снежный голем", "Фантом", "Дракон Края", "Визер", "Разбойник", "Поборник", "Вызыватель", "Разоритель", "Пиглин", "Хоглин", "Магмовый куб", "Пещерный паук", "Чешуйница", "Зомби-житель", "Утопленник", "Бродяга", "Кадавр", "Свинозомби", "Скелет-иссушитель", "Лама", "Белый медведь", "Страйдер", "Шалкер", "Страж", "Вредина", "Хранитель (Варден)", "Лягушка", "Аллай", "Верблюд", "Нюхач", "Бриз"]

MC_ALL = sorted(list(set(MC_BASICS + ["Древний страж", "Зоглин", "Пиглин-дикарь", "Надзиратель", "Броненосец", "Странствующий торговец", "Лама торговца", "Светящийся кальмар", "Лошадь-скелет", "Лошадь-зомби", "Тропическая рыба", "Иглобрюх", "Треска", "Лосось", "Грибная корова", "Козёл", "Снифер", "Болотный зомби"])))

CS_MAPS = ["Dust 2", "Mirage", "Inferno", "Nuke", "Overpass", "Ancient", "Anubis", "Vertigo", "Train", "Cache", "Cobblestone", "Office", "Italy", "AWP Lego", "2000$"]

CS_WEAPONS = ["Glock-18", "USP-S", "P2000", "P250", "Five-SeveN", "Tec-9", "CZ75-Auto", "Dual Berettas", "Desert Eagle", "R8 Revolver", "Nova", "XM1014", "MAG-7", "Sawed-Off", "MAC-10", "MP9", "MP7", "MP5-SD", "UMP-45", "PP-Bizon", "P90", "AK-47", "M4A4", "M4A1-S", "Galil AR", "FAMAS", "SG 553", "AUG", "AWP", "SSG 08", "SCAR-20", "G3SG1", "M249", "Negev", "Zeus x27", "Нож"]

PROFESSIONS = ["Врач", "Учитель", "Программист", "Дизайнер", "Повар", "Полицейский", "Судья", "Адвокат", "Пожарный", "Пилот", "Космонавт", "Журналист", "Актёр", "Певец", "Архитектор", "Строитель", "Водитель", "Таксист", "Фермер", "Менеджер", "Модель", "Футболист", "Киберспортсмен", "Президент", "Хакер"]

RANDOM_THINGS = [
    # Кухня и еда
    "Чайник", "Сковорода", "Кастрюля", "Дуршлаг", "Половник", "Ложка", "Вилка", "Нож", "Тарелка", "Чашка",
    "Блендер", "Миксер", "Тостер", "Микроволновка", "Холодильник", "Духовка", "Хлеб", "Масло", "Сыр", "Колбаса",
    "Пицца", "Пельмени", "Борщ", "Макароны", "Огурец", "Помидор", "Картошка", "Морковь", "Лук", "Яблоко",
    "Банан", "Апельсин", "Торт", "Шоколад", "Мороженое", "Сок", "Кофе", "Бублик", "Яичница", "Салат",
    "Лимон", "Чеснок", "Мёд", "Варенье", "Гречка", "Рис", "Кетчуп", "Майонез", "Горчица", "Суши",

    # Дом и мебель
    "Диван", "Кровать", "Стул", "Стол", "Шкаф", "Комод", "Полка", "Зеркало", "Ковёр", "Штора",
    "Подушка", "Одеяло", "Люстра", "Торшер", "Лампа", "Картина", "Ваза", "Цветок", "Дверь", "Окно",
    "Стена", "Потолок", "Пол", "Лестница", "Балкон", "Замок", "Ключ", "Вешалка", "Тапочки", "Утюг",
    "Пылесос", "Ведро", "Швабра", "Веник", "Совок", "Корзина", "Часы", "Будильник", "Фен", "Мыло",

    # Техника и электроника
    "Телефон", "Ноутбук", "Планшет", "Компьютер", "Монитор", "Мышка", "Клавиатура", "Наушники", "Колонка", "Зарядка",
    "Камера", "Фотоаппарат", "Принтер", "Сканер", "Телевизор", "Пульт", "Батарейка", "Флешка", "Роутер", "Джойстик",
    "Микрофон", "Плеер", "Проектор", "Электросамокат", "Квадрокоптер", "Робот-пылесос", "Смарт-часы", "Рация", "Фонарик", "Калькулятор",

    # Одежда и аксессуары
    "Футболка", "Рубашка", "Свитер", "Куртка", "Пальто", "Джинсы", "Брюки", "Шорты", "Юбка", "Платье",
    "Носки", "Трусы", "Колготки", "Кроссовки", "Туфли", "Ботинки", "Сапоги", "Кепка", "Шапка", "Шарф",
    "Перчатки", "Ремень", "Галстук", "Очки", "Рюкзак", "Сумка", "Кошелёк", "Зонт", "Браслет", "Кольцо",

    # Животные и природа
    "Собака", "Кошка", "Лев", "Тигр", "Медведь", "Волк", "Лиса", "Заяц", "Слон", "Жираф",
    "Зебра", "Бегемот", "Крокодил", "Змея", "Обезьяна", "Хомяк", "Попугай", "Орёл", "Сова", "Пингвин",
    "Акула", "Кит", "Дельфин", "Осьминог", "Краб", "Черепаха", "Лягушка", "Пчела", "Бабочка", "Паук",
    "Дерево", "Цветок", "Трава", "Гриб", "Камень", "Песок", "Гора", "Река", "Озеро", "Море",
    "Океан", "Остров", "Лес", "Пустыня", "Облако", "Дождь", "Снег", "Радуга", "Солнце", "Луна",

    # Транспорт
    "Машина", "Автобус", "Грузовик", "Мотоцикл", "Велосипед", "Самокат", "Поезд", "Трамвай", "Метро", "Самолёт",
    "Вертолёт", "Корабль", "Лодка", "Катер", "Ракета", "Трактор", "Экскаватор", "Такси", "Лимузин", "Квадроцикл",

    # Предметы и разное
    "Книга", "Тетрадь", "Ручка", "Карандаш", "Линейка", "Краски", "Кисточка", "Бумага", "Газета", "Журнал",
    "Письмо", "Конверт", "Марка", "Открытка", "Фотография", "Карта", "Глобус", "Флаг", "Спички", "Зажигалка",
    "Свеча", "Монета", "Купюра", "Коробка", "Пакет", "Мешок", "Верёвка", "Скотч", "Клей", "Ножницы",
    "Иголка", "Нитки", "Пуговица", "Молоток", "Гвоздь", "Топор", "Пила", "Отвертка", "Дрель", "Лего",
    "Мяч", "Кукла", "Машинка", "Пазл", "Шахматы", "Карты", "Гитара", "Барабан", "Пианино", "Флейта",
    "Медаль", "Кубок", "Диплом", "Паспорт", "Маска", "Шлем", "Бинокль", "Мишень", "Удочка", "Сеть",

    # Юмор и "странные" вещи
    "Какашка", "Унитаз", "Сопля", "Прыщ", "Слюна", "Мусор", "Плесень", "Жвачка", "Таракан", "Клоп",
    "Носок", "Стелька", "Дырка", "Пустота", "Ничего", "Воздух", "Пыль", "Грязь", "Лужа", "Кирпич",
    "Шлакоблок", "Арматура", "Бетон", "Пепел", "Окурок", "Палка", "Камушек", "Труба", "Провод", "Шланг",

    # Места
    "Школа", "Больница", "Магазин", "Рынок", "Аптека", "Банк", "Завод", "Музей", "Театр", "Кино",
    "Цирк", "Зоопарк", "Парк", "Стадион", "Бассейн", "Пляж", "Тюрьма", "Церковь", "Отель", "Ресторан",

    # Ещё 500+ слов для массовости
    "Айсберг", "Аккумулятор", "Аквариум", "Антенна", "Асфальт", "Амулет", "Афиша", "Арфа", "Атлас", "Аэростат",
    "Багажник", "Базука", "Байдарка", "Баклажан", "Балалайка", "Баллон", "Бамбук", "Банка", "Бантик", "Барабан",
    "Баржа", "Барометр", "Бархан", "Бассейн", "Батарея", "Батон", "Башмак", "Башня", "Бегемот", "Бивень",
    "Бидон", "Билет", "Бинокль", "Бинт", "Биржа", "Бирка", "Бигуди", "Бицепс", "Блесна", "Блокнот",
    "Блюдце", "Борода", "Бочка", "Браслет", "Бревно", "Бритва", "Броня", "Брошь", "Бубен", "Будильник",
    "Будка", "Булавку", "Бульдозер", "Бумеранг", "Бункер", "Бусина", "Бутылка", "Вагон", "Валенок", "Валун",
    "Ватрушка", "Вафля", "Веер", "Вездеход", "Вектор", "Вертел", "Верстак", "Весло", "Весы", "Ветка",
    "Вигвам", "Витрина", "Вихрь", "Вкладыш", "Водопад", "Водоросль", "Волан", "Воронка", "Вулкан", "Вымпел",
    "Газета", "Гайка", "Галька", "Гамак", "Гантель", "Гарпун", "Гвоздика", "Гейзер", "Герб", "Гиря",
    "Гитара", "Глобус", "Гнездо", "Гну", "Гоблин", "Горилла", "Горн", "Горох", "Горчица", "Горшок",
    "Грабли", "Градусник", "Графин", "Гребень", "Грелка", "Гриль", "Грим", "Гроб", "Груз", "Груша",
    "Губка", "Гусеница", "Дартс", "Двигатель", "Детонатор", "Динамит", "Диплом", "Дирижабль", "Диск", "Дистанция",
    "Долото", "Домино", "Доспехи", "Дротик", "Дубина", "Дудка", "Духовка", "Дуршлаг", "Дыня", "Дырокол",
    "Ежевика", "Енот", "Ёлка", "Жалюзи", "Желудь", "Жерло", "Жетоны", "Жилет", "Жираф", "Журнал",
    "Забор", "Забрало", "Завод", "Зажигалка", "Зажим", "Занавес", "Заплата", "Запонка", "Засов", "Затычка",
    "Зебра", "Зефир", "Зигзаг", "Зонт", "Зубило", "Зубочистка", "Зелье", "Зерно", "Зенитка", "Знак",
    "Игла", "Игрушка", "Изюм", "Икона", "Иллюзия", "Имбирь", "Ингалятор", "Инкубатор", "Ириска", "Искра",
    "Йогурт", "Йод", "Кабан", "Каблук", "Кавычки", "Кадило", "Кадка", "Казак", "Кактус", "Калач",
    "Кальмар", "Кальян", "Камея", "Камин", "Камыш", "Канава", "Канарейка", "Канат", "Канделябр", "Канистра",
    "Капкан", "Капля", "Капюшон", "Карамель", "Карась", "Карат", "Каркас", "Карман", "Карниз", "Картон",
    "Картуз", "Карусель", "Каска", "Кассета", "Кастрюля", "Катамаран", "Катапульта", "Каток", "Катушка", "Кафе",
    "Кафтан", "Качка", "Каша", "Кашне", "Кашпо", "Кегля", "Кеды", "Кекс", "Кенгуру", "Кепи",
    "Керамогранит", "Керосин", "Кетчуп", "Кинжал", "Кино", "Кипарис", "Кипятильник", "Кирпич", "Кисель", "Кисть",
    "Кит", "Китель", "Клавиша", "Клапан", "Кларнет", "Клевер", "Клетка", "Клещ", "Клещи", "Клинок",
    "Клоун", "Клыки", "Клюв", "Клюшка", "Клякса", "Кнопка", "Кнут", "Кобура", "Ковчег", "Ковш",
    "Козырек", "Кокон", "Колба", "Колпак", "Колчан", "Кольцо", "Копыто", "Кора", "Коралл", "Корыто",
    "Коса", "Костер", "Костюм", "Косуля", "Котел", "Кочерга", "Кошелек", "Кошмар", "Кратер", "Крыжовник",
    "Кувшин", "Кукиш", "Кукла", "Кукуруза", "Кулон", "Куница", "Купол", "Купон", "Курага", "Курок",
    "Лабиринт", "Лаваш", "Лавина", "Лавка", "Лагуна", "Ладья", "Лазер", "Лама", "Лампа", "Ландыш",
    "Лапоть", "Ларек", "Лассо", "Ластик", "Латы", "Лафет", "Лачуга", "Лебедка", "Леденец", "Лезвие",
    "Лейка", "Леска", "Лестница", "Лецитин", "Лифт", "Лиана", "Ливень", "Лимон", "Линейка", "Линза",
    "Липучка", "Лира", "Лист", "Лифт", "Лодка", "Ложка", "Локон", "Локомотив", "Локоть", "Лом",
    "Лопата", "Лопух", "Лорнет", "Лосьон", "Лотос", "Лоток", "Лошадь", "Луковица", "Луна", "Лупа",
    "Люстра", "Люк", "Лямка", "Магнит", "Мазут", "Макароны", "Макет", "Малахит", "Малина", "Мангал",
    "Мандарин", "Манекен", "Манжета", "Манифест", "Манометр", "Мансарда", "Мантия", "Манускрипт", "Маргарин", "Мармелад",
    "Маршрут", "Маска", "Масло", "Мачта", "Маятник", "Медальон", "Медведь", "Медуза", "Мел", "Мельница",
    "Метла", "Метро", "Мешок", "Миксер", "Мишень", "Монета", "Монокль", "Мольберт", "Мотор", "Мумия",
    "Мундштук", "Муфта", "Мухомор", "Мышеловка", "Мяч", "Наковальня", "Наперсток", "Нарды", "Наручники", "Насос",
    "Шахматы", "Шлем", "Шторм", "Шприц", "Щетка", "Щит", "Экскаватор", "Эликсир", "Эмблема", "Эфир",
    "Юбка", "Юла", "Юмор", "Ядро", "Якорь", "Яма", "Янтарь", "Ящик"
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
# ЛОГИКА ОЧИСТКИ
# ========================
def safe_delete(chat_id, message_id):
    try: bot.delete_message(chat_id, message_id)
    except: pass

def send_new(chat_id, text, reply_markup=None, parse_mode="Markdown"):
    if chat_id in last_messages:
        safe_delete(chat_id, last_messages[chat_id])
    msg = bot.send_message(chat_id, text, reply_markup=reply_markup, parse_mode=parse_mode)
    last_messages[chat_id] = msg.message_id
    return msg

def get_real_lobby(user_id):
    lid = user_lobbies.get(user_id)
    if lid and lid in lobbies: return lid
    return None

def dissolve_lobby(lobby_id):
    if lobby_id not in lobbies: return
    players = list(lobbies[lobby_id]['players'].keys())
    for cid, mid in lobbies[lobby_id].get('system_msgs', []): safe_delete(cid, mid)
    for cid, mid in lobbies[lobby_id].get('msgs', []): safe_delete(cid, mid)
    for p_id in players:
        user_lobbies.pop(p_id, None)
        user_states.pop(p_id, None)
        if p_id in last_messages: safe_delete(p_id, last_messages[p_id])
        bot.send_message(p_id, "❌ Лобби закрыто.")
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
    bot.send_message(message.chat.id, "⬇️ Меню активно", reply_markup=start_kb)
    send_new(message.chat.id, "🎭 *Чудо Оолаха приветствует тебя!*", reply_markup=kb_main())

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'entering_code')
def handle_code(message):
    uid, code = message.from_user.id, message.text.strip()
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
        else: bot.send_message(uid, "❌ Мест нет!")
    else: bot.send_message(uid, "❌ Код не найден!")

@bot.message_handler(func=lambda m: not m.text.startswith('/'))
def block_text(message):
    safe_delete(message.chat.id, message.message_id)

# ========================
# CALLBACKS
# ========================
@bot.callback_query_handler(func=lambda call: True)
def handle_cb(call):
    chat_id, uid, mid, data = call.message.chat.id, call.from_user.id, call.message.message_id, call.data
    try: bot.answer_callback_query(call.id)
    except: pass

    # --- Главное ---
    if data == "go_main":
        offline_games.pop(uid, None)
        lid = get_real_lobby(uid)
        if lid: dissolve_lobby(lid)
        send_new(chat_id, "🎭 *Главное меню*", reply_markup=kb_main())

    elif data == "online_mode":
        send_new(chat_id, "🌐 *Онлайн режим*\nСоздай лобби или введи код друга.", reply_markup=kb_online_menu())

    # --- Создание онлайн ---
    elif data == "create_game":
        lid = str(random.randint(100000, 999999))
        lobbies[lid] = {'host_id': uid, 'players': {uid: call.from_user.first_name}, 'settings': {'players_count': 3, 'spies_count': 1, 'theme': THEME_KEYS[0]}, 'data': {}, 'msgs': [], 'system_msgs': [], 'started': False}
        user_lobbies[uid] = lid
        m = types.InlineKeyboardMarkup(row_width=4)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_p_{i}") for i in range(3, 11)])
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="online_mode"))
        send_new(chat_id, f"🎲 *Лобби `{lid}`*\n\n1️⃣ Сколько игроков?", reply_markup=m)

    elif data.startswith("set_p_"):
        n = int(data.split("_")[2]); lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['players_count'] = n
            m = types.InlineKeyboardMarkup(row_width=3)
            m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_s_{i}") for i in range(1, min(n, 5))])
            m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="create_game"))
            send_new(chat_id, f"2️⃣ Сколько шпионов?", reply_markup=m)

    elif data.startswith("set_s_"):
        n = int(data.split("_")[2]); lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['spies_count'] = n
            m = types.InlineKeyboardMarkup()
            for i, t in enumerate(THEME_KEYS): m.add(types.InlineKeyboardButton(t, callback_data=f"set_t_{i}"))
            m.add(types.InlineKeyboardButton("🔙 Назад", callback_data=f"set_p_{lobbies[lid]['settings']['players_count']}"))
            send_new(chat_id, "3️⃣ Выбери тему:", reply_markup=m)

    elif data.startswith("set_t_"):
        idx = int(data.split("_")[2]); lid = get_real_lobby(uid)
        if lid:
            lobbies[lid]['settings']['theme'] = THEME_KEYS[idx]
            m = types.InlineKeyboardMarkup(); m.add(types.InlineKeyboardButton("❌ Отмена", callback_data="go_main"))
            send_new(chat_id, f"✅ *Лобби `{lid}` готово!*\nДай код друзьям. Ждем игроков...", reply_markup=m)

    elif data == "join_game":
        user_states[uid] = 'entering_code'
        send_new(chat_id, "🔑 *Введи 6-значный код:*", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔙 Назад", callback_data="online_mode")))

    # --- Оффлайн ---
    elif data == "off_start" or data == "off_back_players":
        offline_games[uid] = {'players': 3, 'spies': 1, 'theme': THEME_KEYS[0], 'cur': 0}
        m = types.InlineKeyboardMarkup(row_width=4)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_p_{i}") for i in range(3, 11)])
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="go_main"))
        send_new(chat_id, "📱 *Оффлайн*\n\n1️⃣ Сколько игроков?", reply_markup=m)

    elif data.startswith("off_p_") or data == "off_back_spies":
        if data.startswith("off_p_"): offline_games[uid]['players'] = int(data.split("_")[2])
        p = offline_games[uid]['players']
        m = types.InlineKeyboardMarkup(row_width=3)
        m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_s_{i}") for i in range(1, min(p, 5))])
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="off_back_players"))
        send_new(chat_id, f"2️⃣ Сколько шпионов?", reply_markup=m)

    elif data.startswith("off_s_") or data == "off_back_themes":
        if data.startswith("off_s_"): offline_games[uid]['spies'] = int(data.split("_")[2])
        m = types.InlineKeyboardMarkup()
        for i, t in enumerate(THEME_KEYS): m.add(types.InlineKeyboardButton(t, callback_data=f"off_t_{i}"))
        m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="off_back_spies"))
        send_new(chat_id, "3️⃣ Выбери тему:", reply_markup=m)

    elif data.startswith("off_t_"):
        og = offline_games[uid]; og['theme'] = THEME_KEYS[int(data.split("_")[2])]
        word = random.choice(THEMES[og['theme']])
        spy_idx = random.sample(range(og['players']), og['spies'])
        og['roles'] = [{'is_spy': i in spy_idx, 'word': word} for i in range(og['players'])]
        off_show_turn(uid, chat_id)

    elif data == "off_show":
        og = offline_games[uid]; role = og['roles'][og['cur']]
        txt = "🕵️ *ТЫ ШПИОН!*" if role['is_spy'] else f"✅ *Мирный*\n\nТема: {og['theme']}\nЗагадано: *{role['word']}*"
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="off_next"))
        send_new(chat_id, f"👤 *Игрок {og['cur']+1}*\n\n{txt}", reply_markup=m)

    elif data == "off_next":
        offline_games[uid]['cur'] += 1; off_show_turn(uid, chat_id)

    elif data == "off_restart":
        og = offline_games[uid]; word = random.choice(THEMES[og['theme']])
        spy_idx = random.sample(range(og['players']), og['spies'])
        og['roles'] = [{'is_spy': i in spy_idx, 'word': word} for i in range(og['players'])]; og['cur'] = 0
        off_show_turn(uid, chat_id)

    # --- Игровые кнопки ---
    elif data == "show_card":
        lid = get_real_lobby(uid); pd = lobbies[lid]['data'].get(uid)
        txt = "🕵️ *ШПИОН!*" if pd['is_spy'] else f"✅ *Мирный*\n\n📂 {pd['theme_name']}\n🎯 *{pd['card_name']}*"
        send_new(chat_id, txt, reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="hide_card")))

    elif data == "hide_card":
        send_new(chat_id, "🔒 Скрыто.", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("👁️ Роль", callback_data="show_card")))

    elif data == "restart_game":
        lid = get_real_lobby(uid); clear_lobby_messages(lid); start_distribution(lid)

    elif data == "main_menu":
        lid = get_real_lobby(uid); if lid: dissolve_lobby(lid)
        send_new(chat_id, "🎭 *Главное меню*", reply_markup=kb_main())

def off_show_turn(uid, chat_id):
    og = offline_games[uid]
    if og['cur'] < og['players']:
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton(f"👁️ Игрок {og['cur']+1}", callback_data="off_show"))
        send_new(chat_id, f"📱 Передай Игроку {og['cur']+1}", reply_markup=m)
    else:
        m = types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("🔄 Заново", callback_data="off_restart")).add(types.InlineKeyboardButton("🏠 Меню", callback_data="go_main"))
        send_new(chat_id, "✅ Начинайте игру!", reply_markup=m)

def clear_lobby_messages(lid):
    if lid in lobbies:
        for cid, mid in lobbies[lid].get('system_msgs', []): safe_delete(cid, mid)
        lobbies[lid]['system_msgs'] = []

def start_distribution(lid):
    l = lobbies[lid]; l['started'] = True; p_ids = list(l['players'].keys())
    spies = set(random.sample(p_ids, l['settings']['spies_count']))
    theme = l['settings']['theme']; word = random.choice(THEMES[theme])
    for p_id in p_ids:
        l['data'][p_id] = {'is_spy': p_id in spies, 'card_name': word, 'theme_name': theme}
        msg = bot.send_message(p_id, "🎮 *Раунд начался!*", parse_mode="Markdown", reply_markup=types.InlineKeyboardMarkup().add(types.InlineKeyboardButton("👁️ Роль", callback_data="show_card")))
        l.setdefault('msgs', []).append((p_id, msg.message_id))
        msg2 = bot.send_message(p_id, "⬇️ Управление:", reply_markup=kb_game_controls())
        l.setdefault('msgs', []).append((p_id, msg2.message_id))

if __name__ == '__main__':
    try:
        bot.remove_webhook()
        print("Чудо Оолаха готово!", flush=True)
        bot.infinity_polling(timeout=20)
    except Exception as e:
        print(f"Ошибка: {e}")
