from aiogram import Router
from aiogram.types import Message
from aiogram.filters import CommandStart
from ..keyboards import main_kb
import yaml
from pathlib import Path

router = Router()
DIALOGS = yaml.safe_load((Path(__file__).parent.parent / "dialogs.yaml").read_text(encoding="utf-8"))

@router.message(CommandStart())
async def start(message: Message):
    welcome = DIALOGS.get("welcome", [])
    text = "\n".join(welcome) if welcome else "Здравствуйте!"
    await message.answer(text, reply_markup=main_kb)
