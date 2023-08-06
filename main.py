import random
import time
import sqlite3
from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, InlineKeyboardMarkup, InlineKeyboardButton


# Здесь должен быть ваш токен Telegram бота
BOT_TOKEN = "6130093637:AAFotIhshAqeNMTtKuOXxd1qvbkTyFDC8Uo"

# Определение редкости и стоимости каждой карты
CARD_RARITIES = {
    "default": {"value": 100},
    "rare": {"value": 250},
    "epic": {"value": 500},
    "a": {"value": 100},
    "collection": {"value": 5000},
}

# Ссылки на изображения rare
image1 = "https://disk.yandex.ru/i/DmC1WQzluV3amg"
image2 = "https://disk.yandex.ru/i/7zY_OAfrtYMGwA"
image3 = "https://disk.yandex.ru/i/5UwTO2DhdN5sLw"
image4 = "https://disk.yandex.ru/i/QN0iTqQbbjN1CQ"
image5 = "https://disk.yandex.ru/i/nYcuJzBF0C0-XA"
image6 = "https://disk.yandex.ru/i/liiro4k6jwz2DA"
image7 = "https://disk.yandex.ru/i/-JdFcVLRIXNRww"
image8 = "https://disk.yandex.ru/i/xHOwxkmVlT0ing"
image9 = "https://disk.yandex.ru/i/fbE1fq2I-3qNXQ"
image10 = "https://disk.yandex.ru/i/2eK5Wv3d0YuteQ"
image11 = "https://disk.yandex.ru/i/cRQSHM0I09VrZw"
image12 = "https://disk.yandex.ru/i/uTRdoWEVczwSBQ"
image13 = "https://disk.yandex.ru/i/FqDZRLPSTeOXDQ"
image14 = "https://disk.yandex.ru/i/4H3qaCSeYdBd9A"
image15 = "https://disk.yandex.ru/i/leVkWaSE0e36HA"
image16 = "https://disk.yandex.ru/i/OAyArYIzy6gLMg"
image17 = "https://disk.yandex.ru/i/Uy5GlW43GXWjvg"
image18 = "https://disk.yandex.ru/i/TlNXr2yIeYDz6g"
image19 = "https://disk.yandex.ru/i/av1Znpc70IcgJA"
image20 = "https://disk.yandex.ru/i/EKth2aniRtcyQg"
image21 = "https://disk.yandex.ru/i/WHSdEDUjVjp7yQ"
image22 = "https://disk.yandex.ru/i/ieDjY0S26t2p2Q"
image23 = "https://disk.yandex.ru/i/d0uZz3VKb5YVUQ"
image24 = "https://disk.yandex.ru/i/ZEdwjijNFVWhzA"
image25 = "https://disk.yandex.ru/i/EptbQV2CnMdCHQ"
image26 = "https://disk.yandex.ru/i/fFGaSKl-RdXdjQ"
image27 = "https://disk.yandex.ru/i/ww4z2xPcw8M3xg"
image28 = "https://disk.yandex.ru/i/6Oq8sHRmr1RJLg"
image29 = "https://disk.yandex.ru/i/BEYauCvr5GfktQ"
image30 = "https://disk.yandex.ru/i/0ftVfV_1BOdrjQ"

# Модифицированный список карт, включающий редкость и стоимость
cards = [
    {"url": image1, "rarity": "rare"},
    {"url": image2, "rarity": "rare"},
    {"url": image3, "rarity": "rare"},
    {"url": image4, "rarity": "rare"},
    {"url": image5, "rarity": "rare"},
    {"url": image6, "rarity": "rare"},
    {"url": image7, "rarity": "rare"},
    {"url": image8, "rarity": "rare"},
    {"url": image9, "rarity": "rare"},
    {"url": image10, "rarity": "rare"},
    {"url": image11, "rarity": "rare"},
    {"url": image12, "rarity": "rare"},
    {"url": image13, "rarity": "rare"},
    {"url": image14, "rarity": "rare"},
    {"url": image15, "rarity": "rare"},
    {"url": image16, "rarity": "rare"},
    {"url": image17, "rarity": "rare"},
    {"url": image18, "rarity": "rare"},
    {"url": image19, "rarity": "rare"},
	{"url": image20, "rarity": "rare"},
    {"url": image21, "rarity": "rare"},
    {"url": image22, "rarity": "rare"},
    {"url": image23, "rarity": "rare"},
    {"url": image24, "rarity": "rare"},
    {"url": image25, "rarity": "rare"},
    {"url": image26, "rarity": "rare"},
    {"url": image27, "rarity": "rare"},
    {"url": image28, "rarity": "rare"},
    {"url": image29, "rarity": "rare"},
    {"url": image30, "rarity": "rare"},
]

# Создание подключения к базе данных и курсора
conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

# Обновите структуру таблицы, добавив новую колонку acquisition_time
cursor.execute('''CREATE TABLE IF NOT EXISTS user_cards
                  (user_id INTEGER, card_url TEXT, rarity TEXT, style INTEGER, acquisition_time INTEGER)''')
conn.commit()

trade_offers = {}

# Функция для проверки, прошло ли достаточно времени с момента последнего запроса карты
def can_get_new_card(user_id, crafting=False):
    cursor.execute("SELECT last_request_time FROM user_cards WHERE user_id=?", (user_id,))
    last_request_time = cursor.fetchone()

    if not last_request_time or last_request_time[0] is None:
        return True

    current_time = int(time.time())
    last_request_time = last_request_time[0]

    if crafting:
        return True

    next_request_time = last_request_time + 14400
    remaining_time = next_request_time - current_time
    return remaining_time <= 0



# Функция для форматирования времени в часы:минуты:секунды
def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}"


# Функция для обновления времени последнего запроса карты
def update_last_request_time(user_id, current_time):
    cursor.execute("UPDATE user_cards SET last_request_time=? WHERE user_id=?", (current_time, user_id))
    conn.commit()


bot = Bot(BOT_TOKEN)
dp = Dispatcher(bot=bot)

main = ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
main.add("Получить карту", "Мои карты").add("Spot Studio")

studio_list = InlineKeyboardMarkup(row_width=1)
studio_list.add(InlineKeyboardButton(text="Trade", callback_data="ttrraaddee"),
                InlineKeyboardButton(text="Игры", callback_data="game"),
                InlineKeyboardButton(text="Крафт", callback_data="craft_menu"))


@dp.message_handler(commands=["start"])
async def cmd_start(message: types.Message):
    await message.answer(f""" 
    🔥{message.from_user.first_name}, добро пожаловать в BRANDS🔥

💥Это простая игра по мотивам мировых брендов, идея взята со SPOT💥

👾Просто собирай карточки, соревнуйся с друзьями своими рейтингами и учавствуй в конкурсах на лимитированные карты👾

Думаю суть ясна, что-ж, пора начинать?🙂
    """,
                         reply_markup=main)


@dp.message_handler(text="Получить карту")
async def send_image(message: types.Message):
    user_id = message.from_user.id

    if not can_get_new_card(user_id):
        cursor.execute("SELECT last_request_time FROM user_cards WHERE user_id=?", (user_id,))
        last_request_time = cursor.fetchone()[0]
        next_request_time = last_request_time + 14400
        remaining_time = next_request_time - int(time.time())
        remaining_time_formatted = format_time(remaining_time)
        await message.answer(f"Следующая попытка будет доступна через: {remaining_time_formatted}.")
        return

    card = random.choice(cards)
    card_url = card["url"]
    card_rarity = card["rarity"]
    style_value = CARD_RARITIES[card_rarity]["value"]

    await bot.send_photo(chat_id=user_id, photo=card_url)

    current_time = int(time.time())
    cursor.execute(
        "INSERT INTO user_cards (user_id, card_url, rarity, style, acquisition_time) VALUES (?, ?, ?, ?, ?)",
        (user_id, card_url, card_rarity, style_value, current_time))
    conn.commit()

    update_last_request_time(user_id, current_time)  # Update last_request_time



@dp.message_handler(text="Мои карты")
async def show_user_cards(message: types.Message):
    cursor.execute("SELECT card_url, style FROM user_cards WHERE user_id=?", (message.from_user.id,))
    user_cards = cursor.fetchall()

    if user_cards:
        await show_user_card_with_keyboard(message.from_user.id, user_cards, 0)
    else:
        await message.answer("У вас пока нет сохраненных карт.")


async def show_user_card_with_keyboard(user_id, user_cards, current_index, message_id=None, trade_mode=False):
    card_url, style_value = user_cards[current_index]
    inline_keyboard = InlineKeyboardMarkup(row_width=3)

    if current_index > 0:
        inline_keyboard.insert(InlineKeyboardButton("⬅️ Назад", callback_data=f"card_{current_index - 1}"))

    cards_count = len(user_cards)
    current_card_index = current_index + 1
    inline_keyboard.insert(
        InlineKeyboardButton(f"Карта {current_card_index}/{cards_count}", callback_data="dummy")
    )

    if current_index < cards_count - 1:
        inline_keyboard.insert(InlineKeyboardButton("➡️ Вперед", callback_data=f"card_{current_index + 1}"))

    if trade_mode:  # Добавляем кнопку для обмена, если включен режим обмена
        inline_keyboard.add(InlineKeyboardButton("Предложить обмен", callback_data=f"trade_{current_index}"))

    media = types.InputMediaPhoto(card_url, caption=f"Style: {style_value}")

    if message_id is not None:
        await bot.edit_message_media(
            media=media, chat_id=user_id, message_id=message_id, reply_markup=inline_keyboard
        )
    else:
        await bot.send_photo(
            chat_id=user_id, photo=card_url, caption=f"Style: {style_value}", reply_markup=inline_keyboard
        )


@dp.callback_query_handler(lambda c: c.data.startswith('card_'))
async def show_next_card(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    current_index = int(callback_query.data.split('_')[1])

    cursor.execute("SELECT card_url, style FROM user_cards WHERE user_id=?", (user_id,))
    user_cards = cursor.fetchall()

    if 0 <= current_index < len(user_cards):
        await show_user_card_with_keyboard(user_id, user_cards, current_index, callback_query.message.message_id)
    else:
        await callback_query.answer("Карты закончились", show_alert=True)


@dp.message_handler(text="Spot Studio")
async def studio(message: types.Message):
    await message.answer("Добро пожаловать в студию!", reply_markup=studio_list)






@dp.callback_query_handler(text="craft_menu")
async def craft_menu(callback: types.CallbackQuery):
    await craft_menu_callback(callback)


def get_duplicate_counts(user_id):
    cursor.execute("SELECT rarity, COUNT(*) FROM user_cards WHERE user_id=? AND rarity!='default' GROUP BY rarity", (user_id,))
    duplicate_counts = dict(cursor.fetchall())
    for rarity in CARD_RARITIES.keys():
        duplicate_counts.setdefault(rarity, 0)
    return duplicate_counts

async def craft_menu_callback(callback: types.CallbackQuery):
    user_id = callback.from_user.id
    duplicate_counts = get_duplicate_counts(user_id)

    duplicate_counts_text = "\n".join([f"{rarity.capitalize()}: {count}" for rarity, count in duplicate_counts.items()])

    message_text = f"Количество повторных карт каждой редкости:\n{duplicate_counts_text}"

    await callback.message.answer(message_text, reply_markup=craft_keyboard)

def get_rarity_counts(user_id):
    cursor.execute("SELECT rarity, COUNT(*) FROM user_cards WHERE user_id=? GROUP BY rarity", (user_id,))
    rarity_counts = dict(cursor.fetchall())
    return rarity_counts



# Новые функции и обработчики для крафта
craft_keyboard = InlineKeyboardMarkup(row_width=1)
craft_keyboard.add(
    InlineKeyboardButton(text="Крафт из 5 Default", callback_data="craft_default"),
    InlineKeyboardButton(text="Крафт из 5 Rare", callback_data="craft_rare"),
    InlineKeyboardButton(text="Крафт из 5 Epic", callback_data="craft_epic")
)


@dp.message_handler(text="Крафт")
async def craft_start(message: types.Message):
    await message.answer("Выбери редкость для крафта:", reply_markup=craft_keyboard)


@dp.callback_query_handler(lambda c: c.data.startswith('craft_'))
async def craft_callback(callback_query: types.CallbackQuery):
    target_rarity = callback_query.data.split('_')[1]
    user_id = callback_query.from_user.id

    if target_rarity == "default":
        if not can_get_new_card(user_id):
            cursor.execute("SELECT last_request_time FROM user_cards WHERE user_id=?", (user_id,))
            last_request_time = cursor.fetchone()[0]
            next_request_time = last_request_time + 14400
            remaining_time = next_request_time - int(time.time())
            remaining_time_formatted = format_time(remaining_time)
            await callback_query.message.answer(f"Следующая попытка будет доступна через: {remaining_time_formatted}.")
            return

    craft_result = await craft_card(user_id, target_rarity)
    await callback_query.answer(craft_result, show_alert=True)

def increase_rarity(rarity):
    higher_rarities = ["rare", "epic"]
    if rarity in higher_rarities:
        higher_rarity = higher_rarities.index(rarity) + 1
        if higher_rarity < len(higher_rarities):
            return higher_rarities[higher_rarity]
    return rarity

def generate_new_card_url(target_rarity):
    higher_rarities = ["rare", "epic"]  # Список более высоких редкостей

    if target_rarity in higher_rarities:
        higher_rarity = higher_rarities.index(target_rarity) - 1
        new_rarity = higher_rarities[higher_rarity]
    else:
        new_rarity = random.choice(higher_rarities)  # Выбираем случайную более высокую редкость

    # Здесь вы можете генерировать новые ссылки на изображения для карт с нужной редкостью
    new_image_url = new_rarity
    return new_image_url


async def craft_card(user_id, target_rarity):
    cursor.execute("SELECT COUNT(*) FROM user_cards WHERE user_id=? AND rarity=?", (user_id, target_rarity))
    card_count = cursor.fetchone()[0]

    if card_count < 5:
        return "Недостаточно карт для крафта."

    # Получите список карт для крафта
    cursor.execute(
        "SELECT card_url FROM user_cards WHERE user_id=? AND rarity=? LIMIT 5", (user_id, target_rarity)
    )
    cards_for_craft = cursor.fetchall()

    # Удалите карты из базы данных
    cursor.execute(
        "DELETE FROM user_cards WHERE rowid IN (SELECT rowid FROM user_cards WHERE user_id=? AND rarity=? LIMIT 5)",
        (user_id, target_rarity)
    )
    conn.commit()

    # Создайте новую карту нужной редкости
    new_card_rarity = increase_rarity(target_rarity)
    new_card_url = generate_new_card_url(new_card_rarity)

    # Добавьте новую карту в базу данных
    current_time = int(time.time())
    cursor.execute(
        "INSERT INTO user_cards (user_id, card_url, rarity, style, last_request_time) VALUES (?, ?, ?, ?, ?)",
        (user_id, new_card_url, new_card_rarity, 0, current_time)
    )
    conn.commit()

    return f"Крафт завершен! Ваша новая карта: {new_card_url} (Редкость: {new_card_rarity.capitalize()})"

def increase_rarity(rarity):
    higher_rarities = ["rare", "epic"]
    if rarity in higher_rarities:
        higher_rarity = higher_rarities.index(rarity) + 1
        if higher_rarity < len(higher_rarities):
            return higher_rarities[higher_rarity]
    return rarity


# Остальная часть кода (обработчики и функции) остается без изменений

@dp.callback_query_handler(text="ttrraaddee")
async def start_trade(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id

    # Retrieve the user's cards from the database
    cursor.execute("SELECT card_url, rarity FROM user_cards WHERE user_id=?", (user_id,))
    user_cards = cursor.fetchall()

    # Show the user's collection and allow them to select cards for trade
    await show_user_card_with_keyboard(user_id, user_cards, 0, callback_query.message.message_id, trade_mode=True)


@dp.callback_query_handler(lambda c: c.data.startswith('trade_'))
async def start_trade(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    current_index = int(callback_query.data.split('_')[1])

    # Получаем список карт пользователя из базы данных
    cursor.execute("SELECT card_url, rarity FROM user_cards WHERE user_id=?", (user_id,))
    user_cards = cursor.fetchall()

    # Показываем коллекцию пользователя и позволяем выбрать карты для обмена
    await show_user_card_with_keyboard(user_id, user_cards, current_index, callback_query.message.message_id, trade_mode=True)


@dp.message_handler(lambda message: message.text.startswith('@'), state=None)
async def enter_username(message: types.Message):
    user_id = message.from_user.id
    username = message.text

    if user_id in trade_offers:
        cards_offered = trade_offers.pop(user_id)
        # Уведомляем другого пользователя о предложении обмена
        offer_message = f"Пользователь @{message.from_user.username} предлагает вам обмен:\n"
        for card in cards_offered:
            offer_message += f"- Карта редкости {card['rarity']}\n"
        inline_keyboard = InlineKeyboardMarkup()
        inline_keyboard.add(InlineKeyboardButton("Принять", callback_data=f"accept_{user_id}"),
                            InlineKeyboardButton("Отклонить", callback_data=f"reject_{user_id}"))
        await bot.send_message(username, offer_message, reply_markup=inline_keyboard)
    else:
        await message.reply("Нет активных предложений обмена для вас.")


@dp.callback_query_handler(lambda c: c.data.startswith('accept_') or c.data.startswith('reject_'))
async def respond_to_trade(callback_query: types.CallbackQuery):
    user_id = callback_query.from_user.id
    action = callback_query.data.split('_')[0]
    offerer_user_id = int(callback_query.data.split('_')[1])

    if action == 'accept':
        # Обновите владение картами для обоих пользователей (реализуйте эту логику)
        await bot.send_message(offerer_user_id, "Ваше предложение обмена было принято!")
        await callback_query.answer("Обмен принят!")
    elif action == 'reject':
        await bot.send_message(offerer_user_id, "Пользователь отклонил ваше предложение обмена.")
        await callback_query.answer("Обмен отклонен.")

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)