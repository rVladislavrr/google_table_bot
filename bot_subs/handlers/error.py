from faststream import Logger
from faststream.nats import NatsRouter

from bot_subs.bot import bot
from bot_subs.schemas.google_access import GoogleAccessAnswer

router = NatsRouter()


@router.subscriber("action_errors")
async def handle_error(msg: dict, logger: Logger):
    logger.info(f"Received error message: {msg}")
    try:
        await bot.send_message(
            msg["user_id"],
            f"⚠️ Ошибка: {msg['error']}\n"
            "Попробуйте позже или обратитесь в поддержку",
            reply_to_message_id=msg['msg_id']
        )
        logger.info("Message sent to user")
    except Exception as e:
        logger.error(f"Failed to send message: {e}")


@router.subscriber("bot.verify_access")
async def handle_error(msg: GoogleAccessAnswer, logger: Logger):
    logger.info(f"Пришло сообщение {msg.request_id}")
    try:
        await bot.delete_message(
            chat_id=msg.user.chat_id,
            message_id=msg.bot_msg_id,
        )
    except Exception as e:
        logger.error(f"Сообщение не удалилось {msg.request_id}", exc_info=e)
    finally:
        await bot.send_message(
            chat_id=msg.user.chat_id,
            reply_to_message_id=msg.user.msg_id,
            text=msg.status,
            reply_markup=None
        )
        logger.info(f"Ушёл ответ {msg.request_id}")  # Для отладки
