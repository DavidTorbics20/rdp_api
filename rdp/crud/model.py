from typing import List
from typing import Optional
from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy import String, Float, DateTime

from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, relationship
from sqlalchemy.orm import sessionmaker


class Base(DeclarativeBase):
    pass


class ValueType(Base):
    __tablename__ = "value_type"
    id: Mapped[int] = mapped_column(primary_key=True)
    type_name: Mapped[str]
    type_unit: Mapped[str]

    values: Mapped[List["Value"]] = relationship(
        back_populates="value_type", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"ValueType(id={self.id!r}, value_type={self.type_name})"


class Value(Base):
    __tablename__ = "value"
    id: Mapped[int] = mapped_column(primary_key=True)
    time: Mapped[int] = mapped_column()
    value: Mapped[float] = mapped_column()
    value_type_id: Mapped[int] = mapped_column(ForeignKey("value_type.id"))
    device_id: Mapped[int] = mapped_column(ForeignKey("device.id"))

    value_type: Mapped["ValueType"] = relationship(back_populates="values")
    device: Mapped["Device"] = relationship(back_populates="devices")

    __table_args__ = (
        UniqueConstraint("time", "value_type_id", "device_id", name="value integrity"), 
    )

    def __repr__(self) -> str:
        return f"Value(id={self.id!r}, value_time={self.time!r} value_type={self.value_type.type_name!r}, value={self.value})"

class Device(Base):
    __tablename__ = "device"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column()
    room_id: Mapped[int] = mapped_column(ForeignKey("room.id"), nullable=True)

    room: Mapped["Room"] = relationship(back_populates="rooms")

    devices: Mapped[List["Value"]] = relationship(
        back_populates="device", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Device(id={self.id!r}, device_name={self.name!r})"

class Room(Base):
    __tablename__ = "room"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_name: Mapped[str] = mapped_column()
    room_group_id: Mapped[str] = mapped_column(ForeignKey("room_group.id"), nullable=True)

    room_group: Mapped["RoomGroup"] = relationship(back_populates="room_groups")

    rooms: Mapped["Device"] = relationship(
        back_populates="room", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"Room(id={self.id!r}, room_name={self.room_name!r}, room_group={self.room_group!r})"

class RoomGroup(Base):
    __tablename__ = "room_group"
    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    room_group_name: Mapped[str] = mapped_column()

    # room_group: Mapped["RoomGroup"] = relationship(back_populates="room_groups")

    room_groups: Mapped["Room"] = relationship(
        back_populates="room_group", cascade="all, delete-orphan"
    )

    def __repr__(self) -> str:
        return f"RoomGroup(id={self.id!r}, room_group_name={self.room_group_name!r})"
