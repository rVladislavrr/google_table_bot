from aiogram.client.session import aiohttp
from aiohttp import ClientResponse

from bot.config import botSettings
from bot.logger import setup_logging
from bot.schemas import BrokerMsgBot

log = setup_logging("Запросы на сервер")

class ServerHTTPError(Exception):
    def __init__(self, message, status_code=None, payload=None):
        self.message = message
        self.status_code = status_code
        self.payload = payload
        super().__init__(message)

async def verify_google_sheet_access(broker_msg: BrokerMsgBot) -> ClientResponse:
    async with aiohttp.ClientSession() as session:
        try:
            async with session.post(f"{botSettings.SERVER_URL}/api/v1/verify_access",
                                    json=broker_msg.model_dump()) as response:
                if response.ok:
                    data = await response.json()
                    log.info(f'Сервер отправил запрос в обработку {data.get('detail', dict()).get('request_id')}')
                    return response
                else:
                    raise ServerHTTPError('Ошибка в принятии данных сервером',
                                          status_code=response.status,
                                          payload=await response.json())
        except ServerHTTPError as e:
            log.error(f'Сервер не начал обработку {e.status_code}, {e.payload}')
            raise
        except Exception as e:
            log.critical('Ошибка при отправке данных на сервер', exc_info=e)
            raise Exception("Не удалось отправить данные")

async def fetch_to_config(user_id: int):
    try:
        async with aiohttp.ClientSession() as session:

            async with session.get(f"{botSettings.SERVER_URL}/api/v1/users/{user_id}") as response:
                log.info('Запрос на сервер для конфига')
                if response.ok:
                    log.info('Конфиг получен')
                    return await response.json()
                log.info('Конфига нет')
                return None
    except Exception as e:
        log.critical('Ошибка при отправке данных на сервер', exc_info=e)
        raise Exception("Не удалось получить данные с сервера")

async def fetch_delete_to_config(user_id: int) -> int:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.delete(f"{botSettings.SERVER_URL}/api/v1/users/{user_id}") as response:
                log.info('Запрос на удаление конфига')
                if response.ok:
                    log.info('Конфиг удалён')
                    return 200
                if response.status == 404:
                    log.info('Конфига не было')
                    return 404
    except Exception as e:
        log.critical('Ошибка при отправке данных на сервер', exc_info=e)
        raise Exception("Не удалось получить данные с сервера")