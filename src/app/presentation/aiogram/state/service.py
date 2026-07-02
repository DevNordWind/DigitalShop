from aiogram.fsm.state import State, StatesGroup


class UnSelectedLangState(StatesGroup):
    select_lang = State()
