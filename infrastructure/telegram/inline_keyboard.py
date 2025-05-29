from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

video_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"transcribe")]
])

photo_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"extract_text")],
    [InlineKeyboardButton(text="Улучшить качество", callback_data=f"upscale_image")],
    [InlineKeyboardButton(text="Удалить фон", callback_data=f"remove_bg")],
    [InlineKeyboardButton(text="Трансформировать в ASCII", callback_data=f"transform_to_ascii")]
])

audio_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"transcribe")],
    [InlineKeyboardButton(text="Удалить фон. звук", callback_data=f"separate_bg")],
    [InlineKeyboardButton(text="Удалить голос", callback_data=f"separate_voice")]
])

return_as_file_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В .txt формате", callback_data=f"file")],
    [InlineKeyboardButton(text="В этом чате", callback_data=f"no_file")]
])

transform_options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="100", callback_data=f"100")],
    [InlineKeyboardButton(text="150", callback_data=f"150")],
    [InlineKeyboardButton(text="200", callback_data=f"200")],
    [InlineKeyboardButton(text="250", callback_data=f"250")],
    [InlineKeyboardButton(text="300", callback_data=f"300")]
])
