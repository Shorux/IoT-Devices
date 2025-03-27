from sqlalchemy import Time, Date, ForeignKey, BigInteger
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing_extensions import TypeVar

from services.database.engine import Base


class Device(Base):
    __tablename__ = 'devices'
    device_id: Mapped[int] = mapped_column(unique=True)

    orders = relationship('Order', backref='device')

class Order(Base):
    __tablename__ = 'orders'

    payment_name: Mapped[str] = mapped_column()
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.device_id'), nullable=True)
    transaction_id = mapped_column(BigInteger)
    amount: Mapped[float] = mapped_column()
    date = mapped_column(Date)
    time = mapped_column(Time)
    status: Mapped[bool] = mapped_column()
    log: Mapped[str] = mapped_column(nullable=True)

ModelType = TypeVar("ModelType", bound=Base)
