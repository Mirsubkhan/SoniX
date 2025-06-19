from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

video_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"handle:transcribe")]
])

photo_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь печатный текст", callback_data=f"process:extract_text")],
    [InlineKeyboardButton(text="Улучшить качество", callback_data=f"process:upscale_image")],
    [InlineKeyboardButton(text="Удалить фон", callback_data=f"process:remove_bg")],
    [InlineKeyboardButton(text="Трансформировать в ASCII", callback_data=f"handle:transform_to_ascii")]
])

audio_process_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Извлечь текст", callback_data=f"handle:transcribe")],
    [InlineKeyboardButton(text="Извлечь фон. звук", callback_data=f"process:no_vocals.mp3")],
    [InlineKeyboardButton(text="Извлечь голос", callback_data=f"process:vocals.mp3")]
])

return_as_file_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="В .txt формате", callback_data=f"process:transcribe_in_file")],
    [InlineKeyboardButton(text="В этом чате", callback_data=f"process:transcribe_in_chat")]
])

transcribe_separate_options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="Не хочу", callback_data=f"process:transcribe_without_demucs")],
    [InlineKeyboardButton(text="Хочу", callback_data=f"process:transcribe_with_demucs")]
])

transform_options_keyboard = InlineKeyboardMarkup(inline_keyboard=[
    [InlineKeyboardButton(text="100", callback_data=f"process:100")],
    [InlineKeyboardButton(text="200", callback_data=f"process:200")],
    [InlineKeyboardButton(text="300", callback_data=f"process:300")]
])
