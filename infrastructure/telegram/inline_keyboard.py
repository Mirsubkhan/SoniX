from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

video_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"transcribe")]
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

