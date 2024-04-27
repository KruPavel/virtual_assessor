from aiogram.filters.callback_data import CallbackData


class Course(CallbackData, prefix='course'):
    name: str
    code: str
    lessons: list


class CompressedCourse(CallbackData, prefix='compressed_course'):
    code: str


class Lesson(CallbackData, prefix='lesson'):
    index : int