import json
from datetime import timedelta

from bot.logger import setup_logging
from bot.redis_con import redis_client


log = setup_logging('Кеш')

async def get_cache_user_config(user_id: int):
    r = await redis_client.get_redis()
    log.info('Запрос в кеш о конфиге юзера')
    try:
        cached_data = await r.get(f"user_config:{user_id}")
        if cached_data:
            try:
                cached_data_dict = json.loads(cached_data)
                log.info('Конфиг получен из кеша')
                return cached_data_dict
            except json.JSONDecodeError:
                log.warning("Ошибка в декодировании")
                await r.delete(f"user_config:{user_id}")
                log.info('Ошибочный конфиг удалён')
        else:
            log.info('В кеше нет конфига')
            return None
    except Exception as e:
        log.critical("Ошибка при получении данных из кеша", exc_info=e)
        return None

async def set_cache_config(user_id: int, config: dict):
    r = await redis_client.get_redis()
    try:
        await r.setex(
            f"user_config:{user_id}",
            timedelta(seconds=30),
            json.dumps(config)
        )
        log.info('Конфиг сохранён в кеш')

    except Exception as e:
        log.critical('Ошибка либо в сохранении в кеш', exc_info=e)
        return None
