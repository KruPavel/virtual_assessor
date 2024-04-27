from aiogram.filters.callback_data import CallbackData


class Course(CallbackData, prefix='course'):
    name: str
