from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase, mapped_column, Mapped


engine = create_async_engine("sqlite+aiosqlite:///sqdata.db")

ses_maker = async_sessionmaker(engine)

class Model(DeclaratibeBase):
    pass

class TicketsOrm(Model):
    __tablename__ = "tickets"
    id: Mapped[int] = mapped_column(primary_key=True)


async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.creat_all)


async def drop_all_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Model.metadata.drop_all)

