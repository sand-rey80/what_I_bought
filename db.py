import datetime
from typing import List, Any, Awaitable, Callable, Dict
from sqlalchemy import func, select, DateTime
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped

from aiogram import BaseMiddleware
from aiogram.types import Message, TelegramObject

engine = create_async_engine("sqlite+aiosqlite:///sqdata.db")
session_maker = async_sessionmaker(engine, class_=AsyncSession)

class DataBaseSession(BaseMiddleware):
    def __init__(self, session_pool: async_sessionmaker):
        self.session_pool = session_pool

    async def __call__(
        self,
        handler: Callable[[TelegramObject, Dict[str, Any]], Awaitable[Any]],
        event: TelegramObject,
        data: Dict[str, Any],
            ) -> Any:
        async with self.session_pool() as session:
            data['session'] = session
            return await handler(event, data)


class Model(DeclarativeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)
    create_date: Mapped[datetime.datetime] = mapped_column(server_default=func.now())

    def to_dict(self) -> dict:
        """Универсальный метод для конвертации объекта SQLAlchemy в словарь"""
        # Получаем маппер для текущей модели
        columns = class_mapper(self.__class__).columns
        # Возвращаем словарь всех колонок и их значений
        return {column.key: getattr(self, column.key) for column in columns}

class Ticket(Model):
    __tablename__ = "tickets"
    qr_value: Mapped[str]
    tg_id: Mapped[str]
   # def __repr__(self) -> str:
    #    return f'Ticket(id={self.id}, create_date ={self.create_date}, qr_value={self.qr_value}, tg_id={self.tg_id}'


async def insert_ticket(async_session: session_maker, ticket: Ticket) -> None:
    async with async_session() as session:
        #async with session.begin():
            session.add(ticket)
            await session.commit()


async def get_tickets(date_from: datetime, date_to: datetime) -> Dict:
    async with session_maker() as session:
        query = select(Ticket).filter(Ticket.create_date.between(date_from, date_to))
        result = await session.execute(query)
        ticket_list = result.scalars().all()
        return ticket_list


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.create_all)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

