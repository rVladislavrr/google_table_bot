from faststream import Logger, Depends
from faststream.nats import NatsRouter

from server_subs.db import db
from server_subs.schemas.users import GoogleAccessAnswer

router = NatsRouter()


@router.subscriber("bot.verify_access")
async def handler_bot_verify_access(msg: GoogleAccessAnswer,
                                    logger: Logger,
                                    session=Depends(db.get_async_session)):
    logger.info(f"Пришло сообщение {msg.request_id}")
    if msg.access:
        Users = db.get_model('users')
        userOrm = Users(telegram_id=msg.user.chat_id,
                        table_id=msg.table_id,
                        )
        session.add(userOrm)
        await session.commit()
        logger.info('Юзер сохранён')
    else:
        logger.info('Доступа нет')

    logger.info(f"Ушёл ответ")
