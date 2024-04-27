from aiogram.fsm.state import State, StatesGroup


class GetAnswer(StatesGroup):
    answer: State = State()
