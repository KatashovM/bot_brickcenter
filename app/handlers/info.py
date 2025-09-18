
from aiogram import Router, F
from aiogram.types import Message
import yaml
from pathlib import Path
router=Router()
DIALOGS=yaml.safe_load((Path(__file__).parent.parent/"dialogs.yaml").read_text(encoding="utf-8"))
@router.message(F.text=="ℹ️ Информация")
async def info(message: Message):
    faq=DIALOGS.get("faq",{})
    parts=["**Информация**:", f"— {faq.get('delivery','')}", f"— {faq.get('payment','')}", f"— {faq.get('materials','')}"]
    await message.answer("\n".join(p for p in parts if p))
