from aiogram import Bot, Dispatcher, Router, types
from aiogram.filters import Command
from aiogram.client.session.base import BaseSession

import json
from text import *


class AssesorBot(Bot):
    def __init__(self, token: str, session: BaseSession | None = None, parse_mode: str | None = None, disable_web_page_preview: bool | None = None, protect_content: bool | None = None) -> None:
        super().__init__(token, session, parse_mode,
                         disable_web_page_preview, protect_content)
        self.dispatcher = Dispatcher()
        self.router = Router()
        self.dispatcher.include_router(self.router)

        self.default_commands = [
            types.BotCommand(command='start', description='Запуск бота')
        ]

        self.router.message.register(self.start, Command('start'))

    async def start(self, message: types.Message):
        await self.set_my_commands(self.default_commands)
        await message.answer(text=f"Здравствуйте, <b>{message.from_user.first_name}</b>! " + start_text, parse_mode='html')


if __name__ == '__main__':
    with open('info.json', 'r') as file:
        data = json.load(file)
        bot = AssesorBot(token=data.get('token'))
        bot.dispatcher.run_polling(bot)
