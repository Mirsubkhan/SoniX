from aiogram import Bot

class TelegramProgressBarRenderer:
    def __init__(self, bot: Bot=None, chat_id: int=None, message_id: int=None):
        self.bot = bot
        self.chat_id = chat_id
        self.message_id = message_id

    async def demucs_progress_callback(self, percent: int):
        hearts = "💚" * (percent // 10) + "🤍" * (10 - (percent // 10))
        try:
            await self.bot.edit_message_text(
                chat_id=self.chat_id,
                message_id=self.message_id,
                text=f"🎧 Разделение музыки...\n{hearts} | {percent}%"
            )
        except Exception as e:
            pass

    async def static_whisper_progress_callback(self, filled: int):
        hearts = "💚" * filled + "🤍" * (10 - filled)
        res = f"📝 Транскрибация...\n{hearts} | {filled * 10}%"

        await self.bot.edit_message_text(
            chat_id=self.chat_id,
            message_id=self.message_id,
            text=res
        )

    async def dynamic_whisper_progress_callback(self, text: str, is_full: bool):
        if not is_full:
            await self.bot.edit_message_text(
                chat_id=self.chat_id,
                message_id=self.message_id,
                text=text
            )
        else:
            new_edit_msg = await self.bot.send_message(text=text, chat_id=self.chat_id)
            self.message_id = new_edit_msg.message_id