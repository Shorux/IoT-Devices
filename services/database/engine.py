from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

from config import DATABASE_URL

engine = create_async_engine(DATABASE_URL, echo=False)
async_session = async_sessionmaker(engine, autoflush=False)


class Base(DeclarativeBase):
    pk: Mapped[int] = mapped_column(primary_key=True)
    
    def __repr__(self):
        table_name = self.__tablename__.capitalize().rstrip('s')
        return f'{table_name}<{self.pk}>'

session = async_session()

async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
