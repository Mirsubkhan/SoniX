from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

video_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"transcribe")],
    [InlineKeyboardButton(text="Трансформировать в ASCII", callback_data=f"transform_to_ascii")]
])

photo_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Трансформировать в ASCII", callback_data=f"transform_to_ascii")],
    [InlineKeyboardButton(text="Удалить фон", callback_data=f"remove_bg")]
])

audio_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"transcribe")],
    [InlineKeyboardButton(text="Извлечь вокал и фон", callback_data=f"separate")],
    [InlineKeyboardButton(text="Удалить шум", callback_data=f"remove_noise")],
])

return_as_file_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В .txt формате", callback_data=f"file")],
    [InlineKeyboardButton(text="В этом чате", callback_data=f"no_file")]
])

transform_options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В цветном формате", callback_data=f"color")],
    [InlineKeyboardButton(text="В черно-белом формате", callback_data=f"no_color")]
])

# TODO: Видео
"""
Извлечь текст:
- Проверяем, чтобы у видео была аудио-дорожка. Если её нет, предупреждаем пользователя;
- Проверяем, чтобы видео было длиной выше 5 секунд;
- Извлекаем аудио-дорожку;
- Выводим return_as_file_keyboard
- Если пользователь выбрал первое, тогда бот отправляет edit сообщение с прогресс баром из 10 🤍 (10% = 💚). В конце бот отправляет файл с результатом пользователю, удалив прогресс бар. Если же пользователь выбрал второе, тогда бот отправляет edit сообщение с динамичной транскрибацией аудио-дорожки. Если размер edit файла превысил более 4000 символов, тогда бот продолжает в следующем сообщении.
- ДОП: добавить кнопку отменить для того, чтобы отменить транскрибацию.

Извлечь аудио:
- Проверяем, чтобы у видео была аудио-дорожка. Если её нет, предупреждаем пользователя;
- Извлекаем аудио-дорожку в .wav и скидываем пользователю

Трансформировать в ascii:
- Проверяем, чтобы у видео была аудио-дорожка, если она есть - извлекаем.
- Выводим transform_options_keyboard
- Если пользователь выбрал первое, тогда бот отправляет в цветном формате, иначе в бесцветном. 
- Здесь уместно использовать edit сообщение с прогресс баром из 10 🤍 (10% = 💚). В конце бот отправляет файл с результатом пользователю, удалив прогресс бар.
- ДОП: добавить кнопку отменить для того, чтобы отменить трансформацию
"""

# TODO: Фото
"""
Трансформировать в ascii:
- Выводим transform_options_keyboard
- Если пользователь выбрал первое, тогда бот отправляет в цветном формате, иначе в бесцветном. 
- Здесь уместно использовать edit сообщение с прогресс баром из 10 🤍 (10% = 💚). В конце бот отправляет файл с результатом пользователю, удалив прогресс бар.
- ДОП: добавить кнопку отменить для того, чтобы отменить трансформацию

Удалить фон:
- Удаляем фон и скидываем
"""

# TODO: Аудио
"""
Извлечь текст:
- Проверяем, чтобы аудио было длиной выше 5 секунд;
- Извлекаем аудио-дорожку;
- Выводим return_as_file_keyboard
- Если пользователь выбрал первое, тогда бот отправляет edit сообщение с прогресс баром из 10 🤍 (10% = 💚). В конце бот отправляет файл с результатом пользователю, удалив прогресс бар. Если же пользователь выбрал второе, тогда бот отправляет edit сообщение с динамичной транскрибацией аудио-дорожки. Если размер edit файла превысил более 4000 символов, тогда бот продолжает в следующем сообщении.
- ДОП: добавить кнопку отменить для того, чтобы отменить транскрибацию.

Удалить шум:
- Удаляем шум и скидываем

Разделить вокал и фон:
- Разделяем аудио на фон и вокал и скидываем
"""
