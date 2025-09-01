import uuid

from pydantic import BaseModel, UUID4

class UserBot(BaseModel):
    username: str
    chat_id: int
    msg_id: int


class BrokerMsgBot(BaseModel):
    user: UserBot
    bot_msg_id: int
    request_id: str = str(uuid.uuid4())
    table_id: str
