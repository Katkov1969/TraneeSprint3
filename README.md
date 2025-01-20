Внесенные изменения:
1. Хранение пользовательского набора символов:
Добавлено поле 'ascii_chars' в user_states для хранения набора символов, введённого пользователем.

2. Запрос символов у пользователя.
Модифицирована функция handle_photo так, чтобы после получения изображения бот запрашивал у пользователя набор символов для ASCII-арта.

3. Обработка пользовательского ввода.
Добавлен новый обработчик текстовых сообщений (handle_text), который будет сохранять пользовательский набор символов проверяя его корректност

4. Использование пользовательских символов.
Функции pixels_to_ascii и image_to_ascii изменены так, чтобы принимать пользовательский набор символов.

5. Обработка отсутствия пользовательских символов.
Модификация функции ascii_and_send для использования пользовательских символов
Теперь функция ascii_and_send будет использовать набор символов, указанный пользователем.
Если пользователь не указывает набор символов, используется стандартный набор @%#*+=-:. .

Прмер выполнения
1. Введенное фото:
 ![Введенное фото](https://github.com/user-attachments/assets/54623512-f585-4d72-8ec4-ac04e9810128)
2. Результат:э
   ![Результат](https://github.com/user-attachments/assets/e0712c4b-89af-4143-b3cc-64506b4857ff)

 +++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
 ЗАДАНИЕ 2
Внесенные изменения:
1. Импорт ImageOps. Для инверсии цветов потребуется модуль ImageOps из Pillow.
Используется для инверсии цветов (ImageOps.invert).

2. Добавлена новая функциюя invert_colors, которая применяет инверсию цветов к изображению.
Реализует инверсию цветов, используя встроенную функцию из Pillow.

3. Добавлена кнопка "Invert Colors".
Обновлен функция get_options_keyboard, чтобы добавить новую кнопку для выбора инверсии цветов. Новая кнопка появляется в интерфейсе Telegram для выбора действия "инверсия цветов".

4.Обновлен обработчик callback_query.
Добавлена новая ветка для обработки нажатия кнопки "Invert Colors".

5. Добавлена новая функция invert_and_send.
Функция выполняет инверсию цветов изображения и отправляет результат пользователю.

Пример использования:
1. Исходное изображение
![Исходное изображение](https://github.com/user-attachments/assets/c6689f77-79d0-460b-ae2c-9c672fc6f83c)

2. Инверсия
![Инверсия и новая кнопка](https://github.com/user-attachments/assets/ecfc0337-fde1-4e02-b675-3d6005d65853)

+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 3
Внесенные изменения:
1. Добавлена функция mirror_image.
  Функция использует метод transpose из Pillow для отражения изображения по горизонтали (Image.FLIP_LEFT_RIGHT) или вертикали (Image.FLIP_TOP_BOTTOM).

2. Добпавлены кнопки для отражения.
 Добавлены кнопки "Mirror Horizontally" и "Mirror Vertically" в меню действий.

3. Изменен обработчик callback_query.
   Добавлены ветки для обработки действий "Mirror Horizontally" и "Mirror Vertically".

4. Добавлена функция mirror_and_send:
   Функция выполняет отражение изображения в указанном направлении и отправляет результат пользователю.

Пример использования:
![Исходное изображение](https://github.com/user-attachments/assets/6fbfccc9-77f1-4316-a3c5-d4d7bc13308d)

Горизонтальное отражение:
![Горизонтальная отражение](https://github.com/user-attachments/assets/2ba9775d-f1b1-4e62-b947-9cd226816670)

Вертикальное отражение:
![Вертикальное отражение](https://github.com/user-attachments/assets/1b2ea326-3ff7-4c59-af53-a526334fc135)


+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 4
Внесенные изменения:

1. Добавлена функция convert_to_heatmap:
  Функция преобразует изображение в оттенках серого в тепловую карту с использованием цветового градиента от синего (холодные области) до красного (теплые области).

2. Добавлена кнопка "Heatmap. 
  Новая кнопка для выбора преобразования изображения в тепловую карту добавлена в функцию get_options_keyboard.

3. Изменен обработчик callback_query:
    Добавлена новая ветка для обработки действия "Heatmap".

4. Добавлена новая функция heatmap_and_send.
    Функция преобразует изображение в тепловую карту и отправляет его пользователю.

Пример использования:
Исходное изображение:
![Исходное изображение](https://github.com/user-attachments/assets/d74617d1-68d2-4469-a5f6-b71b365abe81)

Тепловая карта:
![Тепловая карта](https://github.com/user-attachments/assets/be348016-b5ea-458b-b91e-367e169c3893)

+++++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 5
Внесенные изменения:

1. Добавлена функция resize_for_sticker:
Изменяет размер изображения, чтобы его максимальное измерение не превышало 512 пикселей, сохраняя пропорции.
Если изображение уже меньше 512 пикселей, размер не изменяется.

2. Добавлена кнопка "Resize for Sticker":
Добавлена новая кнопка для выбора функции изменения размера изображения для стикера.

3. Изменен обработчик callback_query:
Добавлена новая ветка для обработки действия "Resize for Sticker".

4. Добавлена новая функция resize_sticker_and_send:
Выполняет изменение размера изображения для стикера и отправляет результат в формате PNG.

Пример использования:
Исходное изображение:
![Исходное изображение](https://github.com/user-attachments/assets/9635ad99-cbe6-4fda-a066-de54f9263eaf)

Стикер:
![Добавлена кнопка и изменен размер изображения](https://github.com/user-attachments/assets/1a80870c-7271-4e3e-b75f-c76bddacb64c)

+++++++++++++++++++++++++++++++++++++++++++++++++
ЗАДАНИЕ 6 "Случайная шутка"
Внесенные изменения:
1. Добавлен список JOKES.
      Добавлен список шуток, из которого бот случайно выбирает шутку.
2. Добавлена кнопка  "Random Joke".
     Добавлена кнопка для выбора команды отправки случайной шутки.
3. Добавлена новая функция send_random_joke.
   Реализована функция для отправки случайной шутки пользователю.

Пример использования:
![Случайные шутки](https://github.com/user-attachments/assets/9994ed2e-0914-422a-a36d-93b9e1423629)









