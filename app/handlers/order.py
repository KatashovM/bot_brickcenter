
from aiogram import Router, F
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.context import FSMContext
from ..states import OrderForm
from ..storage import OrderDraft
from ..keyboards import quantity_unit_kb, delivery_type_kb, confirm_kb, main_kb
from ..config import settings
from ..models import SessionLocal, Order
from ..mailer import send_mail
import app.models as m
from app.config import settings
router=Router()
@router.message(F.text=="🧱 Оформить заявку")
@router.message(F.text=="/order")
async def order_start(message: Message, state: FSMContext):
    await state.set_state(OrderForm.material); await state.update_data(draft=OrderDraft().__dict__)
    await message.answer("Какой материал нужен? Укажите наименование и, при необходимости, цвет/марку.")
@router.message(OrderForm.material)
async def set_material(message: Message, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft")); d.material=message.text.strip()
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.quantity_value)
    await message.answer("Сколько требуется? Укажите число.")
@router.message(OrderForm.quantity_value, F.text.regexp(r"^\d+[\,\.]?\d*$"))
async def set_quantity_value(message: Message, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft")); d.quantity_value=message.text.replace(",", ".")
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.quantity_unit)
    await message.answer("В каких единицах?", reply_markup=quantity_unit_kb())
@router.message(OrderForm.quantity_value)
async def quantity_value_invalid(message: Message): await message.answer("Введите число, например 120 или 18.5")
@router.callback_query(F.data.startswith("unit:"))
async def set_quantity_unit(c: CallbackQuery, state: FSMContext):
    u=c.data.split(":",1)[1]; d=OrderDraft(**(await state.get_data()).get("draft")); d.quantity_unit=u
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.delivery_type)
    await c.message.edit_reply_markup(); await c.message.answer("Тип доставки?", reply_markup=delivery_type_kb())
@router.callback_query(F.data.startswith("del:"))
async def set_delivery_type(c: CallbackQuery, state: FSMContext):
    t=c.data.split(":",1)[1]; d=OrderDraft(**(await state.get_data()).get("draft")); d.delivery_type=t
    await state.update_data(draft=d.__dict__); await c.message.edit_reply_markup()
    if t=="site": await state.set_state(OrderForm.delivery_address); await c.message.answer("Укажите адрес доставки (город, улица, объект).")
    else: await state.set_state(OrderForm.name); await c.message.answer("Ваше имя?")
@router.message(OrderForm.delivery_address)
async def set_delivery_address(message: Message, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft")); d.delivery_address=message.text.strip()
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.name); await message.answer("Ваше имя?")
@router.message(OrderForm.name)
async def set_name(message: Message, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft")); d.name=message.text.strip()
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.phone); await message.answer("Номер телефона? (+7...) ")
@router.message(OrderForm.phone, F.text.regexp(r"^\+?\d[\d\s\-]{7,}$"))
async def set_phone(message: Message, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft")); d.phone=message.text.strip()
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.email); await message.answer("Email для связи и счёта?")
@router.message(OrderForm.phone)
async def phone_invalid(message: Message): await message.answer("Некорректный номер. Пример: +7 999 123-45-67")
@router.message(OrderForm.email, F.text.regexp(r"^[^\s@]+@[^\s@]+\.[^\s@]+$"))
async def set_email(message: Message, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft")); d.email=message.text.strip()
    await state.update_data(draft=d.__dict__); await state.set_state(OrderForm.confirm)
    unit="шт" if d.quantity_unit=="pcs" else "м²"; deliv="На склад" if d.delivery_type=="warehouse" else "До объекта"
    lines=["Проверьте заявку:", f"Материал: {d.material}", f"Количество: {d.quantity_value} {unit}", f"Доставка: {deliv}"]
    if d.delivery_type=="site": lines.append(f"Адрес: {d.delivery_address}")
    lines += [f"Имя: {d.name}", f"Телефон: {d.phone}", f"Email: {d.email}"]
    await message.answer("\n".join(lines), reply_markup=confirm_kb())
@router.message(OrderForm.email)
async def email_invalid(message: Message): await message.answer("Неверный email. Пример: name@example.com")
@router.callback_query(F.data=="confirm:cancel")
async def confirm_cancel(c: CallbackQuery, state: FSMContext):
    await state.clear(); await c.message.edit_reply_markup(); await c.message.answer("Заявка отменена.", reply_markup=main_kb)
@router.callback_query(F.data=="confirm:edit")
async def confirm_edit(c: CallbackQuery, state: FSMContext):
    await c.message.edit_reply_markup(); await c.message.answer("Что хотите изменить? Введите материал заново."); await state.set_state(OrderForm.material)
@router.callback_query(F.data=="confirm:yes")
async def confirm_yes(c: CallbackQuery, state: FSMContext):
    d=OrderDraft(**(await state.get_data()).get("draft"))
    if m.Engine is None or m.SessionLocal is None:
        m.setup_db(settings.db_path)
    s=m.SessionLocal()
    s.add(Order(material=d.material or "", quantity_value=d.quantity_value or "", quantity_unit=d.quantity_unit or "",
                delivery_type=d.delivery_type or "", delivery_address=d.delivery_address or "",
                name=d.name or "", phone=d.phone or "", email=d.email or ""))
    s.commit()
    unit="шт" if d.quantity_unit=="pcs" else "м²"; deliv="На склад" if d.delivery_type=="warehouse" else "До объекта"
    text=("Новая заявка:\n"
          f"Материал: {d.material}\nКол-во: {d.quantity_value} {unit}\nДоставка: {deliv}\n"
          + (f"Адрес: {d.delivery_address}\n" if d.delivery_type=='site' else "")
          + f"Имя: {d.name}\nТелефон: {d.phone}\nEmail: {d.email}")
    await c.bot.send_message(chat_id=settings.admin_chat_id, text=text)
    try:
        await send_mail(settings.smtp_host, settings.smtp_port, settings.smtp_user, settings.smtp_password,
                        settings.mail_from, settings.mail_to, "Новая заявка из Telegram", text)
    except Exception as e:
        await c.bot.send_message(settings.admin_chat_id, text=f"Ошибка отправки email: {e}")
    await state.clear(); await c.message.edit_reply_markup()
    await c.message.answer("Спасибо! Ваша заявка отправлена. Мы свяжемся с вами в ближайшее время.", reply_markup=main_kb)
