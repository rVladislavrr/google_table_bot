from faststream import Logger
from faststream.nats import NatsRouter

from google_subs.google_utils import verify_google_sheet_access
from google_subs.shemas.google_shemas import GoogleAccess, GoogleAccessAnswer

router = NatsRouter()


@router.subscriber("verify_access")
@router.publisher("bot.verify_access")
async def verify_access(
        logger: Logger,
        google_credentials: GoogleAccess
):
    logger.info(f"Запрос в обработке {google_credentials.request_id}")
    answer: GoogleAccessAnswer = await verify_google_sheet_access(google_credentials, logger)
    logger.info(f"Ушло в ответ {google_credentials.request_id}")

    return answer



    # await broker.publish({'user_id': google_credentials.user.chat_id,
    #                       'msg_id': google_credentials.user.msg_id,
    #                       'error': 'проблема'}, subject='action_errors', )
    # logger.info("Ушло в ответ: {}".format({'user_id': google_credentials.user.chat_id,
    #                                        'msg_id': google_credentials.user.msg_id,
    #                                        'error': 'проблема'}))

