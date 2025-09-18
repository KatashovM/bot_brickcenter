
from aiogram.fsm.state import StatesGroup, State
class OrderForm(StatesGroup):
    material=State(); quantity_value=State(); quantity_unit=State()
    delivery_type=State(); delivery_address=State()
    name=State(); phone=State(); email=State(); confirm=State()
