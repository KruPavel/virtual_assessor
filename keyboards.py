from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardButton
import json

from filters import Course, CompressedCourse, Lesson


def get_courses():
    data = dict()
    with open('data.json', 'r', encoding='utf-8') as file:
        data = json.load(file)

    courses = []
    for value in list(data.values()):
        name = ''
        code = ''
        lessons = []
        for k, v in value.items():
            if k == 'name':
                name = v
            elif k == 'code':
                code = v
            else:
                for val in list(v.values()):
                    lessons.append(val)
        courses.append(Course(name=name, code=code, lessons=lessons))

    return courses


def choose_keyboard():
    courses = get_courses()

    choose_markup = InlineKeyboardBuilder()
    for course in courses:
        choose_markup.row(InlineKeyboardButton(
            text=course.name, callback_data=CompressedCourse(code=course.code).pack()))

    return choose_markup.as_markup()


def get_course_keyboard(code):
    courses = get_courses()

    for elem in courses:
        if elem.code == code:
            course = elem
            break

    course_markup = InlineKeyboardBuilder()
    for i, value in enumerate(course.lessons):
        course_markup.row(InlineKeyboardButton(
            text=f"{i + 1}. {value}", callback_data=Lesson(index=int(i + 1), course_code=code).pack()))
    course_markup.row(InlineKeyboardButton(
        text='Назад', callback_data=Lesson(index=-1, course_code='').pack()))
    return course_markup.as_markup()
