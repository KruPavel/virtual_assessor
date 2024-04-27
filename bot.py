from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession

import json
from text import *
from keyboards import choose_keyboard
from filters import Course


class AssesorBot(Bot):
    def __init__(self, token: str, session: BaseSession | None = None, parse_mode: str | None = None, disable_web_page_preview: bool | None = None, protect_content: bool | None = None) -> None:
        super().__init__(token, session, parse_mode,
                         disable_web_page_preview, protect_content)
        self.dispatcher = Dispatcher()
        self.router = Router()
        self.dispatcher.include_router(self.router)

        self.default_commands = [
            types.BotCommand(command='start', description='Запуск бота'),
            types.BotCommand(command='choose_course',
                             description='Выбор курса')
        ]

        self.router.message.register(self.start, Command('start'))
        self.router.message.register(
            self.choose_course, Command('choose_course'))
        self.router.callback_query.register(self.choosing_course, Course.filter())

    async def start(self, message: types.Message):
        await self.set_my_commands(self.default_commands)
        await message.answer(text=f"Здравствуйте, <b>{message.from_user.first_name}</b>! " + start_text, parse_mode='html')

    async def choose_course(self, message: types.Message):
        await message.answer(text=choose_text, reply_markup=choose_keyboard())

    async def choosing_course(self, query: types.callback_query.CallbackQuery, callback_data: Course):
        await query.message.answer(text=callback_data.name)


if __name__ == '__main__':
    with open('info.json', 'r') as file:
        data = json.load(file)
        bot = AssesorBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
