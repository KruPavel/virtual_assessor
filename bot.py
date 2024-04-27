from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession
from aiogram.utils.keyboard import InlineKeyboardBuilder


import csv
import json
from random import randint
from text import *
from keyboards import choose_keyboard, get_course_keyboard
from filters import CompressedCourse, Lesson


class AssesorBot(Bot):
    def __init__(self, token: str, session: BaseSession | None = None, parse_mode: str | None = None, disable_web_page_preview: bool | None = None, protect_content: bool | None = None) -> None:
        super().__init__(token, session, parse_mode,
                         disable_web_page_preview, protect_content)
        self.dispatcher = Dispatcher()
        self.router = Router()
        self.dispatcher.include_router(self.router)
        self.questions = [[[] for _ in range(6)], [[] for _ in range(6)]]

        self.default_commands = [
            types.BotCommand(command='start', description='Запуск бота'),
            types.BotCommand(command='choose_course',
                             description='Выбор курса')
        ]

        self.router.message.register(self.start, Command('start'))
        self.router.message.register(
            self.choose_course, Command('choose_course'))
        self.router.callback_query.register(
            self.choosing_course, CompressedCourse.filter())
        self.router.callback_query.register(
            self.choossing_lesson, Lesson.filter())

    async def start(self, message: types.Message):
        await self.set_my_commands(self.default_commands)
        await message.answer(text=f"Здравствуйте, <b>{message.from_user.first_name}</b>! " + start_text, parse_mode='html')
        with open('train_dataset_train_Assessor/train_Assessor/train_data.csv', encoding='utf-8') as file:
            file_reader = csv.reader(file, delimiter=',')
            flag = True
            for row in file_reader:
                if flag:
                    flag = False
                    continue
                course, lesson = row[3].split(
                    '_')[0], int(row[3].split('_')[2])
                if course == 'process':
                    self.questions[0][lesson - 1].append(row[0])
                elif course == 'introduction':
                    self.questions[1][lesson - 1].append(row[0])

    async def choose_course(self, message: types.Message):
        await message.answer(text="Выберите курс: ", reply_markup=choose_keyboard())

    async def choosing_course(self, query: types.callback_query.CallbackQuery, callback_data: CompressedCourse):
        await query.message.edit_text(text="Выберите урок: ", reply_markup=get_course_keyboard(callback_data.code))

    async def choossing_lesson(self, query: types.callback_query.CallbackQuery, callback_data: Lesson):
        if callback_data.index == -1:
            await query.message.edit_text(text="Выберите курс: ", reply_markup=choose_keyboard())
            return

        if len(self.questions[callback_data.course_code == 'introduction'][callback_data.index - 1]) != 0:
            await query.message.edit_text(text=self.questions[callback_data.course_code == 'introduction'][callback_data.index - 1][randint(0, len(self.questions[callback_data.course_code == 'introduction'][callback_data.index - 1]) - 1)], reply_markup=InlineKeyboardBuilder().as_markup())
        else:
            await query.message.answer(text='Извините, нет вопросов на данную тему.')


if __name__ == '__main__':
    with open('info.json', 'r') as file:
        data = json.load(file)
        bot = AssesorBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
