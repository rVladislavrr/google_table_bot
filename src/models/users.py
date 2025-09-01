from sqlalchemy import func
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from src.models.base import Base


class Users(Base):
    __tablename__ = 'users'

    uuid: Mapped[UUID] = mapped_column(UUID(as_uuid=True), server_default=func.gen_random_uuid(),
                                       nullable=False, index=True, primary_key=True)

    telegram_id: Mapped[int] = mapped_column(unique=True, index=True, primary_key=True)
    table_id: Mapped[str] = mapped_column(unique=True)


