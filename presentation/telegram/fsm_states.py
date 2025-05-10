from aiogram.fsm.state import StatesGroup, State

class FileProcessing(StatesGroup):
    file_received = State()