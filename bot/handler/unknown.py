from aiogram import Router, F, types

from bot.utils.keybB import main_kb

router = Router()

@router.message(F.text.startswith('/'))
async def unknown_command(message: types.Message):
    await message.answer("ℹ️ Неизвестная команда. Введите /start для начала работы.",  reply_markup=main_kb())