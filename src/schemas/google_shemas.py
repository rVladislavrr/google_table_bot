from pydantic import BaseModel, UUID4, Field


class TableUser(BaseModel):
    chat_id: int
    msg_id: int

class TableId(BaseModel):
    request_id: str | None = None
    bot_msg_id: int
    table_id: str
    user: TableUser

class GoogleAccess(BaseModel):
    status: str = "Ошибка"
    access: bool = False