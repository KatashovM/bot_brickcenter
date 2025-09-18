
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.utils.keyboard import InlineKeyboardBuilder
main_kb = ReplyKeyboardMarkup(
    keyboard=[[KeyboardButton(text="🧱 Оформить заявку"), KeyboardButton(text="ℹ️ Информация")],
              [KeyboardButton(text="💬 Задать вопрос")]], resize_keyboard=True)
def quantity_unit_kb():
    kb=InlineKeyboardBuilder(); kb.button(text="в штуках", callback_data="unit:pcs"); kb.button(text="в м²", callback_data="unit:m2")
    kb.adjust(2); return kb.as_markup()
def delivery_type_kb():
    kb=InlineKeyboardBuilder(); kb.button(text="На склад", callback_data="del:warehouse"); kb.button(text="До объекта", callback_data="del:site")
    kb.adjust(2); return kb.as_markup()
def confirm_kb():
    kb=InlineKeyboardBuilder(); kb.button(text="✅ Подтвердить", callback_data="confirm:yes")
    kb.button(text="✏️ Изменить", callback_data="confirm:edit"); kb.button(text="❌ Отменить", callback_data="confirm:cancel")
    kb.adjust(2,1); return kb.as_markup()
