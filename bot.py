import telebot
from telebot import types
import random
import logging
import threading

# ========================
# НАСТРОЙКИ
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
# МОБЫ МАЙНКРАФТА
# ========================
MC_MOBS = [
    "Зомби", "Скелет", "Крипер", "Паук", "Эндермен",
    "Слизень", "Ведьма", "Визер", "Визер-скелет",
    "Страж", "Древний страж", "Шалкер", "Вызыватель",
    "Поборник", "Разоритель", "Вредина", "Фантом",
    "Утопленник", "Бродяга", "Разбойник", "Чародей",
    "Блейз", "Гаст", "Магмовый куб", "Серебряная рыбка",
    "Чешуйница Края", "Зоглин", "Пиглин-дикарь",
    "Хранитель", "Надзиратель", "Пещерный паук",
    "Крипер заряженный", "Страйдер",
    "Пчела", "Волк", "Железный голем", "Зомбифицированный пиглин",
    "Пиглин", "Лама", "Белый медведь", "Дельфин", "Панда",
    "Корова", "Свинья", "Овца", "Курица", "Кролик",
    "Лошадь", "Осёл", "Мул", "Кошка", "Оцелот",
    "Попугай", "Черепаха", "Лиса", "Треска", "Лосось",
    "Тропическая рыба", "Иглобрюх", "Кальмар",
    "Светящийся кальмар", "Аксолотль", "Козёл",
    "Лягушка", "Головастик", "Аллай", "Верблюд",
    "Нюхач", "Броненосец", "Житель",
    "Странствующий торговец", "Снеговик",
    "Хоглин", "Летучая мышь", "Бриз",
    "Дракон Края", "Визер-босс"
]

# ========================
# КС2 КАРТЫ
# ========================
CS_MAPS = [
    "Dust 2", "Mirage", "Inferno", "Nuke", "Overpass",
    "Ancient", "Anubis", "Vertigo", "Train", "Cache",
    "Cobblestone", "Office", "Italy", "AWP Lego", "2000$"
]

# ========================
# КС2 ОРУЖИЕ
# ========================
CS_WEAPONS = [
    "Glock-18", "USP-S", "P2000", "P250", "Five-SeveN",
    "Tec-9", "CZ75-Auto", "Dual Berettas", "Desert Eagle", "R8 Revolver",
    "Nova", "XM1014", "MAG-7", "Sawed-Off",
    "MAC-10", "MP9", "MP7", "MP5-SD", "UMP-45",
    "PP-Bizon", "P90",
    "AK-47", "M4A4", "M4A1-S", "Galil AR", "FAMAS",
    "SG 553", "AUG",
    "AWP", "SSG 08", "SCAR-20", "G3SG1",
    "M249", "Negev",
    "Zeus x27", "Нож",
    "Дымовая граната", "Осколочная граната", "Молотов",
    "Зажигательная граната", "Световая граната", "Декой"
]

# ========================
# ПРОФЕССИИ (200)
# ========================
PROFESSIONS = [
    "Врач", "Хирург", "Стоматолог", "Педиатр", "Терапевт",
    "Окулист", "Психолог", "Психиатр", "Ветеринар", "Медсестра",
    "Учитель", "Преподаватель", "Воспитатель", "Репетитор", "Тренер",
    "Логопед", "Дефектолог", "Директор школы", "Декан", "Профессор",
    "Программист", "Дизайнер", "Веб-разработчик", "Тестировщик", "Сисадмин",
    "Аналитик", "Data Scientist", "DevOps", "Хакер", "Геймдизайнер",
    "Повар", "Шеф-повар", "Кондитер", "Пекарь", "Бариста",
    "Бармен", "Официант", "Сомелье", "Мясник", "Сушист",
    "Полицейский", "Детектив", "Следователь", "Судья", "Адвокат",
    "Прокурор", "Нотариус", "Юрист", "Пристав", "Криминалист",
    "Пожарный", "Спасатель", "Сапёр", "Охранник", "Телохранитель",
    "Военный", "Снайпер", "Пилот", "Танкист", "Моряк",
    "Космонавт", "Астроном", "Физик", "Химик", "Биолог",
    "Математик", "Геолог", "Археолог", "Историк", "Географ",
    "Журналист", "Репортёр", "Блогер", "Ведущий", "Диктор",
    "Оператор", "Режиссёр", "Продюсер", "Сценарист", "Монтажёр",
    "Актёр", "Каскадёр", "Клоун", "Фокусник", "Цирковой артист",
    "Певец", "Рэпер", "Диджей", "Гитарист", "Барабанщик",
    "Пианист", "Скрипач", "Дирижёр", "Композитор", "Звукорежиссёр",
    "Художник", "Скульптор", "Фотограф", "Иллюстратор", "Граффитист",
    "Архитектор", "Строитель", "Каменщик", "Плотник", "Сварщик",
    "Электрик", "Сантехник", "Маляр", "Штукатур", "Кровельщик",
    "Водитель", "Таксист", "Дальнобойщик", "Машинист", "Пилот самолёта",
    "Капитан корабля", "Стюардесса", "Проводник", "Курьер", "Почтальон",
    "Фермер", "Агроном", "Садовник", "Лесник", "Рыбак",
    "Охотник", "Пчеловод", "Доярка", "Тракторист", "Комбайнёр",
    "Бухгалтер", "Экономист", "Банкир", "Трейдер", "Брокер",
    "Страховщик", "Аудитор", "Кассир", "Инкассатор", "Финансист",
    "Менеджер", "Маркетолог", "Рекламщик", "PR-менеджер", "HR-менеджер",
    "Риелтор", "Логист", "Товаровед", "Мерчандайзер", "Продавец",
    "Парикмахер", "Стилист", "Визажист", "Косметолог", "Массажист",
    "Мастер маникюра", "Татуировщик", "Портной", "Швея", "Модельер",
    "Модель", "Манекенщица", "Фитнес-тренер", "Диетолог", "Йога-инструктор",
    "Футболист", "Хоккеист", "Баскетболист", "Теннисист", "Боксёр",
    "Борец", "Гимнаст", "Пловец", "Лыжник", "Фигурист",
    "Шахматист", "Киберспортсмен", "Комментатор", "Судья спортивный", "Тренер спортивный",
    "Священник", "Монах", "Имам", "Раввин", "Миссионер",
    "Дипломат", "Посол", "Политик", "Депутат", "Президент",
    "Губернатор", "Мэр", "Министр", "Переводчик", "Лингвист",
    "Библиотекарь", "Музейный работник", "Экскурсовод", "Гид", "Аниматор"
]

# ========================
# РАНДОМ 1000 ВЕЩЕЙ
# ========================
RANDOM_THINGS = [
    "Нога", "Рука", "Палец", "Голова", "Нос", "Ухо", "Глаз", "Зуб", "Язык", "Колено",
    "Локоть", "Пятка", "Лоб", "Щека", "Подбородок", "Шея", "Плечо", "Спина", "Живот", "Пупок",
    "Ноготь", "Бровь", "Ресница", "Губа", "Кулак", "Ладонь", "Череп", "Ребро", "Позвоночник", "Мозг",
    "Хлеб", "Масло", "Сыр", "Колбаса", "Сосиска", "Пельмени", "Борщ", "Суп", "Каша", "Макароны",
    "Пицца", "Бургер", "Шаурма", "Сало", "Огурец", "Помидор", "Картошка", "Морковь", "Лук", "Чеснок",
    "Яблоко", "Банан", "Апельсин", "Лимон", "Арбуз", "Дыня", "Виноград", "Клубника", "Малина", "Вишня",
    "Торт", "Пирожок", "Блин", "Вафля", "Печенье", "Конфета", "Шоколад", "Мороженое", "Йогурт", "Кефир",
    "Молоко", "Сметана", "Творог", "Яйцо", "Рис", "Гречка", "Овсянка", "Мёд", "Варенье", "Сахар",
    "Соль", "Перец", "Уксус", "Майонез", "Кетчуп", "Горчица", "Соус", "Суши", "Ролл", "Лапша",
    "Вода", "Чай", "Кофе", "Сок", "Компот", "Лимонад", "Кола", "Квас", "Пиво", "Вино",
    "Водка", "Коктейль", "Смузи", "Какао", "Энергетик",
    "Собака", "Кошка", "Хомяк", "Попугай", "Рыбка", "Черепаха", "Кролик", "Мышь", "Крыса", "Ёжик",
    "Лошадь", "Корова", "Свинья", "Коза", "Овца", "Курица", "Утка", "Гусь", "Индюк", "Петух",
    "Лев", "Тигр", "Медведь", "Волк", "Лиса", "Заяц", "Олень", "Лось", "Жираф", "Слон",
    "Обезьяна", "Горилла", "Панда", "Коала", "Кенгуру", "Крокодил", "Змея", "Ящерица", "Лягушка", "Акула",
    "Кит", "Дельфин", "Осьминог", "Краб", "Медуза", "Пингвин", "Орёл", "Сова", "Ворона", "Голубь",
    "Муравей", "Пчела", "Бабочка", "Комар", "Муха", "Таракан", "Паук", "Скорпион", "Улитка", "Червяк",
    "Стул", "Стол", "Кровать", "Диван", "Шкаф", "Полка", "Зеркало", "Ковёр", "Занавеска", "Подушка",
    "Одеяло", "Матрас", "Лампа", "Люстра", "Розетка", "Выключатель", "Дверь", "Окно", "Стена", "Потолок",
    "Пол", "Крыша", "Лестница", "Балкон", "Забор", "Ворота", "Замок", "Ключ", "Звонок", "Почтовый ящик",
    "Плита", "Духовка", "Микроволновка", "Холодильник", "Чайник", "Тостер", "Блендер", "Мясорубка", "Сковорода", "Кастрюля",
    "Тарелка", "Чашка", "Стакан", "Ложка", "Вилка", "Нож кухонный", "Разделочная доска", "Половник", "Скалка", "Тёрка",
    "Футболка", "Рубашка", "Свитер", "Куртка", "Пальто", "Шуба", "Джинсы", "Штаны", "Шорты", "Юбка",
    "Платье", "Костюм", "Пиджак", "Галстук", "Носки", "Трусы", "Колготки", "Шапка",
    "Кепка", "Шарф", "Перчатки", "Варежки", "Ремень", "Кроссовки", "Туфли", "Ботинки", "Сапоги", "Тапочки",
    "Сандалии", "Шлёпанцы", "Очки", "Солнечные очки", "Часы", "Браслет", "Кольцо", "Серьги", "Цепочка", "Рюкзак",
    "Машина", "Автобус", "Трамвай", "Троллейбус", "Метро", "Поезд", "Самолёт", "Вертолёт", "Корабль", "Лодка",
    "Катер", "Яхта", "Велосипед", "Мотоцикл", "Скутер", "Самокат", "Скейтборд", "Ролики", "Санки", "Лыжи",
    "Коньки", "Снегоход", "Трактор", "Экскаватор", "Бульдозер", "Кран", "Грузовик", "Фура", "Карета", "Ракета",
    "Ручка", "Карандаш", "Тетрадь", "Учебник", "Дневник", "Линейка", "Ластик", "Точилка", "Пенал", "Портфель",
    "Мел", "Доска", "Парта", "Глобус", "Карта мира", "Циркуль", "Транспортир", "Калькулятор", "Фломастер", "Краски",
    "Кисточка", "Альбом", "Ножницы", "Клей", "Скотч", "Степлер", "Скрепка", "Кнопка", "Папка", "Файл",
    "Телефон", "Смартфон", "Планшет", "Ноутбук", "Компьютер", "Монитор", "Клавиатура", "Мышка", "Наушники", "Колонка",
    "Телевизор", "Пульт", "Камера", "Фотоаппарат", "Принтер", "Сканер", "Флешка", "Жёсткий диск", "Провод", "Зарядка",
    "Батарейка", "Аккумулятор", "Фонарик", "Утюг", "Пылесос", "Стиральная машина", "Фен", "Бритва", "Кондиционер", "Вентилятор",
    "Дерево", "Куст", "Трава", "Цветок", "Роза", "Ромашка", "Тюльпан", "Подсолнух", "Кактус", "Гриб",
    "Мох", "Лист", "Ветка", "Корень", "Пень", "Бревно", "Камень", "Песок", "Глина", "Земля",
    "Гора", "Холм", "Овраг", "Река", "Озеро", "Море", "Океан", "Водопад", "Болото", "Остров",
    "Пещера", "Вулкан", "Ледник", "Пустыня", "Лес", "Поле", "Луг", "Степь", "Тундра", "Джунгли",
    "Облако", "Туча", "Дождь", "Снег", "Град", "Молния", "Гром", "Радуга", "Ветер", "Торнадо",
    "Солнце", "Луна", "Звезда", "Планета", "Комета", "Метеорит",
    "Мяч", "Кукла", "Машинка", "Конструктор", "Пазл", "Кубик Рубика", "Юла", "Плюшевый мишка", "Солдатик",
    "Настольная игра", "Шахматы", "Шашки", "Домино", "Карты", "Дартс", "Бильярд", "Боулинг", "Воздушный змей", "Фрисби",
    "Качели", "Горка", "Карусель", "Батут", "Песочница", "Водный пистолет", "Пузыри мыльные", "Лего", "Барби", "Трансформер",
    "Молоток", "Гвоздь", "Шуруп", "Отвёртка", "Пила", "Топор", "Лопата", "Грабли", "Метла", "Ведро",
    "Швабра", "Тряпка", "Губка", "Верёвка", "Цепь", "Крючок", "Гаечный ключ", "Плоскогубцы", "Дрель", "Болгарка",
    "Рулетка", "Уровень", "Наждачка", "Клещи", "Тиски", "Паяльник", "Шланг", "Насос", "Домкрат", "Лом",
    "Гитара", "Барабан", "Пианино", "Скрипка", "Флейта", "Труба", "Саксофон", "Аккордеон", "Балалайка", "Бубен",
    "Маракас", "Арфа", "Виолончель", "Контрабас", "Губная гармошка", "Укулеле", "Банджо", "Орган", "Синтезатор", "Ксилофон",
    "Школа", "Больница", "Магазин", "Рынок", "Аптека", "Банк", "Почта", "Библиотека", "Музей", "Театр",
    "Кинотеатр", "Цирк", "Зоопарк", "Парк", "Площадь", "Вокзал", "Аэропорт", "Порт", "Стадион", "Бассейн",
    "Спортзал", "Ресторан", "Кафе", "Бар", "Клуб", "Дискотека", "Церковь", "Мечеть", "Тюрьма", "Суд",
    "Полиция", "Пожарная часть", "Завод", "Фабрика", "Склад", "Гараж", "Автомойка", "Заправка", "Кладбище", "Свалка",
    "Какашка", "Ничего", "Пустота", "Тишина", "Воздух", "Огонь", "Дым", "Пепел", "Пыль", "Грязь",
    "Мусор", "Жвачка", "Сопли", "Слюна", "Слеза", "Пот", "Кровь", "Синяк", "Шрам", "Прыщ",
    "Тень", "Эхо", "Запах", "Вкус", "Боль", "Страх", "Смех", "Крик", "Шёпот", "Храп",
    "Икота", "Чихание", "Зевота", "Отрыжка", "Кашель", "Щекотка", "Мурашки",
    "Книга", "Газета", "Журнал", "Письмо", "Конверт", "Марка", "Открытка", "Фотография", "Картина", "Плакат",
    "Флаг", "Свеча", "Спички", "Зажигалка", "Пепельница", "Ваза", "Горшок", "Бутылка", "Банка", "Коробка",
    "Пакет", "Мешок", "Чемодан", "Сумка", "Кошелёк", "Зонт", "Веер", "Компас", "Бинокль", "Лупа",
    "Термометр", "Песочные часы", "Будильник", "Календарь", "Блокнот", "Магнит", "Пружина", "Болт", "Гайка",
    "Чипсы", "Сухарики", "Семечки", "Орехи", "Попкорн", "Сникерс", "Твикс", "Киткат", "Скитлс",
    "Леденец", "Зефир", "Пастила", "Халва", "Козинак", "Круассан", "Багет", "Лаваш", "Чебурек",
    "Самса", "Манты", "Хинкали", "Вареники", "Оладьи", "Сырник", "Запеканка", "Салат", "Винегрет", "Окрошка",
    "Футбольный мяч", "Баскетбольный мяч", "Теннисная ракетка", "Хоккейная клюшка", "Шайба",
    "Гантель", "Штанга", "Скакалка", "Обруч", "Турник", "Секундомер",
    "Спутник", "Телескоп", "Скафандр", "Астероид", "Чёрная дыра", "НЛО", "Инопланетянин",
    "Ёлка", "Снеговик", "Дед Мороз", "Снегурочка", "Подарок", "Гирлянда", "Фейерверк", "Хлопушка",
    "Воздушный шар", "Меч", "Щит", "Лук", "Стрела", "Копьё", "Корона", "Трон", "Дракон",
    "Единорог", "Эльф", "Гном", "Орк", "Тролль", "Волшебная палочка", "Зелье", "Свиток", "Сундук",
    "Мыло", "Шампунь", "Зубная щётка", "Зубная паста", "Полотенце", "Туалетная бумага", "Расчёска",
    "Бинт", "Пластырь", "Таблетка", "Шприц", "Градусник",
    "Наручники", "Дубинка", "Свисток", "Рация",
    "Светофор", "Дорожный знак", "Люк", "Лавочка", "Урна", "Фонарный столб",
    "Рельсы", "Мост", "Тоннель", "Маяк", "Якорь", "Спасательный круг",
    "Весло", "Парус", "Руль", "Педаль", "Колесо", "Шина", "Фара"
]

# ========================
# ЮМОР (200)
# ========================
HUMOR = [
    # Классика
    "Какашка", "Понос", "Пердёж", "Сопля", "Козявка",
    "Блевотина", "Жопа", "Пуп земли", "Говнюк", "Лох",
    "Даун", "Дебил", "Тупица", "Идиот", "Баран",
    "Осёл", "Бревно", "Пень", "Овощ", "Табуретка",

    # Халяль / Оолах
    "Халяль", "Харам", "Аллах акбар", "Машаллах", "Иншаллах",
    "Астагфируллах", "Субханаллах", "Бисмиллях", "Джаннат", "Джаханнам",
    "Шайтан", "Иблис", "Джинн", "Хиджаб", "Никаб",
    "Тасбих", "Намаз", "Вуду", "Закят", "Хадж",
    "Минарет", "Мечеть", "Имам", "Муэдзин", "Азан",
    "Коран", "Сура", "Аят", "Дуа", "Фатиха",

    # Чёрный юмор
    "Гроб", "Могила", "Скелет в шкафу", "Кладбище", "Призрак",
    "Зомби-апокалипсис", "Конец света", "Ядерная бомба", "Метеорит в лицо", "Падение с крыши",
    "Банановая кожура", "Кирпич на голову", "Наступил на лего", "Удар мизинцем", "Дверь в лицо",
    "Птица нагадила", "Голубь-террорист", "Кошка на лицо", "Собака съела домашку", "Хомяк сбежал",

    # Школа / жиза
    "Двойка", "Вызвали к доске", "Забыл домашку", "Контрольная", "ЕГЭ",
    "Шпаргалка", "Списал у соседа", "Учитель злой", "Перемена 5 минут", "Столовская котлета",
    "Школьный туалет", "Бабка у подъезда", "Сосед с дрелью", "Будильник в 6 утра", "Понедельник",

    # Интернет
    "Вайфай пропал", "Лагает интернет", "Завис компьютер", "Синий экран", "Батарея 1%",
    "Зарядка сломалась", "Наушник один работает", "Камера на созвоне", "Микрофон включён", "Скринил переписку",
    "Лайк бывшей", "Сторис в 3 часа ночи", "Голосовое на 5 минут", "Флексит в тиктоке", "Рофл",

    # Еда юмор
    "Шаурма с котом", "Доширак", "Бомж-пакет", "Кипяток в лицо", "Просрочка",
    "Плесневый хлеб", "Каша с комками", "Суп без соли", "Пересоленый борщ", "Горелый блин",
    "Подгоревшая сосиска", "Кетчуп на мороженое", "Майонез на арбуз", "Молоко с огурцом", "Пиво с молоком",

    # Люди
    "Бабушка с батоном", "Дед на жигулях", "Мамкин геймер", "Папа за молоком", "Сестра в ванной",
    "Брат-предатель", "Друг-крыса", "Сосед сверху", "Сосед снизу", "Тёща",
    "Свекровь", "Начальник", "Препод", "Одноклассник", "Бывшая",

    # Ситуации
    "Сел на жвачку", "Порвались штаны", "Забыл ключи", "Опоздал на автобус", "Застрял в лифте",
    "Наступил в лужу", "Промок под дождём", "Обгорел на солнце", "Комар в ухе", "Муха в супе",
    "Паук в ванной", "Таракан на кухне", "Мышь в доме", "Кот на шторе", "Собака на диване",

    # Рандом дичь
    "Летающий тапок", "Бабушкин ремень", "Мамин тапок", "Папин ремень", "Указка учителя",
    "Веник возмездия", "Швабра справедливости", "Сковорода судьбы", "Кастрюля на голове", "Ведро на ноге",
    "Носок потерялся", "Второй тапок", "Пульт под диваном", "Телефон в унитазе", "Ключи в холодильнике",
    "Кот на люстре", "Хомяк в стиралке", "Рыбка на полу", "Попугай ругается", "Собака на столе",

    # Оолах специал
    "Чудо Оолаха", "Оолах мощный", "Оолах всемогущий", "Благословение Оолаха", "Гнев Оолаха",
    "Тапок Оолаха", "Борода Оолаха", "Халат Оолаха", "Сандалии Оолаха", "Чай Оолаха"
]

MC_MOBS = list(set(MC_MOBS))
CS_MAPS = list(set(CS_MAPS))
CS_WEAPONS = list(set(CS_WEAPONS))
PROFESSIONS = list(set(PROFESSIONS))
RANDOM_THINGS = list(set(RANDOM_THINGS))
HUMOR = list(set(HUMOR))

THEMES = {
    "🧟 Майнкрафт (мобы)": MC_MOBS,
    "🗺 КС2 (карты)": CS_MAPS,
    "🔫 КС2 (оружие)": CS_WEAPONS,
    "👷 Профессии": PROFESSIONS,
    "🎲 Рандом": RANDOM_THINGS,
    "😂 Юмор": HUMOR
}
THEME_KEYS = list(THEMES.keys())

# ========================
# ВСПОМОГАТЕЛЬНЫЕ
# ========================

def safe_delete(chat_id, message_id):
    try:
        bot.delete_message(chat_id, message_id)
    except:
        pass

def track_msg(lobby_id, msg):
    if msg and lobby_id in lobbies:
        lobbies[lobby_id].setdefault('msgs', []).append((msg.chat.id, msg.message_id))

def clear_lobby_messages(lobby_id):
    if lobby_id not in lobbies:
        return
    for cid, mid in lobbies[lobby_id].get('msgs', []):
        safe_delete(cid, mid)
    lobbies[lobby_id]['msgs'] = []

def get_real_lobby(user_id):
    lid = user_lobbies.get(user_id)
    if lid and lid != "joining" and lid in lobbies:
        return lid
    return None

def dissolve_lobby(lobby_id, reason="Лобби закрыто."):
    if lobby_id not in lobbies:
        return
    players = list(lobbies[lobby_id]['players'].keys())
    clear_lobby_messages(lobby_id)
    clear_system_messages(lobby_id)
    for p_id in players:
        if user_lobbies.get(p_id) == lobby_id:
            user_lobbies.pop(p_id, None)
        user_states.pop(p_id, None)
    del lobbies[lobby_id]

def create_lobby(user_id, first_name):
    old = get_real_lobby(user_id)
    if old:
        dissolve_lobby(old)
    lobby_id = str(random.randint(100000, 999999))
    while lobby_id in lobbies:
        lobby_id = str(random.randint(100000, 999999))
    lobbies[lobby_id] = {
        'host_id': user_id,
        'players': {user_id: first_name},
        'settings': {'players_count': 3, 'spies_count': 1, 'theme': THEME_KEYS[0]},
        'data': {},
        'msgs': [],
        'system_msgs': [],
        'started': False
    }
    user_lobbies[user_id] = lobby_id
    return lobby_id

def track_system_msg(lobby_id, msg):
    if msg and lobby_id in lobbies:
        lobbies[lobby_id].setdefault('system_msgs', []).append((msg.chat.id, msg.message_id))

def clear_system_messages(lobby_id):
    if lobby_id not in lobbies:
        return
    for cid, mid in lobbies[lobby_id].get('system_msgs', []):
        safe_delete(cid, mid)
    lobbies[lobby_id]['system_msgs'] = []

def notify_all_system(lobby_id, text):
    if lobby_id not in lobbies:
        return
    for p_id in lobbies[lobby_id]['players']:
        try:
            msg = bot.send_message(p_id, text)
            track_system_msg(lobby_id, msg)
        except:
            pass

# ========================
# КЛАВИАТУРЫ
# ========================

def kb_main():
    m = types.InlineKeyboardMarkup(row_width=1)
    m.add(
        types.InlineKeyboardButton("📱 Оффлайн (1 телефон)", callback_data="offline_mode"),
        types.InlineKeyboardButton("🌐 Онлайн (по коду)", callback_data="online_mode")
    )
    return m

def kb_online_menu():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("Создать ➕", callback_data="create_game"),
        types.InlineKeyboardButton("Войти 🤝", callback_data="join_game")
    )
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="go_main"))
    return m

def kb_players():
    m = types.InlineKeyboardMarkup(row_width=4)
    m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_p_{i}") for i in range(3, 11)])
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_main"))
    return m

def kb_spies(pc):
    mx = min(pc - 1, 5)
    m = types.InlineKeyboardMarkup(row_width=3)
    m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"set_s_{i}") for i in range(1, mx + 1)])
    m.add(types.InlineKeyboardButton("🎲 Случайно", callback_data="set_s_random"))
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_players"))
    return m

def kb_themes():
    m = types.InlineKeyboardMarkup()
    for i, t in enumerate(THEME_KEYS):
        m.add(types.InlineKeyboardButton(t, callback_data=f"set_t_{i}"))
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_spies"))
    return m

def kb_lobby_wait():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🔙 Назад", callback_data="back_to_themes"),
        types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_lobby")
    )
    return m

def kb_show():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("👁️ Показать роль", callback_data="show_card"))
    return m

def kb_hide():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("🔒 Скрыть", callback_data="hide_card"))
    return m

def kb_game_controls():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🔄 Новый раунд", callback_data="restart_game"),
        types.InlineKeyboardButton("🏠 Выйти", callback_data="main_menu")
    )
    return m

def kb_join_code():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("❌ Отмена", callback_data="cancel_join"))
    return m

def kb_off_players():
    m = types.InlineKeyboardMarkup(row_width=4)
    m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_p_{i}") for i in range(3, 11)])
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="go_main"))
    return m

def kb_off_spies(pc):
    mx = min(pc - 1, 5)
    m = types.InlineKeyboardMarkup(row_width=3)
    m.add(*[types.InlineKeyboardButton(str(i), callback_data=f"off_s_{i}") for i in range(1, mx + 1)])
    m.add(types.InlineKeyboardButton("🎲 Случайно", callback_data="off_s_random"))
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="off_back_players"))
    return m

def kb_off_themes():
    m = types.InlineKeyboardMarkup()
    for i, t in enumerate(THEME_KEYS):
        m.add(types.InlineKeyboardButton(t, callback_data=f"off_t_{i}"))
    m.add(types.InlineKeyboardButton("🔙 Назад", callback_data="off_back_spies"))
    return m

def kb_off_show(num):
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton(f"👁️ Игрок {num} — Показать", callback_data="off_show"))
    return m

def kb_off_hide():
    m = types.InlineKeyboardMarkup()
    m.add(types.InlineKeyboardButton("🔒 Скрыть и передать", callback_data="off_next"))
    return m

def kb_off_done():
    m = types.InlineKeyboardMarkup(row_width=2)
    m.add(
        types.InlineKeyboardButton("🔄 Ещё раунд", callback_data="off_restart"),
        types.InlineKeyboardButton("🏠 Меню", callback_data="go_main")
    )
    return m

# ========================
# ТЕКСТЫ
# ========================

def text_welcome():
    return (
        "🎭 *Добро пожаловать в Чудо Оолаха!*\n\n"
        "📖 *Правила:*\n"
        "• Все узнают загаданное слово — *кроме Шпиона!*\n"
        "• Шпион знает только тему\n"
        "• Задавайте вопросы и ищите шпиона!\n\n"
        "Выбери режим 👇"
    )

def text_lobby(lobby_id, s):
    return (
        f"✅ *Лобби готово!*\n\n"
        f"🔑 Код: `{lobby_id}`\n"
        f"👥 Игроков: {s['players_count']}\n"
        f"🕵️ Шпионов: {s['spies_count']}\n"
        f"📂 Тема: {s['theme']}\n\n"
        f"📩 Отправь код друзьям!\n"
        f"⏳ Ожидание..."
    )

# ========================
# /start
# ========================

@bot.message_handler(commands=['start'])
def cmd_start(message):
    uid = message.from_user.id
    user_states.pop(uid, None)
    offline_games.pop(uid, None)
    start_kb = types.ReplyKeyboardMarkup(resize_keyboard=True)
    start_kb.add(types.KeyboardButton("/start"))
    bot.send_message(message.chat.id, "", reply_markup=start_kb)
    bot.send_message(message.chat.id, text_welcome(), parse_mode="Markdown", reply_markup=kb_main())

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) != 'entering_code' and not m.text.startswith('/'))
def block_text(message):
    safe_delete(message.chat.id, message.message_id)

# ========================
# ВВОД КОДА
# ========================

@bot.message_handler(func=lambda m: user_states.get(m.from_user.id) == 'entering_code')
def handle_code(message):
    uid = message.from_user.id
    code = message.text.strip()
    safe_delete(message.chat.id, message.message_id)

    if code not in lobbies:
        bot.send_message(message.chat.id, "❌ Неверный код:", reply_markup=kb_join_code())
        return

    lobby = lobbies[code]

    if lobby.get('started'):
        bot.send_message(message.chat.id, "⏳ Игра уже идёт!")
        user_states.pop(uid, None)
        return

    if uid in lobby['players']:
        bot.send_message(message.chat.id, "⚠️ Ты уже в лобби!")
        user_states.pop(uid, None)
        return

    if len(lobby['players']) >= lobby['settings']['players_count']:
        bot.send_message(message.chat.id, "❌ Лобби заполнено!")
        user_states.pop(uid, None)
        return

    old = get_real_lobby(uid)
    if old and old != code:
        lobbies[old]['players'].pop(uid, None)

    lobby['players'][uid] = message.from_user.first_name
    user_lobbies[uid] = code
    user_states.pop(uid, None)

    cur = len(lobby['players'])
    total = lobby['settings']['players_count']
    notify_all_system(code, f"➕ {message.from_user.first_name} зашёл! ({cur}/{total})")

    if cur == total:
        clear_system_messages(code)
        clear_lobby_messages(code)
        start_distribution(code)

# ========================
# КНОПКИ
# ========================

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

    try:
        # ========== ГЛАВНОЕ ==========
        if data == "go_main":
            offline_games.pop(uid, None)
            user_states.pop(uid, None)
            lid = get_real_lobby(uid)
            if lid:
                dissolve_lobby(lid)
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, text_welcome(), parse_mode="Markdown", reply_markup=kb_main())

        elif data == "online_mode":
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, "🌐 *Онлайн режим*", parse_mode="Markdown", reply_markup=kb_online_menu())

        # ========== ОФФЛАЙН ==========
        elif data == "offline_mode":
            offline_games[uid] = {'players': 3, 'spies': 1, 'theme': THEME_KEYS[0]}
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, "📱 *Оффлайн*\n\n1️⃣ Сколько игроков?", parse_mode="Markdown", reply_markup=kb_off_players())

        elif data.startswith("off_p_"):
            n = int(data.split("_")[2])
            offline_games.setdefault(uid, {})['players'] = n
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, f"2️⃣ Сколько шпионов? (макс. {min(n-1, 5)})", reply_markup=kb_off_spies(n))

        elif data.startswith("off_s_"):
            og = offline_games.get(uid, {})
            pc = og.get('players', 3)
            if data == "off_s_random":
                n = random.randint(1, min(pc - 1, 5))
            else:
                n = int(data.split("_")[2])
            og['spies'] = n
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, "3️⃣ Выбери тему:", reply_markup=kb_off_themes())

        elif data.startswith("off_t_"):
            idx = int(data.split("_")[2])
            og = offline_games.get(uid, {})
            og['theme'] = THEME_KEYS[idx]
            off_start_game(uid, chat_id, mid)

        elif data == "off_back_players":
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, "📱 *Оффлайн*\n\n1️⃣ Сколько игроков?", parse_mode="Markdown", reply_markup=kb_off_players())

        elif data == "off_back_spies":
            og = offline_games.get(uid, {})
            pc = og.get('players', 3)
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, f"2️⃣ Сколько шпионов? (макс. {min(pc-1, 5)})", reply_markup=kb_off_spies(pc))

        elif data == "off_show":
            og = offline_games.get(uid)
            if not og: return
            cur = og.get('current_player', 0)
            roles = og.get('roles', [])
            if cur >= len(roles): return
            role = roles[cur]
            safe_delete(chat_id, mid)
            if role['is_spy']:
                text = (
                    f"👤 *Игрок {cur + 1}*\n\n"
                    "🕵️ *ТЫ ШПИОН!*\n\n"
                    f"📂 Тема: *{og['theme']}*\n\n"
                    "❓ Ты НЕ знаешь что загадано\n"
                    "🤫 Запомни и передай телефон"
                )
            else:
                text = (
                    f"👤 *Игрок {cur + 1}*\n\n"
                    f"✅ *Ты мирный*\n\n"
                    f"📂 Тема: *{og['theme']}*\n"
                    f"🎯 Загадано: *{role['card']}*\n\n"
                    "🤫 Запомни и передай телефон"
                )
            bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb_off_hide())

        elif data == "off_next":
            og = offline_games.get(uid)
            if not og: return
            og['current_player'] = og.get('current_player', 0) + 1
            cur = og['current_player']
            roles = og.get('roles', [])
            safe_delete(chat_id, mid)
            if cur >= len(roles):
                bot.send_message(
                    chat_id,
                    "✅ *Все получили роли!*\n\n🎮 Начинайте обсуждение!",
                    parse_mode="Markdown", reply_markup=kb_off_done()
                )
            else:
                bot.send_message(
                    chat_id,
                    f"📱 *Передай телефон Игроку {cur + 1}*",
                    parse_mode="Markdown", reply_markup=kb_off_show(cur + 1)
                )

        elif data == "off_restart":
            og = offline_games.get(uid)
            if not og:
                safe_delete(chat_id, mid)
                bot.send_message(chat_id, text_welcome(), parse_mode="Markdown", reply_markup=kb_main())
                return
            off_start_game(uid, chat_id, mid)

        # ========== ОНЛАЙН ==========
        elif data == "create_game":
            lid = create_lobby(uid, call.from_user.first_name)
            safe_delete(chat_id, mid)
            msg = bot.send_message(
                chat_id, f"🎲 *Комната `{lid}` создана*\n\n1️⃣ Сколько игроков?",
                parse_mode="Markdown", reply_markup=kb_players()
            )
            track_msg(lid, msg)

        elif data.startswith("set_p_"):
            n = int(data.split("_")[2])
            lid = get_real_lobby(uid)
            if not lid: return
            lobbies[lid]['settings']['players_count'] = n
            if lobbies[lid]['settings']['spies_count'] >= n:
                lobbies[lid]['settings']['spies_count'] = 1
            safe_delete(chat_id, mid)
            msg = bot.send_message(chat_id, f"2️⃣ Сколько шпионов? (макс. {min(n-1, 5)})", reply_markup=kb_spies(n))
            track_msg(lid, msg)

        elif data.startswith("set_s_"):
            lid = get_real_lobby(uid)
            if not lid: return
            pc = lobbies[lid]['settings']['players_count']
            if data == "set_s_random":
                n = random.randint(1, min(pc - 1, 5))
            else:
                n = int(data.split("_")[2])
            lobbies[lid]['settings']['spies_count'] = n
            safe_delete(chat_id, mid)
            msg = bot.send_message(chat_id, "3️⃣ Выбери тему:", reply_markup=kb_themes())
            track_msg(lid, msg)

        elif data.startswith("set_t_"):
            idx = int(data.split("_")[2])
            lid = get_real_lobby(uid)
            if not lid: return
            lobbies[lid]['settings']['theme'] = THEME_KEYS[idx]
            safe_delete(chat_id, mid)
            msg = bot.send_message(chat_id, text_lobby(lid, lobbies[lid]['settings']), parse_mode="Markdown", reply_markup=kb_lobby_wait())
            track_msg(lid, msg)

        elif data == "back_to_main":
            lid = get_real_lobby(uid)
            if lid:
                dissolve_lobby(lid)
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, text_welcome(), parse_mode="Markdown", reply_markup=kb_main())

        elif data == "back_to_players":
            lid = get_real_lobby(uid)
            if not lid: return
            safe_delete(chat_id, mid)
            msg = bot.send_message(chat_id, f"🎲 *Комната `{lid}` создана*\n\n1️⃣ Сколько игроков?", parse_mode="Markdown", reply_markup=kb_players())
            track_msg(lid, msg)

        elif data == "back_to_spies":
            lid = get_real_lobby(uid)
            if not lid: return
            pc = lobbies[lid]['settings']['players_count']
            safe_delete(chat_id, mid)
            msg = bot.send_message(chat_id, f"2️⃣ Сколько шпионов? (макс. {min(pc-1, 5)})", reply_markup=kb_spies(pc))
            track_msg(lid, msg)

        elif data == "back_to_themes":
            lid = get_real_lobby(uid)
            if not lid: return
            safe_delete(chat_id, mid)
            msg = bot.send_message(chat_id, "3️⃣ Выбери тему:", reply_markup=kb_themes())
            track_msg(lid, msg)

        elif data == "cancel_lobby":
            lid = get_real_lobby(uid)
            if lid:
                dissolve_lobby(lid)
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, text_welcome(), parse_mode="Markdown", reply_markup=kb_main())

        elif data == "cancel_join":
            user_states.pop(uid, None)
            user_lobbies.pop(uid, None)
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, "🌐 *Онлайн режим*", parse_mode="Markdown", reply_markup=kb_online_menu())

        elif data == "join_game":
            user_states[uid] = 'entering_code'
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, "🔑 Введи 6-значный код:", reply_markup=kb_join_code())

        elif data == "show_card":
            lid = get_real_lobby(uid)
            if not lid: return
            pd = lobbies[lid]['data'].get(uid)
            if not pd: return
            safe_delete(chat_id, mid)
            if pd['is_spy']:
                text = (
                    "🕵️ *ТЫ ШПИОН!*\n\n"
                    f"📂 Тема: *{pd['theme_name']}*\n\n"
                    "❓ Ты НЕ знаешь что загадано\n"
                    "🤫 Притворяйся"
                )
            else:
                text = (
                    f"✅ *Ты мирный*\n\n"
                    f"📂 Тема: *{pd['theme_name']}*\n"
                    f"🎯 Загадано: *{pd['card_name']}*\n\n"
                    "🤫 Не говори вслух!"
                )
            msg = bot.send_message(chat_id, text, parse_mode="Markdown", reply_markup=kb_hide())
            track_msg(lid, msg)

        elif data == "hide_card":
            safe_delete(chat_id, mid)
            lid = get_real_lobby(uid)
            msg = bot.send_message(chat_id, "🔒 Скрыто.", reply_markup=kb_show())
            if lid:
                track_msg(lid, msg)

        elif data == "restart_game":
            lid = get_real_lobby(uid)
            if not lid: return
            if lobbies[lid]['host_id'] != uid:
                return
            clear_lobby_messages(lid)
            lobbies[lid]['started'] = False
            start_distribution(lid)

        elif data == "main_menu":
            lid = get_real_lobby(uid)
            if lid:
                lobby = lobbies[lid]
                if uid == lobby['host_id']:
                    dissolve_lobby(lid)
                else:
                    lobby['players'].pop(uid, None)
                    lobby['data'].pop(uid, None)
                    user_lobbies.pop(uid, None)
            safe_delete(chat_id, mid)
            bot.send_message(chat_id, text_welcome(), parse_mode="Markdown", reply_markup=kb_main())

    except Exception as e:
        log.error(f"Ошибка '{data}': {e}")

# ========================
# ОФФЛАЙН СТАРТ
# ========================

def off_start_game(uid, chat_id, mid):
    og = offline_games.get(uid)
    if not og: return

    pc = og.get('players', 3)
    sc = og.get('spies', 1)
    theme = og.get('theme', THEME_KEYS[0])
    word_list = THEMES.get(theme, MC_MOBS)
    card = random.choice(word_list)

    spy_indices = set(random.sample(range(pc), sc))
    roles = []
    for i in range(pc):
        roles.append({'is_spy': i in spy_indices, 'card': card})

    og['roles'] = roles
    og['card'] = card
    og['current_player'] = 0

    safe_delete(chat_id, mid)
    bot.send_message(
        chat_id,
        f"🎮 *Игра!*\n\n"
        f"👥 Игроков: {pc} | 🕵️ Шпионов: {sc}\n"
        f"📂 Тема: {theme}\n\n"
        f"📱 *Передай телефон Игроку 1*",
        parse_mode="Markdown", reply_markup=kb_off_show(1)
    )

# ========================
# ОНЛАЙН РАЗДАЧА
# ========================

def start_distribution(lobby_id):
    if lobby_id not in lobbies: return
    lobby = lobbies[lobby_id]
    lobby['started'] = True
    lobby['data'] = {}

    player_ids = list(lobby['players'].keys())
    settings = lobby['settings']
    spies = set(random.sample(player_ids, settings['spies_count']))

    theme_name = settings['theme']
    word_list = THEMES.get(theme_name, MC_MOBS)
    card_name = random.choice(word_list)

    for p_id in player_ids:
        is_spy = p_id in spies
        lobby['data'][p_id] = {
            'is_spy': is_spy,
            'card_name': card_name,
            'theme_name': theme_name
        }
        try:
            msg = bot.send_message(p_id, "🎮 *Раунд начался!*\nЖми кнопку.", parse_mode="Markdown", reply_markup=kb_show())
            track_msg(lobby_id, msg)
        except:
            pass

    for p_id in player_ids:
        try:
            msg = bot.send_message(p_id, "⬇️ *После обсуждения:*", parse_mode="Markdown", reply_markup=kb_game_controls())
            track_msg(lobby_id, msg)
        except:
            pass

# ========================
# ЗАПУСК
# ========================

if __name__ == '__main__':
    bot.remove_webhook()
    log.info("Чудо Оолаха запущен!")
    bot.polling(none_stop=True, skip_pending=True)