from pydantic import BaseModel


class GoogleUser(BaseModel):
    chat_id: int
    msg_id: int


class GoogleAccess(BaseModel):
    request_id: str
    bot_msg_id: int
    table_id: str
    user: GoogleUser


class GoogleAccessAnswer(GoogleAccess):
    access: bool
    status: str
