from aiogram.fsm.state import State, StatesGroup


class ProductState(StatesGroup):
    waiting_for_artikul = State()
