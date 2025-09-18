
from aiogram import Router
from aiogram.types import Message
import yaml
from pathlib import Path
router=Router()
DIALOGS=yaml.safe_load((Path(__file__).parent.parent/"dialogs.yaml").read_text(encoding="utf-8"))
@router.message(lambda m: m.text=="💬 Задать вопрос")
async def prompt_hint(message: Message): await message.answer("Задайте ваш вопрос. Я отвечу по базе знаний.")
@router.message()
async def smalltalk_or_faq(message: Message):
    text=(message.text or "").lower().strip()
    for item in DIALOGS.get("smalltalk", []):
        if any(q in text for q in item.get("q", [])): return await message.answer(item.get("a",""))
    faq=DIALOGS.get("faq",{})
    if any(w in text for w in ["достав","адрес","привез"]): return await message.answer(faq.get("delivery",""))
    if any(w in text for w in ["оплат","счет","цена","стоим"]): return await message.answer(faq.get("payment",""))
    if any(w in text for w in ["материал","кирпич","блок"]): return await message.answer(faq.get("materials",""))
    return await message.answer('Не совсем понял. Могу оформить заявку: нажмите "🧱 Оформить заявку".')
