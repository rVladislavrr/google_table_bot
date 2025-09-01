from aiohttp.abc import HTTPException
from fastapi import APIRouter, HTTPException, status, Request

from src.fs_broker import broker
from src.logger import setup_logging
from src.schemas import TableId

router = APIRouter(
)

log = setup_logging('Роутер verify_access')

@router.post('/verify_access')
async def verify_google_access(
        request: Request,
        tableId: TableId
):
    try:
        log.info(f"Запрос принял {request.state.request_id}")
        tableId.request_id = request.state.request_id
        await broker.publish(tableId, subject="verify_access")
        log.info(f'Запрос перенаправлен в брокер {request.state.request_id}')
    except Exception as e:
        log.error(f'Запрос не был перенаправлен {request.state.request_id}', exc_info=e)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail={"status": "Ошибка при "
                                                                                                 "публикации задачи"})

    return {
        'detail': {
            'status': 'ok',
            'request_id': request.state.request_id
        }
    }
