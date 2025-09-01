from aiogram import BaseMiddleware, types


class CommandCancelMiddleware(BaseMiddleware):
    async def __call__(self, handler, event, data):
        if (isinstance(event, types.Message) and
                event.text and
                event.text.startswith('/')):

            state = data['state']
            if await state.get_state():
                await state.clear()
                await event.answer(
                    "❌ Конфигурация отменена",
                    reply_markup=types.ReplyKeyboardRemove()
                )

        return await handler(event, data)