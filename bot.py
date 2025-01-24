import telebot
from PIL import Image, ImageOps, ImageFilter
import io
from telebot import types
import random  # Для выбора случайной шутки

TOKEN = '7585140510:AAH4vOvoVTp1tee5bamKriSUvZ6QKpy5MX4'
bot = telebot.TeleBot(TOKEN)

user_states = {}  # тут будем хранить информацию о действиях пользователя
# user_states[chat_id] будет хранить:
# - 'photo': ID изображения
# - 'ascii_chars': набор символов, введённый пользователем

# набор символов из которых составляем изображение
ASCII_CHARS = '@%#*+=-:. '

# Список шуток
JOKES = [
    "Почему программисты не любят природу? Слишком много багов.",
    "Сколько программистов нужно, чтобы заменить лампочку? Ни одного, это аппаратная проблема.",
    "Почему Python такой грустный? Потому что у него нет классов.",
    "Программист заходит в бар, заказывает 1 пиво, 0 пива и -1 пиво. Бармен говорит: 'Ты пьешь слишком много!'",
    "Почему программисты любят темную тему? Потому что светлая тема выжигает глаза!",
    "Программист женился на девушке, потому что она была 'совместима'.",
    "В чем разница между программистом и обычным человеком? Программист считает с нуля.",
    "Ошибка 404: шутка не найдена.",
    "Как программист расслабляется? Пишет код, который не запускается.",
    "Почему программисты всегда носят очки? Потому что они не могут найти 'C'."
]

# Список комплиментов
COMPLIMENTS = [
    "Ты сегодня выглядишь потрясающе!",
    "Ты — воплощение красоты и ума.",
    "У тебя невероятная улыбка!",
    "Ты вдохновляешь окружающих своим позитивом.",
    "Ты замечательный человек!",
    "Твоя доброта делает мир лучше.",
    "Ты способен достичь всего, чего захочешь!",
    "Ты просто сияешь сегодня!",
    "С тобой всегда приятно общаться.",
    "Ты делаешь этот мир ярче!"
]

def resize_image(image, new_width=100):
    width, height = image.size
    ratio = height / width
    new_height = int(new_width * ratio)
    return image.resize((new_width, new_height))


def grayify(image):
    return image.convert("L")


def image_to_ascii(image_stream: io.BytesIO, ascii_chars: str, new_width=40) -> str:
    """
    Преобразует изображение в ASCII-арт.

    :param image_stream: Поток изображения.
    :param ascii_chars: Набор символов для ASCII-арта.
    :param new_width: Ширина изображения в символах.
    :return: Строка ASCII-арта.
    """
    # Переводим в оттенки серого
    image = Image.open(image_stream).convert('L')

    # Меняем размер, сохраняя пропорции
    width, height = image.size
    aspect_ratio = height / float(width)
    new_height = int(aspect_ratio * new_width * 0.55)  # 0.55 так как буквы выше, чем шире
    img_resized = image.resize((new_width, new_height))

    # Преобразуем пиксели в ASCII
    img_str = pixels_to_ascii(img_resized, ascii_chars)
    img_width = img_resized.width

    # Ограничиваем длину ASCII-арта
    max_characters = 4000 - (new_width + 1)
    max_rows = max_characters // (new_width + 1)

    ascii_art = ""
    for i in range(0, min(max_rows * img_width, len(img_str)), img_width):
        ascii_art += img_str[i:i + img_width] + "\n"

    return ascii_art


def pixels_to_ascii(image: Image.Image, ascii_chars: str) -> str:
    """
    Конвертирует пиксели изображения в ASCII-символы на основе пользовательского набора.

    :param image: Изображение в градациях серого.
    :param ascii_chars: Строка с символами для преобразования.
    :return: Строка ASCII-символов.
    """
    pixels = image.getdata()
    characters = ""
    for pixel in pixels:
        characters += ascii_chars[pixel * len(ascii_chars) // 256]
    return characters


# Огрубляем изображение
def pixelate_image(image, pixel_size):
    image = image.resize(
        (image.size[0] // pixel_size, image.size[1] // pixel_size),
        Image.NEAREST
    )
    image = image.resize(
        (image.size[0] * pixel_size, image.size[1] * pixel_size),
        Image.NEAREST
    )
    return image

# Новая функция: инверсия цветов
def invert_colors(image: Image.Image) -> Image.Image:
    """
    Применяет инверсию цветов (негатив) к изображению.

    :param image: Исходное изображение.
    :return: Изображение с инверсией цветов.
    """
    return ImageOps.invert(image)  # Используем встроенную функцию из PIL


# Новая функция: отражение изображения
def mirror_image(image: Image.Image, direction: str) -> Image.Image:
    """
    Отражает изображение по горизонтали или вертикали.

    :param image: Исходное изображение.
    :param direction: Направление отражения ("horizontal" или "vertical").
    :return: Отраженное изображение.
    """
    if direction == "horizontal":
        return image.transpose(Image.FLIP_LEFT_RIGHT)  # Отражение по горизонтали
    elif direction == "vertical":
        return image.transpose(Image.FLIP_TOP_BOTTOM)  # Отражение по вертикали
    else:
        raise ValueError("Direction must be 'horizontal' or 'vertical'.")

# Функция: преобразование в тепловую карту
def convert_to_heatmap(image: Image.Image) -> Image.Image:
    """
    Преобразует изображение в тепловую карту.

    :param image: Исходное изображение.
    :return: Изображение в виде тепловой карты.
    """
    grayscale_image = image.convert("L")  # Преобразуем изображение в оттенки серого
    heatmap_image = ImageOps.colorize(grayscale_image, black="blue", white="red")  # Градиент от синего к красному
    return heatmap_image

# Новая функция: изменение размера изображения для стикера
def resize_for_sticker(image: Image.Image, max_size: int = 512) -> Image.Image:
    """
    Изменяет размер изображения для использования в качестве стикера.

    :param image: Исходное изображение.
    :param max_size: Максимальный размер измерения (по умолчанию 512 пикселей).
    :return: Изображение с измененным размером.
    """
    width, height = image.size
    scaling_factor = min(max_size / width, max_size / height)
    if scaling_factor >= 1:
        return image  # Если изображение уже меньше заданного размера, возвращаем его без изменений
    new_width = int(width * scaling_factor)
    new_height = int(height * scaling_factor)
    resized_image = image.resize((new_width, new_height), Image.Resampling.LANCZOS)  # Используем Resampling вместо ANTIALIAS
    return resized_image


@bot.message_handler(commands=['start', 'help'])
def send_welcome(message):
    bot.reply_to(message, "Send me an image, and I'll provide options for you!")


@bot.message_handler(content_types=['photo'])
def handle_photo(message):
    # Изменено: Запрашиваем у пользователя набор символов после получения изображения
    bot.reply_to(message, "I got your photo! Now, please send me the characters you want to use for ASCII art.\n"
                          "For example: @%#*+=-:. (default).")
    user_states[message.chat.id] = {'photo': message.photo[-1].file_id}


@bot.message_handler(content_types=['text'])
def handle_text(message):
    # Изменено: Обрабатываем текст, чтобы сохранить пользовательский набор символов
    chat_id = message.chat.id

    # Проверяем, есть ли у пользователя состояние с фото
    if chat_id in user_states and 'photo' in user_states[chat_id]:
        ascii_chars = message.text.strip()

        # Проверяем, что пользователь ввёл хотя бы 2 символа
        if len(ascii_chars) < 2:
            bot.reply_to(message, "Please provide at least two characters for the ASCII art.")
            return

        # Сохраняем набор символов в user_states
        user_states[chat_id]['ascii_chars'] = ascii_chars

        # Предлагаем пользователю выбрать действие
        bot.reply_to(message, "Got it! Now, choose what you'd like to do with your image:",
                     reply_markup=get_options_keyboard())
    else:
        bot.reply_to(message, "Please send me an image first.")


def get_options_keyboard():
    # Изменено: добавлена кнопка для подбрасывания монетки
    keyboard = types.InlineKeyboardMarkup()
    pixelate_btn = types.InlineKeyboardButton("Pixelate", callback_data="pixelate")
    ascii_btn = types.InlineKeyboardButton("ASCII Art", callback_data="ascii")
    invert_btn = types.InlineKeyboardButton("Invert Colors", callback_data="invert")
    mirror_horiz_btn = types.InlineKeyboardButton("Mirror Horizontally", callback_data="mirror_horizontal")
    mirror_vert_btn = types.InlineKeyboardButton("Mirror Vertically", callback_data="mirror_vertical")
    heatmap_btn = types.InlineKeyboardButton("Heatmap", callback_data="heatmap")
    resize_sticker_btn = types.InlineKeyboardButton("Resize for Sticker", callback_data="resize_sticker")
    joke_btn = types.InlineKeyboardButton("Random Joke", callback_data="random_joke")
    compliment_btn = types.InlineKeyboardButton("Random Compliment", callback_data="random_compliment")
    coin_flip_btn = types.InlineKeyboardButton("Flip a Coin", callback_data="flip_coin")  # Новая кнопка
    keyboard.add(pixelate_btn, ascii_btn, invert_btn)
    keyboard.add(mirror_horiz_btn, mirror_vert_btn)
    keyboard.add(heatmap_btn, resize_sticker_btn)
    keyboard.add(joke_btn, compliment_btn)
    keyboard.add(coin_flip_btn)  # Добавляем кнопку "Flip a Coin" на отдельный ряд
    return keyboard

@bot.callback_query_handler(func=lambda call: True)
def callback_query(call):
    if call.data == "pixelate":
        bot.answer_callback_query(call.id, "Pixelating your image...")
        pixelate_and_send(call.message)
    elif call.data == "ascii":
        bot.answer_callback_query(call.id, "Converting your image to ASCII art...")
        ascii_and_send(call.message)
    elif call.data == "invert":
        bot.answer_callback_query(call.id, "Inverting colors of your image...")
        invert_and_send(call.message)
    elif call.data == "mirror_horizontal":
        bot.answer_callback_query(call.id, "Mirroring your image horizontally...")
        mirror_and_send(call.message, "horizontal")
    elif call.data == "mirror_vertical":
        bot.answer_callback_query(call.id, "Mirroring your image vertically...")
        mirror_and_send(call.message, "vertical")
    elif call.data == "heatmap":
        bot.answer_callback_query(call.id, "Converting your image to a heatmap...")
        heatmap_and_send(call.message)
    elif call.data == "resize_sticker":
        bot.answer_callback_query(call.id, "Resizing your image for a sticker...")
        resize_sticker_and_send(call.message)
    elif call.data == "random_joke":
        bot.answer_callback_query(call.id, "Here's a joke for you!")
        send_random_joke(call.message)
    elif call.data == "random_compliment":
        bot.answer_callback_query(call.id, "Here's a compliment for you!")
        send_random_compliment(call.message)
    elif call.data == "flip_coin":  # Новая ветка для подбрасывания монетки
        bot.answer_callback_query(call.id, "Flipping a coin...")
        flip_coin_and_send(call.message)


def pixelate_and_send(message):
    photo_id = user_states[message.chat.id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    pixelated = pixelate_image(image, 20)

    output_stream = io.BytesIO()
    pixelated.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(message.chat.id, output_stream)


def ascii_and_send(message):
    # Изменено: Используем пользовательский набор символов
    chat_id = message.chat.id

    # Получаем данные о фото и наборе символов
    photo_id = user_states[chat_id]['photo']
    ascii_chars = user_states[chat_id].get('ascii_chars', ASCII_CHARS)  # Используем стандартный набор, если пользователь не указал свой

    # Загружаем изображение
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)

    # Преобразуем в ASCII-арт
    ascii_art = image_to_ascii(image_stream, ascii_chars)

    # Отправляем результат
    bot.send_message(chat_id, f"```\n{ascii_art}\n```", parse_mode="MarkdownV2")


# Новая функция: обработка инверсии цветов
def invert_and_send(message):
    """
    Применяет инверсию цветов к изображению и отправляет его пользователю.

    :param message: Сообщение Telegram.
    """
    chat_id = message.chat.id
    photo_id = user_states[chat_id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    inverted_image = invert_colors(image)
    output_stream = io.BytesIO()
    inverted_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(chat_id, output_stream)


# Новая функция: обработка отражения изображения
def mirror_and_send(message, direction: str):
    """
    Отражает изображение и отправляет его пользователю.

    :param message: Сообщение Telegram.
    :param direction: Направление отражения ("horizontal" или "vertical").
    """
    chat_id = message.chat.id
    photo_id = user_states[chat_id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    mirrored_image = mirror_image(image, direction)
    output_stream = io.BytesIO()
    mirrored_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(chat_id, output_stream)


# Новая функция: обработка тепловой карты
def heatmap_and_send(message):
    """
    Преобразует изображение в тепловую карту и отправляет его пользователю.

    :param message: Сообщение Telegram.
    """
    chat_id = message.chat.id
    photo_id = user_states[chat_id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)
    heatmap_image = convert_to_heatmap(image)
    output_stream = io.BytesIO()
    heatmap_image.save(output_stream, format="JPEG")
    output_stream.seek(0)
    bot.send_photo(chat_id, output_stream)

def resize_sticker_and_send(message):
    """
    Изменяет размер изображения для использования в качестве стикера и отправляет его пользователю.

    :param message: Сообщение Telegram.
    """
    chat_id = message.chat.id

    # Получаем ID изображения из состояния пользователя
    photo_id = user_states[chat_id]['photo']
    file_info = bot.get_file(photo_id)
    downloaded_file = bot.download_file(file_info.file_path)

    # Открываем изображение
    image_stream = io.BytesIO(downloaded_file)
    image = Image.open(image_stream)

    # Применяем изменение размера для стикера
    resized_image = resize_for_sticker(image)

    # Отправляем результат
    output_stream = io.BytesIO()
    resized_image.save(output_stream, format="PNG")  # Стикеры Telegram требуют формат PNG
    output_stream.seek(0)
    bot.send_document(chat_id, output_stream, visible_file_name="sticker.png")

def send_random_joke(message):
    """
    Отправляет случайную шутку пользователю.

    :param message: Сообщение Telegram.
    """
    chat_id = message.chat.id
    joke = random.choice(JOKES)  # Выбираем случайную шутку
    bot.send_message(chat_id, joke)  # Отправляем шутку пользователю

def send_random_compliment(message):
    """
    Отправляет случайный комплимент пользователю.

    :param message: Сообщение Telegram.
    """
    chat_id = message.chat.id
    compliment = random.choice(COMPLIMENTS)  # Выбираем случайный комплимент
    bot.send_message(chat_id, compliment)  # Отправляем комплимент пользователю

def flip_coin_and_send(message):
    """
    Симулирует подбрасывание монетки и отправляет результат пользователю.

    :param message: Сообщение Telegram.
    """
    chat_id = message.chat.id
    result = random.choice(["Орел", "Решка"])  # Случайный выбор между "Орел" и "Решка"
    bot.send_message(chat_id, f"Монета упала на: {result}")

bot.polling(none_stop=True)