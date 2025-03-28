from sqlalchemy import Time, Date, ForeignKey, BigInteger, DateTime, func
from sqlalchemy.orm import Mapped, relationship, mapped_column
from typing_extensions import TypeVar

from services.database.engine import Base


class Device(Base):
    __tablename__ = 'devices'
    device_id: Mapped[int] = mapped_column(unique=True)

    orders = relationship('Order', backref='device')

class Order(Base):
    __tablename__ = 'orders'

    payment_name: Mapped[str] = mapped_column(nullable=True)
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.device_id'), nullable=True)
    transaction_id: Mapped[str] = mapped_column(nullable=True)
    amount: Mapped[float] = mapped_column(nullable=True)
    date = mapped_column(Date, nullable=True)
    time = mapped_column(Time, nullable=True)
    status: Mapped[bool] = mapped_column(nullable=True)
    log: Mapped[str] = mapped_column(nullable=True)
    created_at = mapped_column(DateTime, default=func.now())

ModelType = TypeVar("ModelType", bound=Base)
