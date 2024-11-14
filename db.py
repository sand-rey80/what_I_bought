from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped, sessionmaker

engine = create_async_engine("sqlite+aiosqlite:///sqdata.db")
ses_maker = async_sessionmaker(engine)

class Model(DeclaratibeBase):
    __abstract__ = True
    id: Mapped[int] = mapped_column(primary_key=True)


class TicketsOrm(Model):
    __tablename__ = "tickets"
    qr_value: Mapped[str]


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.creat_all)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

