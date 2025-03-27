from datetime import date as d, time as t

from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete, update, desc, text

from services.database.models import Device, Order, ModelType

def get_columns(class_):
    return {column.name for column in class_.__table__.columns}

class DB:
    def __init__(self, session: AsyncSession, model: type[ModelType]):
        self.session = session
        self.model = model

    async def _create(self, model_obj, obj_id: int) -> bool:
        if not await self.is_exists(obj_id):
            self.session.add(model_obj)
            await self.session.commit()
            return True
        return False

    async def get(
            self, obj_id: int = None, sort_by: str = None,
            where_statement = None, descend: bool = False,
    ):
        if obj_id:
            return await self._get_one(obj_id)
        elif sort_by:
            return await self._get_ordered_by(sort_by, descend)
        elif where_statement:
            return await self._get_where(where_statement)
        else:
            return await self._get_all()

    async def _get_one(self, obj_id: int):
        statement = select(self.model).where(self.where_model_id() == obj_id)
        device = (await self.session.execute(statement)).scalar()

        return device

    async def _get_all(self):
        model_objs = (await self.session.execute(select(self.model))).scalars().all()
        return model_objs

    async def _get_where(self, where_statement: str):
        statement = select(self.model).where(text(where_statement))

        model_objs = (await self.session.execute(statement)).scalars().all()
        return model_objs

    async def _get_ordered_by(self, sort_by: str, descend=False):
        valid_columns = get_columns(self.model)

        if sort_by in valid_columns:
            sort_column = getattr(self.model, sort_by)
        else:
            raise ValueError(f"Column '{sort_by}' does not exist in '{self.model.__name__}'.")

        sort_column = desc(sort_column) if descend else sort_column

        statement = select(self.model).order_by(sort_column)

        result = await self.session.execute(statement)
        return result.scalars().all()

    async def update(self, obj_id: int, **kwargs):
        valid_columns = get_columns(self.model)
        update_data = {key: value for key, value in kwargs.items() if key in valid_columns}

        if update_data:
            statement = update(self.model).where(self.where_model_id() == obj_id).values(update_data)
            await self.session.execute(statement)
            await self.session.commit()

        return await self._get_one(obj_id)

    async def delete(self, obj_id: int):
        device = await self._get_one(obj_id)

        statement = delete(self.model).where(self.where_model_id() == obj_id)
        await self.session.execute(statement)

        return device

    async def is_exists(self, obj_id: int = None) -> bool:
        if not obj_id:
            return False
        statement = select(self.model).where(self.where_model_id() == obj_id)
        result = await self.session.execute(statement)
        return result.scalar_one_or_none() is not None

    def where_model_id(self):
        if self.model is Device:
            return Device.device_id
        if self.model is Order:
            return Order.transaction_id

class Devices(DB):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Device)

    async def create(self, device_id: int):
        device = Device(device_id=device_id)
        return await self._create(device, device_id)

    async def update(self, obj_id: int, **kwargs):
        pass


class Orders(DB):
    def __init__(self, session: AsyncSession):
        super().__init__(session, Order)

    async def create(self, payment_name: str, transaction_id: int, amount: float, date: d,
                     time: t, status: bool, device: Device=None, log: str=None) -> bool:
        order = Order(payment_name=payment_name, transaction_id=transaction_id, amount=amount,
                      date=date, time=time, status=status, device=device, log=log)

        device_id = device.device_id if device else None
        return await self._create(order, device_id)
