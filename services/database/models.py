from importlib import reload

from sqlalchemy import Time, Date, func, DateTime, mapped_column, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from services.database.engine import Base


class Device(Base):
    __tablename__ = 'devices'
    device_id: Mapped[int] = mapped_column(unique=True)

    transactions = relationship('PaymentTransaction', backref='device')

class PaymentTransaction(Base):
    __tablename__ = 'payment_transactions'

    payment_name: Mapped[str] = mapped_column()
    device_id: Mapped[int] = mapped_column(ForeignKey('devices.device_id'), nullable=True)
    transaction_id: Mapped[int] = mapped_column()
    amount: Mapped[float] = mapped_column()
    date = mapped_column(Date)
    time = mapped_column(Time)
    status: Mapped[bool] = mapped_column()
