from bot.utils.redis_req import get_cache_user_config, set_cache_config
from bot.utils.req import fetch_to_config


async def get_user_config(user_id: int):
    config = await get_cache_user_config(user_id)

    if not config:
        config = await fetch_to_config(user_id)
        if config:
            await set_cache_config(user_id, config)

    return config
